# vk-bot-template
Универсальный python бот-заготовка для https://vk.com/. 
## Возможности бота:
* Это longpoll бот.
* Бот умеет отвечать как в беседах, так и в личных сообщениях для отдельных пользователей.
* В боте реализована поддержка multithreading.
* Добавлена система авторизации по id пользователя с подразделениями на 4 уровня допуска к функциям. 
* Присутствует возможность добавлять команды на русском языке. Например: ```Поищи Апельсин```
* Текст сообщений для бота разнесён на отдельные файлы, что делает их редактирование крайне простым.
* Написано несколько example функций. ```Поиск в DuckDuckGo, отправка сообщения пользователя от имени группы, отправка help сообщения.```
* Добавление функций для бота является очень простой задачей. (см. Wiki **в процессе создания!**)
* Конфигурация бота содержится в одном json файле с подразделениями на разделы.
## Зависимости:
```
vk_api - Необходимо для функционирования бота
requests - Необходимо для example функции (Поиск в DuckDuckGo)
json - Необходимо для парсинга config.json и text_id.json
```
## Запуск бота:
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
