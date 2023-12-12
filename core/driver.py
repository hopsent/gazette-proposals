from os import getenv

from dotenv import load_dotenv
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from core.data import StoredGazette as SG
from core.data import NamesCompiler as NC


load_dotenv()


class DriverHandler:
    """
    Создание драйвера веб-браузера с заданными настройками.
    """

    DOWNLOAD_DIR = getenv('DOWNLOAD_DIR', default='downloads/')
    EXEC_PATH: str = getenv('EXEC_PATH', default='geckodriver')
    LOG_PATH: str = 'logs/geckodriver.log'

    def __init__(self, exact_gazette: str = 'last') -> None:
        self.exact_gazette = exact_gazette

    def create_driver(self) -> Firefox:
        """
        Создаём драйвер Файрфокс на основе гецкодрайвера.
        Headless режим активирован. Установлены свойства, чтобы
        скачивать pdf-файлы.
        """

        profile = FirefoxProfile()

        # Преференции на скачивание .pdf.
        gazette = SG.get_next_or_exact_number(self.exact_gazette)
        profile.set_preference(
            'browser.download.dir',
            f'{self.DOWNLOAD_DIR}{NC.get_relative_downloads_dir(gazette)}'
        )
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference(
            'browser.download.manager.showWhenStarting',
            False
        )
        profile.set_preference(
            'browser.helperApps.neverAsk.saveToDisk',
            'application/pdf'
        )
        profile.set_preference(
            'browser.helperApps.neverAsk.openFile',
            ''
        )
        profile.set_preference('pdfjs.disabled', True)
        profile.set_preference('plugin.scan.Acrobat', "99.0")
        profile.set_preference('plugin.scan.plid.all', False)

        # Устанавливаем видимый профиль.
        profile.set_preference('dom.webdriver.enabled', False)
        profile.set_preference(
            'general.useragent.override',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0)'
            'Gecko/20100101 Firefox/117.0'
        )

        options = Options()
        options.headless = True  # Установи False для визуального дебага.
        options.profile = profile

        service = Service(
            log_path=self.LOG_PATH,
            executable_path=self.EXEC_PATH,
            service_args=['--log', 'info']
        )

        return Firefox(service=service, options=options)
