import pandas as pd

from core.data import ExcelData as ED
from core.data import NamesCompiler as NC


class Extractor:
    """
    Вытаскивает обработанные человеком данные из xlsx.
    """

    def __init__(self, file: str) -> None:
        self.file = file

    def extract_from_excel(self) -> dict:
        """
        Переводит из заданного xlsx-файла данные в формат словаря.
        """

        prefix = NC.get_ref_dir_no_name()
        sheet_name = self.file.replace('.xlsx', '').replace(prefix, '')
        ws = pd.read_excel(
            self.file,
            sheet_name=sheet_name,
            engine='openpyxl',
            converters={ED.COLONS['reg_num']: str},
            na_filter=False
        )
        ws_dict = ws.to_dict(orient='split', index=False)

        return ws_dict
