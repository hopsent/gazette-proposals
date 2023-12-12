import logging
from logging.handlers import RotatingFileHandler
from time import sleep
from typing import Union, List
import os
import json

from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from core.extractor import Extractor
from core.letter import Letter
from core.data import ExcelData as ED
from core.data import PagesData as PD
from core.data import StatusData as ST
from core.data import StoredGazette as SG
from core.data import DirectoryStorage as DS


formater = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(process)d, %(message)s, %(name)s'
)
handler = RotatingFileHandler(
    'logs/' + __name__ + '.log',
    maxBytes=52428800,
)
handler.setFormatter(formater)
handler.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
logger.addHandler(handler)


class Reader:
    """
    Считывает информацию с целевого сайта.
    Сохраняет файлы .pdf, записывает нужные данные в объекты LetterData().
    """

    def __init__(self,
                 articles: List[Letter] = [],
                 status: Union[int, str] = ST.OK
                 ) -> None:
        self.articles = articles
        self.status = status

    def choose_summary(self, wait: WebDriverWait) -> Union[str, None]:
        """
        Выбираем нужную опцию из поля summary.
        """

        # Ждем отображения поля summary.
        try:
            sleep(2)
            summary_field = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, PD.FORM_DATA['summary'])
                )
            )
            # Выбираем нужное summary.
            Select(summary_field).select_by_visible_text(PD.OPTIONS['summary'])
        except Exception:
            self.status = ST.NO_SECTION
            logger.error(self.status, exc_info=True)
            return self.status

    def get_gazette(self, driver: Firefox) -> Union[str, int]:
        """
        Получаем последнюю газету. Если последняя газета уже получена
        ранее (сохранена в файле old_gazette.txt), то сообщаем об этом.
        """

        wait = WebDriverWait(driver, 20)
        self.choose_summary(wait)

        # Проверяем, не читали ли мы эту газету ранее.
        try:
            sleep(2)
            gazette_number = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, PD.FORM_DATA['No'])
                    )
                )
            issue = Select(gazette_number).first_selected_option.text.split()[0]
        except Exception:
            self.status = ST.NO_OPTION
            logger.error(self.status, exc_info=True)
            return self.status
        if issue == SG.get_current_number():
            self.status = ST.NO_NEW_GAZETTE
            logger.info(self.status)
            return self.status
        SG.save_next_number(issue)  # Сохраняем текущую последнюю газету.

        return ST.OK

    def get_exact_gazette(
            self,
            driver: Firefox,
            gazette: str) -> Union[str, int]:
        """
        Получаем определенную газету.
        """

        wait = WebDriverWait(driver, 20)
        self.choose_summary(wait)

        # Ищем в списке опций конкретную газету.
        try:
            sleep(2)
            Select(
                wait.until(
                    EC.element_to_be_clickable(
                        ((By.CSS_SELECTOR, PD.FORM_DATA['No']))
                    )
                )
            ).select_by_value(gazette)
            return ST.OK
        except Exception:
            self.status = f'{ST.NO_EXACT_GAZETTE} № {gazette}'
            logger.error(self.status, exc_info=True)
            return self.status

    def read_gazette(self, driver: Firefox) -> Union[str, int]:
        """
        Получаем данные газеты: выбираем фильтры, получаем
        перечень отказов, во всплывшем окне читаем данные
        каждого отказа в отдельности.
        """

        wait = WebDriverWait(driver, 20)

        # Переходим к выбору фильтров: страна, свойства.
        try:
            sleep(2)
            state_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, PD.FORM_DATA['state'])
                )
            )
            Select(state_field).select_by_visible_text(PD.OPTIONS['state'])
        except Exception:
            self.status = ST.NO_COUNTRY
            logger.error(self.status, exc_info=True)
            return self.status

        try:
            sleep(2)
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, PD.FORM_DATA['checkboxes'])
                )
            )
            sleep(2)
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, PD.FORM_DATA['origin']))
            ).click()
        except Exception:
            self.status = ST.ORIGIN_FAIL
            logger.error(self.status, exc_info=True)
            return self.status

        # Отправляем опции фильтра.
        try:
            sleep(2)
            driver.find_element(
                By.CSS_SELECTOR, PD.FORM_DATA['submit']
            ).click()
        except Exception:
            self.status = ST.SUBMIT_FAIL
            logger.error(self.status, exc_info=True)
            return self.status

        try:
            wait.until(  # Ждем появления скрытых элементов.
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, PD.HIDDEN_TAB['tab_header'])
                )
            )
        except Exception:
            self.status = ST.NO_SUBMIT_RESULTS
            logger.error(self.status, exc_info=True)
            return self.status

        original_window = driver.current_window_handle  # Запоминаем окно.

        try:  # Переходим по ссылке во всплывающее окно.
            wait.until(  # Ждем появления скрытых элементов.
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"{PD.HIDDEN_TAB['link']}")
                )
            ).click()
        except Exception:
            self.status = ST.NO_REFUSALS
            logger.error(self.status, exc_info=True)
            return self.status

        try:  # Ждем всплывающее окно.
            wait.until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            self.status = ST.REFUSAL_WINDOW_FAIL
            logger.error(self.status, exc_info=True)
            return self.status

        # Переключаемся на всплывающее окно с данными по каждому отказу.
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Запоминаем количество отказов, чтобы вовремя остановить их
        # перелистывание далее.
        try:
            element_total_amount = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, PD.REFUSALS_DATA['ref_amount'])
                )
            )
            refusal_amount = int(
                element_total_amount.text.replace('/', '').replace(' ', '')
            )
            logger.info(f'Общее количество отказов = {refusal_amount}')
        except Exception:
            self.status = ST.REFUSAL_AMOUNT_FAILURE
            logger.error(self.status, exc_info=True)
            return self.status

        # Изучаем страницы с детализацией отказов
        # и собираем объект LetterData по сведениям,
        # полученным со страниц.
        for i in range(refusal_amount):
            try:
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, PD.REFUSALS_DATA['container'])
                    )
                )

                header_holder = driver.find_element(
                    By.XPATH,
                    f"//*[contains (text(), '{PD.REFUSALS_DATA['holder']}')]"
                )
                holder = header_holder.find_element(
                        By.XPATH, "following-sibling::*[1]"
                ).text
                details = driver.find_element(
                    By.CSS_SELECTOR, PD.REFUSALS_DATA['TM']
                ).text.split(' ')

                data = Letter(
                    reg_num=details[0],
                    holder=holder,
                    type_of_refusal=driver.find_element(
                        By.CSS_SELECTOR, PD.REFUSALS_DATA['type_of_refusal']
                    ).text.split()[0],
                    file_name=''
                )

                # Сведения о 2х атрибутах могут отсутствовать.
                if len(details) > 1:
                    data.trade_mark = ' '.join(details[1:])[1:-1]
                header_represent = driver.find_elements(
                    By.XPATH,
                    f"//*[contains (text(), '{PD.REFUSALS_DATA['represent']}')]"  # noqa
                )
                if header_represent:
                    data.representative = header_represent[0].find_element(
                        By.XPATH, "following-sibling::*[1]"
                    ).text

                # Скачиваем детализацию отказа.
                pdf_file = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, PD.REFUSALS_DATA['file'])
                ))
                link = pdf_file.get_attribute('href')
                reversed_link = link[::-1]
                for letter in reversed_link:
                    if letter == '=':
                        i = reversed_link.index(letter)
                        reversed_link = reversed_link[:i]
                        link_raw = reversed_link[::-1]
                        if link_raw[-1] == '1' and link_raw[-2] == '0':
                            link = link_raw[:-2]
                        break
                data.file_name = link
                pdf_file.click()

                # Включаем в общий список отказов.
                self.articles.append(data)
                sleep(10)  # Ожидание скачивания.

                if i == (refusal_amount - 1):  # Выходим на последней странице.
                    break

                driver.find_element(  # Или переходим к следующей странице.
                    By.CSS_SELECTOR, PD.REFUSALS_DATA['next']
                ).click()

            except Exception:
                self.status = f'{ST.EXACT_REFUSAL_FAIL}{i + 1}'
                logger.error(self.status, exc_info=True)
                return self.status

        return ST.OK

    def check_and_save_emails(self) -> None:
        """
        Заполняем статью недостающими данными об адресах электронных почт
        владельцев товарных знаков и представителей, найденных в базе данных.
        """

        holders = [article.holder for article in self.articles]
        reprs = [article.representative for article in self.articles]

        email_db = {
            'holders_mails': {},
            'reprs_mails': {},
        }

        order = ED.ORDER

        for path, dirs, files in os.walk(DS.TABLES):
            for filename in files:
                table_name = os.path.join(path, filename)
                ws = Extractor(table_name).extract_from_excel()
                for line in ws['data']:
                    holder_mail = line[order['owner_mail']]
                    holder = line[order['holder']]
                    if (len(holder_mail) > 0) and (holder in holders):
                        email_db['holders_mails'][holder] = holder_mail
                    repr_mail = line[order['repr_mail']]
                    representative = line[order['representative']]
                    if (
                        len(representative) > 0) and (
                            len(repr_mail) > 0) and (representative in reprs):
                        email_db['reprs_mails'][representative] = repr_mail

        logger.info(f'Повторяющиеся адреса:{json.dumps(email_db, indent=4)}')

        for article in self.articles:
            if article.holder in email_db['holders_mails'].keys():
                article.owner_mail = email_db['holders_mails'][article.holder]
            if article.representative in email_db['reprs_mails'].keys():
                ar = article.representative
                article.repr_mail = email_db['reprs_mails'][ar]

    def check_one_holder_multiple_tm(self):
        """
        Проверяем количество вхождений владельцев и представителей в список
        статей с тем, чтобы объединить торговые марки одного владельца.
        """

        art = self.articles
        for a in art:
            for reff_a in art:
                if a is not reff_a:
                    if (a.holder == reff_a.holder) and (
                            a.representative == reff_a.representative):
                        a.trade_mark += ', ' + reff_a.trade_mark
                        a.reg_num += ', ' + reff_a.reg_num
                        a.file_name += ', ' + reff_a.file_name
                        art.remove(reff_a)
