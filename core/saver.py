from typing import List

import pandas as pd

from core.letter import Letter
from core.data import ExcelData as ED
from core.data import NamesCompiler as NC
from core.data import StoredGazette as SG


class Saver:
    """
    Сохраняет спарсенные данные в xlsx.
    """

    def __init__(self, exact_gazette: str = 'last') -> None:
        self.exact_gazette = exact_gazette

    def save_to_excel(self, articles: List[Letter]):

        data = {
            k: [] for k in ED.COLONS.values()
        }
        # Сведения о каждой сохраненной странице сохраняем
        # в словаре, ключи которого - это наименования столбцов.
        for article in articles:
            attrs = article.get_letter_data()
            for attr in attrs:
                if attr in ED.COLONS.keys():
                    value = getattr(article, attr)
                    data[ED.COLONS[f'{attr}']].append(value)
        for k in data.keys():
            if len(data[k]) != len(articles):
                for _ in range(len(articles)):
                    data[k].append(None)

        df = pd.DataFrame(data)  # Трансформируем словарь в Датафрэйм.

        gazette_number = SG.get_current_or_exact_number(self.exact_gazette)
        sheet_name = NC.get_basename(gazette_number)

        with pd.ExcelWriter(  # Сохраняем объект Датафрэйм в таблицу.
            NC.get_refusals_dir(gazette_number),  # Имя файла.
            engine='xlsxwriter'  # Движок для метода .автофит().
        ) as dw:
            df.to_excel(dw, sheet_name=sheet_name, index=False)
            dw.sheets[sheet_name].autofit()
