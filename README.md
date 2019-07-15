# vk-bot-template
Универсальный python бот-заготовка для https://vk.com/. \
Текущая версия: ``[Common Update][1.2]``.
## Возможности бота:
* Это longpoll бот.
* Бот умеет отвечать как в беседах, так и в личных сообщениях для отдельных пользователей.
* В боте реализована поддержка multithreading.
* Добавлена система авторизации по id пользователя с подразделениями на 4 уровня допуска к функциям. 
* Присутствует возможность добавлять команды на русском языке. Например: ```Поищи Апельсин```
* Текст сообщений для бота разнесён на отдельные файлы, что делает их редактирование крайне простым.
* Написано несколько example функций. ```Поиск в DuckDuckGo, отправка сообщения пользователя от имени группы, отправка help сообщения.```
* Добавление функций для бота является очень простой задачей. (см. [Wiki](https://github.com/OPHoperHPO/vk-bot-template/wiki/%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D0%B8#%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E-%D0%BD%D0%BE%D0%B2%D1%8B%D1%85-%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B9))
* Конфигурация бота содержится в одном json файле с подразделениями на разделы.
* При потере интернет соединения, бот терпиливо ждёт восстановления соединения, посылая раз в две минуты GET запрос к vk.com.
## Зависимости:
```
vk_api - Необходимо для функционирования бота
requests - Необходимо для исключения краша бота в случае отсутствия интернет соединения и функции (Поиск в DuckDuckGo)
json - Необходимо для парсинга config.json и text_id.json
```
## Запуск бота:
* ``ВНИМАНИЕ! Бота нужно запускать из PROJECT ROOT(это папка, где он лежит)!``
* Скачиваем репозиторий в какую-нибудь папку. ``` git clone https://github.com/OPHoperHPO/python_vk_bot```
* Идём по пути ```cd config```
* Прописываем в config.json бота
`longpoll токен, id группы. Также необходимо вписать id админа в bot_creator для доступа ко всем функциям бота.`
* Возвращаемся в корневую директорию. ```cd ..```
* Запускаем бота. ```python3 bot.py```

### TODO:
```
1) Написать example модуль.
2) Написать грамотное wiki для бота.
```
