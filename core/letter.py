from typing import Optional, List

from core.sample import Sample
from core.data import ExcelData as ED


class Letter:
    """
    Хранение данных и подстановка в рассылку.

    Holder - владелец товарного знака,
    representative - это представитель владельца,
    reg_num - регистрационный номер на сайте (IRN),
    trade_mark - торговая марка, по поводу которой подано заявление,
    type_of_refusal - тип отказа (полный или частичный),
    file_name - имя пдф-файла, скачанного с сайта,
    repr_mail - адрес электронной почты представителя,
    owner_mail - адрес электронной почты владельца.
    """

    def __init__(self,
                 reg_num: str,
                 holder: str,
                 type_of_refusal: str,
                 file_name: str,
                 trade_mark: str = '[non-text trade mark]',
                 representative: Optional[str] = None,
                 repr_mail: Optional[str] = None,
                 owner_mail: Optional[str] = None,
                 ) -> None:

        self.reg_num = reg_num
        self.holder = holder
        self.type_of_refusal = type_of_refusal
        self.trade_mark = trade_mark
        self.representative = representative
        self.repr_mail = repr_mail
        self.owner_mail = owner_mail
        self.file_name = file_name

    def get_letter_data(self) -> list:
        """
        Получаем наименования атрибутов данного объекта
        для будущего письма.
        """

        return [
            attr for attr in self.__dict__
            if not callable(getattr(self, attr))
            and not attr.startswith('__')
        ]

    def compose_letter_html(self, mult: bool) -> str:
        """
        Составляем письмо с учетом образца.
        """

        if mult:
            text = Sample.HTML_SAMPLE_MULT['text'][:]
        else:
            text = Sample.HTML_SAMPLE['text'][:]
        vars = Sample.VARS

        attrs = self.get_letter_data()

        for attr in attrs:
            if attr in vars:
                value = getattr(self, attr)
                if attr == 'holder':  # Этот блок if зависит от формата данных.
                    value = value.split('\n')
                    last_line = value[-1]
                    if '))' in last_line:
                        count = 0
                        index = 0
                        rev_list = last_line[::-1]
                        for i in rev_list:
                            if count == 2:
                                index += 2
                                cut_list = rev_list[index:]
                                value[-1] = cut_list[::-1]
                                value = '<br>'.join(value)
                                break
                            if i == '(':
                                count += 1
                                index = rev_list.index(i, index+1)
                text = text.replace(attr, value)

        return text


class LettersContainer:
    """
    Управляет множество писем, создаваемых при получении
    данных из направленного челоеком файла.
    """

    def __init__(self, letters=[]) -> None:
        self.letters = letters

    def save_extracted_data_as_letter(self, ws_dict: dict) -> List[Letter]:
        """
        Сохраняем данные из таблицы построчно,
        используя для этого модель хранения данных
        LetterData().
        """

        order = ED.ORDER
        for line in ws_dict['data']:
            if line[order['use']] is False:
                letter_data = Letter(  # Обязательные атрибуты.
                    reg_num=line[order['reg_num']],
                    holder=line[order['holder']],
                    type_of_refusal=line[order['type_of_refusal']],
                    file_name=line[order['file_name']]
                )
                # Необязательные атрибуты.
                if len(line[order['trade_mark']]) > 0:
                    letter_data.trade_mark = line[order['trade_mark']]
                if len(line[order['owner_mail']]) > 0:
                    letter_data.owner_mail = line[order['owner_mail']]
                if len(line[order['repr_mail']]) > 0:
                    letter_data.repr_mail = line[order['repr_mail']]
                if len(line[order['representative']]) > 0:
                    letter_data.representative = line[order['representative']]

                self.letters.append(letter_data)

        return self.letters
