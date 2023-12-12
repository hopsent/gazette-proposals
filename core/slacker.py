from requests import get
import re
from time import sleep

from slack_sdk.web.client import WebClient

from core.commander import Commander
from core.data import StatusData as ST
from core.data import NamesCompiler as NC
from core.data import StoredGazette as SG


class Slacker:
    """
    При получении меншена @App в Слаке триггерятся процессы.
    Предназначен для соединения работы программы-скраппера
    и программы-писателя с интерфейсом пользователя в Слаке.
    Атрибут mode предназначен для диспетчеризации команд
    в зависимости от текста сообщения с меншеном.
    Используйте в коде mode 'w' - для написания черновиков писем
    или mode 'r' - для скрэппинга данных с целевого сайта.
    """

    EMOJI_START = 'eyes-3'
    EMOJI_DONE = 'heart'

    def __init__(self,
                 action: str,
                 user: str,
                 client: WebClient,
                 channel: str,
                 msg: str,
                 exact_gazette: str = 'last'
                 ) -> None:

        self.action = action
        self.user = user
        self.client = client
        self.channel = channel
        self.msg = msg
        self.exact_gazette = exact_gazette

    def set_reaction_in_progress(self) -> None:
        """
        Типовая реакция "принято в работу".
        """

        self.client.reactions_add(
            channel=self.channel,
            name=self.EMOJI_START,
            timestamp=self.msg
        )

    def set_reaction_complete(self) -> None:
        """
        Типовая реакция "работа завершена".
        """

        self.client.reactions_remove(
            channel=self.channel,
            name=self.EMOJI_START,
            timestamp=self.msg
        )
        self.client.reactions_add(
            channel=self.channel,
            name=self.EMOJI_DONE,
            timestamp=self.msg
        )

    def send_msg(self, chunk) -> None:
        """
        Типовое сообщение для треда.
        """

        self.client.chat_postMessage(
            channel=self.channel,
            text=f'<@{self.user}>\n{chunk}',
            thread_ts=self.msg
        )

    def send_scrapped_data(self, commander: Commander) -> None:
        """
        Отправляем скрапленные данные в слак.
        """

        result = commander.make_archive()
        if result == ST.NOT_OK:
            return self.send_msg(ST.C_ZIP_PROBLEM)
        number, archive = result[0], result[1]
        text = '!'
        if (
            commander.download_directory != SG.get_current_number()
            and self.exact_gazette == 'last'
        ):
            text += ST.C_UNUSUAL_GAZETTE

        self.client.files_upload_v2(  # Направляем в тред файлы.
            channel=self.channel,
            initial_comment=f'<@{self.user}>\n'
                            f'{ST.C_REFUSALS_DOWNLOADED}{number}{text}',
            file_uploads=[
                {
                    "filename": NC.get_archive_filename(number),
                    "file": f'{archive}',
                    "title": 'Архив сканов',
                },
                {
                    "filename": NC.get_refusals_filename(number),
                    "file": NC.get_refusals_dir(number),
                    "title": 'Табличка для редактирования',
                },
            ],
            thread_ts=self.msg
        )

    def human_interaction(self, event: dict, token: str) -> None:
        """
        Активируем различные методы объекта Commander()
        в зависимости от полученного в треде сообщения.
        """

        if self.action == ST.WRITE_LETTERS:  # Пишем письма.

            self.set_reaction_in_progress()

            # Забираем файл из хранилища слака.
            url = event['files'][0]['url_private_download']
            response = get(  # Загружаем.
                url,
                headers={'Authorization': 'Bearer %s' % token}
            )
            headers = response.headers['content-disposition']
            att_name = re.findall("filename=(.*?);", headers)[0]  # Имя файла.
            fname = f'{NC.get_ref_dir_no_name()}{att_name}'.replace('\"', '')
            with open(fname, mode='wb+') as f:
                f.write(response.content)  # Записываем файл.

            # Создаем черновики.
            status = Commander().create_draft_letters(file=fname)

            if status == ST.NOT_OK:
                self.send_msg(ST.C_UNKNOWN_PROBLEM)
            if status == ST.OK:  # Сообщаем: черновики созданы.
                self.send_msg(ST.C_DRAFTS_READY)

            self.set_reaction_complete()

        # Если поступает команда получить данные с сайта.
        if self.action == ST.READ_DATA:

            self.set_reaction_in_progress()

            # Забираем данные с целевого сайта.
            commander = Commander()
            status, count = 1, 0
            while status != ST.OK:  # Пока не будет обнаружена новая газета.
                status = commander.scrape_data()

                if status == ST.OK:
                    self.send_scrapped_data(commander)
                    break

                elif status == 1:
                    self.send_msg(ST.C_UNKNOWN_PROBLEM)
                    break

                elif type(status) == str:

                    if ST.NO_NEW_GAZETTE in status:
                        if count == 0:
                            self.send_msg(ST.C_NO_NEW_GAZETTE)

                        if count % 10 == 0 and count != 0:
                            chunk = ST.C_LONG_CHECK + f' {int(count / 2)} ч.'
                            self.send_msg(chunk=chunk)
                        count += 1
                        if count == 60:  # Предельное количество проверок.
                            self.send_msg(ST.C_STOP_CHECKING)
                            break
                        sleep(1800)
                    else:
                        self.send_msg(ST.C_EXACT_PROBLEM + f' {status}.')
                        break

                else:
                    self.send_msg(ST.C_EXACT_PROBLEM + f' {status}.')
                    break

            self.set_reaction_complete()

        if self.action == ST.READ_EXACT_DATA:

            self.set_reaction_in_progress()

            # Забираем данные с целевого сайта.
            commander = Commander()
            commander.exact_gazette = self.exact_gazette
            status = commander.scrape_data_exact_gazette()

            if status == ST.OK:
                self.send_scrapped_data(commander)
            elif type(status) == str:
                if ST.NO_EXACT_GAZETTE in status:
                    chunk = f'Газета № {self.exact_gazette}' + ST.C_NO_EXACT_G
                    self.send_msg(chunk)
                else:
                    self.send_msg(ST.C_EXACT_PROBLEM + f' {status}.')
            else:
                self.send_msg(ST.C_UNKNOWN_PROBLEM)

            self.set_reaction_complete()

        if self.action == ST.NO_ACTION:
            self.set_reaction_in_progress()
            self.send_msg(ST.WRONG_MESSAGE)
            sleep(1)
            self.set_reaction_complete()
