import logging
from logging.handlers import RotatingFileHandler
from os import getenv
import time
from typing import Optional, Tuple, Union
from shutil import make_archive

from dotenv import load_dotenv

from core.letter import LettersContainer
from core.driver import DriverHandler
from core.reader import Reader
from core.writer import Writer
from core.saver import Saver
from core.extractor import Extractor
from core.data import PagesData, StatusData, StoredGazette, NamesCompiler


load_dotenv()

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


class Commander:
    """
    Интерфейс, объединяющий следующих функций:
    - создание драйвера Файрфокс,
    - скрэппинг данных с целевого сайта,
    - сохранение данных в xlsx-таблице,
    - извлечение дополненных данных из таблицы и
    - создание черновиков электронных писем.
    Имеет разделение на скраппер и автор черновиков.
    """

    URL = getenv('URL', default=PagesData.DEFAULT_URL)
    login = getenv('LOGIN_MAIL', default='')
    password = getenv('PASSWORD_MAIL', default='')
    server = getenv('SERVER_MAIL', default='')
    addressee = getenv('FROM_MAIL', default='')
    card_name = getenv('CARD_NAME', default='')

    def __init__(self,
                 exact_gazette: str = 'last',
                 download_directory: Optional[str] = None,
                 ) -> None:
        self.exact_gazette = exact_gazette
        self.download_directory = download_directory

    def scrape_data(self) -> Union[str, int]:
        """
        Сводит воедино эмулятор веббраузера файрфокс,
        программу-скраппер данных с целевого сайта
        и программу, сохраняющую данные в эксель-файле.
        Если находим последнюю газету - "читаем" её, сохраняя данные.
        """

        driver_handler = DriverHandler()
        driver = driver_handler.create_driver()  # Создаем дайвер браузера.
        driver.get(self.URL)  # Заходим на целевой сайт.

        reader = Reader()

        status = reader.get_gazette(driver)  # "Извлекаем" последнюю газету.
        if status != StatusData.OK:
            driver.quit()
            return reader.status

        status = reader.read_gazette(driver)  # "Читаем" газету.
        if status != StatusData.OK:
            driver.quit()
            return reader.status

        p = driver.options.profile
        self.download_directory = p.default_preferences['browser.download.dir']
        driver.quit()  # Выходим из браузера.
        logger.info('Браузер закрыт')

        reader.check_and_save_emails()  # Ищем совпадения по email.
        reader.check_one_holder_multiple_tm()  # Ищем повторных владельцев ТМ.
        Saver().save_to_excel(reader.articles)  # Сохраняем данные.

        return StatusData.OK

    def scrape_data_exact_gazette(self) -> Union[str, int]:
        """
        То же, что и self.scrape_data(), но в отношении
        конкретной газеты, поступающей из сообщения пользователя в Слаке.
        """

        driver_handler = DriverHandler()
        driver_handler.exact_gazette = self.exact_gazette
        driver = driver_handler.create_driver()  # Создаем дайвер браузера.
        driver.get(self.URL)  # Заходим на целевой сайт.

        reader = Reader()

        # Код для поиска конкретной газеты.
        status = reader.get_exact_gazette(driver, self.exact_gazette)
        if status != StatusData.OK:  # Проверка правильности извлечения.
            driver.quit()
            return reader.status

        status = reader.read_gazette(driver)  # "Читаем" газету.
        if status != StatusData.OK:
            driver.quit()
            return reader.status

        p = driver.options.profile
        self.download_directory = p.default_preferences['browser.download.dir']
        driver.quit()  # Выходим из браузера.
        logger.info('Браузер закрыт')

        reader.check_and_save_emails()  # Ищем и сохраняем совпадения по email.
        reader.check_one_holder_multiple_tm()  # Ищем повторных владельцев ТМ.
        # Сохраняем данные по конкретной газете.
        Saver(exact_gazette=self.exact_gazette).save_to_excel(reader.articles)

        return StatusData.OK

    def create_draft_letters(self, file):
        """
        Создаём черновики писем на почтовом клиенте через IMAP.
        """

        try:
            # Берём данные.
            ws = Extractor(file=file).extract_from_excel()
            articles = LettersContainer().save_extracted_data_as_letter(ws)
        except Exception as er:
            logger.error(er, exc_info=True)
            return StatusData.NOT_OK

        try:
            writer = Writer(
                login=self.login,
                password=self.password,
                server=self.server,
                addressee=self.addressee,
                card_name=self.card_name
            )
        except Exception as er:
            logger.error(er, exc_info=True)
            return StatusData.NOT_OK

        try:
            conn = writer.login_to()  # Создаем подключение.
            for article in articles:
                # Сохраняем одно письмо в черновиках.
                writer.send_letter(article, conn)
                time.sleep(1)
            # Прерываем подключение.
            writer.logout_from(conn)
        except Exception as er:
            logger.error(er, exc_info=True)
            return StatusData.NOT_OK

        return StatusData.OK

    def make_archive(self) -> Union[Tuple[str, str], int]:
        """
        Создаём архив из скачанных пдф-сканов.
        """

        try:
            number = StoredGazette.get_current_or_exact_number(
                self.exact_gazette
            )
            archive = make_archive(  # Делаем архив с файлами.
                base_name=NamesCompiler.get_archive_dir(number)[:-4],
                format='zip',
                root_dir=self.download_directory
            )
            return number, archive
        except Exception as er:
            logger.error(er, exc_info=True)
            return StatusData.NOT_OK
