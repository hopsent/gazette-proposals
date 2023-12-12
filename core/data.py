from datetime import datetime as dt


class Year:
    """
    Получаем значение текущего года.
    """

    @classmethod
    def current_year(cls) -> str:
        """
        Значение текущего года.
        """
        return f'{dt.now().year}'


class DirectoryStorage:
    """
    Содержит директории хранения файлов проекта.
    """

    DATA = './data/'
    ARCHIVES = './archives/'
    OLD_GAZETTE = f'{DATA}old_gazette.txt'
    CARD = f'{DATA}card.pdf'
    TABLES = f'{DATA}tables/'

    REFUSALS_CHUNK = 'refusals_from_gazette_'


class StoredGazette:

    @classmethod
    def get_current_number(cls) -> str:
        """
        Получаем номер газеты, ранее сохраненный в специальном файле.
        """
        with open(DirectoryStorage.OLD_GAZETTE, 'r') as f:
            gazette_number = f.readlines()[0]
        return gazette_number

    @classmethod
    def get_current_or_exact_number(cls, gazette: str) -> str:
        """
        В программе использован следующий алгоритм:

        (1) если значение атрибута "газета" == 'last',
        то считается, что программа выполняется в отношении
        последней газеты;
        (2) если значение атрибута "газета" становится
        другим, то поиск выполняется в отношении конкретной газеты.

        Такой подход реализован на разных объектах.
        """
        if gazette == 'last':
            return cls.get_current_number()
        return gazette

    @classmethod
    def get_next_or_exact_number(cls, gazette) -> str:
        """
        Исключительно для целей создания директории загрузки
        объектом WebDriver() в модуле driver.py.
        """
        if gazette == 'last':
            return f'{int(cls.get_current_number()) + 1}'
        return gazette

    @classmethod
    def save_next_number(cls, issue) -> None:
        """
        Сохраняем номер газеты, который сейчас будет исследован.
        """
        with open(DirectoryStorage.OLD_GAZETTE, 'w') as f:
            f.write(f'{issue}')


class NamesCompiler:
    """
    Отдает названия файлов/директории для размещения и доступа к отказам
    и архивам скан-копий документов.
    """

    @classmethod
    def get_basename(cls, gazette: str) -> str:
        """
        Базовое имя для архивов и таблиц: нет формата, нет директории.
        """
        return f'{DirectoryStorage.REFUSALS_CHUNK}{gazette}'

    @classmethod
    def get_refusals_filename(cls, gazette: str) -> str:
        """
        Принимая номер газеты, возращаем имя Excel-таблицы
        с информацией с целевого сайта.
        """
        return f'{cls.get_basename(gazette)}.xlsx'

    @classmethod
    def get_archive_filename(cls, gazette: str) -> str:
        """
        Принимая номер газеты, возвращаем имя архива с отказами,
        скачанными из неё.
        """
        return f'{cls.get_basename(gazette)}.zip'

    @classmethod
    def get_archive_dir(cls, gazette: str) -> str:
        """
        Относительный путь до архива (директория и имя).
        """
        archives = f'{DirectoryStorage.ARCHIVES}{Year.current_year()}/'
        return f'{archives}{cls.get_archive_filename(gazette)}'

    @classmethod
    def get_ref_dir_no_name(cls) -> str:
        """
        Относительный путь для отказов (директория и имя).
        """
        tables = DirectoryStorage.TABLES
        year = Year.current_year()
        return f'{tables}{year}/'

    @classmethod
    def get_refusals_dir(cls, gazette: str) -> str:
        """
        Относительный путь для отказов (директория и имя).
        """
        return f'{cls.get_ref_dir_no_name()}{cls.get_refusals_filename(gazette)}'  # noqa

    @classmethod
    def get_relative_downloads_dir(cls, gazette: str) -> str:
        """
        Базовый относительный путь для загруженных файлов (без имени файла).
        """
        return f'downloads/{Year.current_year()}/downloads_{gazette}'


class PagesData:
    """
    Определяет константы, используемые программой.
    В частности, определяет дефолтное значение URL,
    CSS полей, кнопок, которые используются драйвером на сайте.
    """

    DEFAULT_URL: str = 'https://www.google.com/'

    FORM_DATA: dict = {  # Все - css-селекторы.
        'browse': '#tabBrowse',
        'year': '#selYear',  # Не используется.
        'No': '#selIssue',
        'summary': '#selChapter',
        'state': '#selCountry',
        'checkboxes': 'div.browseContext:nth-child(3)',
        'origin': '#optOrigin',
        'submit': '#btnQuery',
    }

    OPTIONS: dict = {  # Внутренние HTML.
        'summary': 'Notifications of provisional refusals',
        'state': 'Russian Federation (RU)',
    }

    HIDDEN_TAB: dict = {  # Все css, кроме одного.
        'tab_header': '#divChapterHeader',
        'tab': '#tabHits',
        'first_res': 'tr.odd:nth-child(2) > td:nth-child(2) > a:nth-child(1)',  # noqa
        'empty_tab': 'No match',  # html.
        'link': '[href="details.jsp?seq=1"]',
    }

    REFUSALS_DATA: dict = {  # Все - css.
        'ref_amount': 'ul.no-print > li:nth-child(7) > span:nth-child(1)',
        'container': '#detailsContainer',
        'file': '.regNum > a:nth-child(1)',
        'type_of_refusal': '.label',
        'TM': '.regNum',
        'next': 'li.next:nth-child(8)',
        'holder': 'Name and address of the holder of the registration',
        'represent': 'Name and address of the representative',
    }

    #  В настоящий момент не применяется.
    MAIL_DATA: dict = {  # Все - css.
        'login_button': '#header-login-button',
        'via_mail': '.Button2_checked',
        'via_mail_unpressed': '.Button2_view_clear',
        'login': '#passp-field-login',
        'password': '#passp-field-passwd',
        'submit': r'#passp\:sign-in',
        'compose': 'a.Button2_view_action',
        'text': '.cke_wysiwyg_div',  # aft sign
        # 'text': '.cke_htmlplaceholder',  # b4 sign
        'close_letter': '.HeaderButtons__root--WwDCZ > button:nth-child(3)',
    }


class StatusData:
    """
    Содержит типовые статусы, используемые в программе.
    """

    # Статусы эмуляции поведения человека на сайте.
    # Используются в reader.py
    NO_SECTION = 'Не нашел поле выбора разделов газеты'
    NO_OPTION = 'Не смог выбрать последнюю газету в списке'
    NO_NEW_GAZETTE = 'Возможно, новая газета не опубликована'
    NO_EXACT_GAZETTE = 'Не нашел конкретную газету'
    NO_COUNTRY = 'Не нашел поле выбора страны'
    ORIGIN_FAIL = 'Не смог снять галочку с origin'
    SUBMIT_FAIL = 'Не смог нажать на кнопку submit'
    NO_SUBMIT_RESULTS = 'Не получил результаты кнопки submit'
    NO_REFUSALS = 'Список отказов пуст'
    REFUSAL_AMOUNT_FAILURE = 'Не могу определить количество отказов'
    FIRST_REFUSAL_FAIL = 'Не удалось кликнуть на 1-й отказ'
    REFUSAL_WINDOW_FAIL = 'Окно со всеми отказами не открылось.'
    EXACT_REFUSAL_FAIL = 'Не подгрузились данные отказа № '

    # Статусы выполнения различных частей программ.
    OK = 200
    NOT_OK = 400

    # Куски текстов для объекта Slacker().
    C_UNKNOWN_PROBLEM = """
    Случилась неопределенная проблема. Требуется прочитать лог.
    Возможно требуется перезагрузка.
    """
    C_EXACT_PROBLEM = 'Случилась ошибка. Попробуй снова! Описание проблемы:'
    C_DRAFTS_READY = 'Черновики писем отправлены в почту!'
    C_NO_NEW_GAZETTE = 'Новая газета не обнаружена.\nБуду проверять каждые 30 минут и каждые 5 часов сообщать статус проверки.'  # noqa
    C_NO_EXACT_G = ' не обнаружена. Правильно ли был введён номер?'
    C_LONG_CHECK = 'Новая газета не появилась. Проверка продолжается:'
    C_STOP_CHECKING = 'Прекращаю проверку. Можно начать скрипт заново.'
    C_REFUSALS_DOWNLOADED = 'Скачаны отказы из газеты № '
    C_UNUSUAL_GAZETTE = '\nОбрати внимание на необычный формат номера газеты на этой неделе.'  # noqa
    C_ZIP_PROBLEM = 'Не смог создать архив с файлами.'
    WRONG_MESSAGE = 'Недопустимый формат команды.\nИнформацию об использовании бота можешь найти в разделе "About".'  # noqa

    # Статусы запросов пользователей через слак.
    WRITE_LETTERS = 'w'
    READ_DATA = 'r'
    READ_EXACT_DATA = '№'
    NO_ACTION = ''

    # Текст запросов пользователей в слаке.
    READ_REQUEST = 'принеси, пожалуйста, газету'
    WRITE_REQUEST = 'подготовь, пожалуйста, письма'


class ExcelData:
    """
    Храним данные о столбцах базы данных в словаре
    COLONS: наименование и отнесение к атрибуту объекта
    LetterData. Также в словаре ORDER храним последовательность
    отображения атрибутов LetterData в столбцах таблицы.
    """

    COLONS: dict = {
        'holder': 'Owner',
        'owner_mail': 'Owner\'s e-mail',
        'representative': 'Representative',
        'repr_mail': 'Representative\'s e-mail',
        'reg_num': 'Reg. Number',
        'trade_mark': 'Trade Mark',
        'type_of_refusal': 'Type of refusal',
        'use': 'Set mark for kick out',
        'ru_office': 'Representative has Office in Russia',
        'file_name': 'PDF name in PDF-folder',
    }

    ORDER: dict = {
        'holder': 0,
        'owner_mail': 1,
        'representative': 2,
        'repr_mail': 3,
        'reg_num': 4,
        'trade_mark': 5,
        'type_of_refusal': 6,
        'use': 7,
        'ru_office': 8,
        'file_name': 9,
    }
