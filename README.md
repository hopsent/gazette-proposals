# gazette-proposals
Скрапим данные с целевого сайта, отдаём человеку в слаке и организуем маркетинговую рассылку с использованием модернизированных человеком данных.
# технологии
- python 3.8.10
- selenium 4.10
- geckodriver
- slack_bolt
- pandas
# описание проекта
Программа:
- забирает данные с целевого сайта и отдаёт человеку;
- создаёт проекты черновиков на основе модифицированных человеком данных целевого сайта.
```
Чтение сайта
```
Получив команду от человека в слаке, программа заходит на сайт с газетами.
Программа помнит номер предыдущей газеты.
Если запомненный номер и номер последней газеты не совпадают, программа продолжает работу - собирает данные.
Иначе проверяет сайт каждые полчаса. Каждые 5 ч. он сообщает, если не нашёл газету; максимум - 30 ч.
Программа может читать конкретную газету, если человек об этом попросит в слаке.
Программа читает каждую страницу, сохраняя сведения из газеты.
Программа отдаёт в слаке человеку xlsx-таблицу и zip-архив с пдф.
```
Создание черновиков писем
```
Программа получает от человека в слаке таблицу и построчно отправляет письма в "Черновики" на электронный адрес.
# развертывание проекта
Прежде всего нужно настроить сервер и пробросить запросы из Slack на определенный порт.
На примере ниже проброс портов сделан на порт 5000, который биндится к порту 5000 контейнера.
```
Разворачиваем образ приложения: качаем образ и запускаем контейнер
```
- sudo docker image pull hopsent/gazette-proposals:latest
- sudo docker run --name gazette-proposals -it -d -p 5000:5000 hopsent/gazette-proposals:latest
```
Готовим программу к работе: переменные окружения и запуск контейнера
```
- sudo docker cp stuff-for-gazette-proposals/.env gazette-proposals:/app/
- sudo docker exec -ti gazette-proposals /bin/sh
```
Готовим программу к работе: создание значения последней газеты
```
- apt install nano
- nano data/old_gazette.txt
Задаём номер газеты, являющийся последним на текущий момент.
```
Запуск программы
```
- python3 __main__.py
# структура проекта
## структура директорий из гитигнора
В корневой директории нужно разместить (mkdir):
- archives/ 
- data/
- logs/
- downloads/
В data/ создаются:
- директория tables/
- файл card.pdf с карточкой компании
- файл old_gazette.txt с номером газеты
В следующих директориях создаются директории по годам (2023, 2024...):
- archives/
- /tables/
- downloads/
## структура файла .env
URL=_адрес целевого сайта в интеренете_
URL_MAIL=_адрес почтового клиента_
EXEC_PATH=_путь до исполняемого файла гецкодрайвера_
DOWNLOAD_DIR='_абсолютный путь до директории проекта_'
LOGIN_MAIL='_логин на электронную почту_'
PASSWORD_MAIL='_пароль от почты_'
SERVER_MAIL='_почтовый сервер АйМап_'
FROM_MAIL='_поле в письме "от кого"_'
CARD_NAME='_название карточки компании в письме_'
BOT_TOKEN='_бот токен для слака_'
APP_TOKEN='_токен приложения для слака_'
SIGNING_SECRET='_подпись приложения для слака_'
SLACK_PORT='_порт для вебхука_'
CHANNEL_ID='_референтный канал_'
# лицензия
# автор
Алексей Кулаков