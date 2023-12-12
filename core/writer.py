from imaplib import IMAP4_SSL, Time2Internaldate
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

from core.letter import Letter
from core.data import DirectoryStorage as DS


class Writer:
    """
    Пишем письма в почтовом клиенте с использованием
    соскрапленных данных.
    """

    def __init__(self,
                 login: str,
                 password: str,
                 server: str,
                 addressee: str,
                 card_name: str) -> None:
        self.login = login
        self.password = password
        self.server = server
        self.addressee = addressee
        self.card_name = card_name

    def send_letter(self, article: Letter, conn: IMAP4_SSL) -> None:

        new_letter = MIMEMultipart('mixed')

        # Работа с почтовыми адресами. Они не всегда могут быть,
        # их количество может разниться.
        addresses = []
        if article.owner_mail is not None:
            owner_mails = article.owner_mail.split('\n')
            for owner_mail in owner_mails:
                addresses.append(owner_mail)
        if article.repr_mail is not None:
            repr_mails = article.repr_mail.split('\n')
            for repr_mail in repr_mails:
                addresses.append(repr_mail)
        if addresses:
            new_letter['To'] = ', '.join(addresses)
        if not addresses:
            return None
        new_letter['From'] = self.addressee
        new_letter['Subject'] = f'Provisional refusal IRN {article.reg_num}'

        # Создаём флаг для выбора формы текста в зависимости от
        # количества ТМ в составе письма.
        mult = False
        if ', ' in article.reg_num:
            mult = True

        letter_html = MIMEText(article.compose_letter_html(mult), 'html')
        new_letter.attach(letter_html)

        with open(DS.CARD, 'rb') as f:  # Прицепляем карточку компании.
            attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=self.card_name
        )
        new_letter.attach(attachment)

        conn.append('Drafts',
                    '',
                    Time2Internaldate(time.time()),
                    new_letter.as_bytes()
                    )

    def login_to(self) -> IMAP4_SSL:

        conn = IMAP4_SSL(self.server)
        conn.login(self.login, self.password)
        conn.select('Drafts')

        return conn

    def logout_from(self, conn: IMAP4_SSL) -> None:

        conn.close()
        conn.logout()
