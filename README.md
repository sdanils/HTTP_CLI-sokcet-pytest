# Клиент для взаимодействия с сервером в виде CLI программы. 
Проект содержит CLI программу для взаимедействи с сервером, так же включает в себя логирование некоторых событий и тесты. Спецификация API сервера описана в sms-platform.yaml. 

Описание:
При запуске программы, вызывается функция login_verification() для проверки пользователя. Проверка осуществляется с помощью ввода пороля, который хранится файле параметров программы config.toml. Для хранения пароля используется хэш md5. Для примера в программе используется "12345". 
Если хэш пароля совпадает с сохранённым, меню продлогает создать рассылку. В этом случае происходит чтение данных рассылки и проверка на корректность данных. Номер телефона проверяется с помощью регулярного выражения, которое достается из файла конфигурации. Это должно упростить изменение маски ввода.
После проверки данных создается экземпляр http запроса Mailing_request. В нём хранится вся необходимая информация о запросе и функции, нужные для отправки.
Метод Mailing_request.to_bytes конвертирует поля класса в строку http запроса. Которая передаётся по сокету, соеденённому с адресом из конфигурации программы. Тоесть общение с сервером реализовано через модуль socket.
Для хранения ответа сервера реализован класс Mailing_response, содержащий статический метод from_bytes. from_bytes преобразует строку байт в обьект http ответа. 
Данная структура позволяет просто реализовать работу сокета и запросов.
Для отправки сообщения создается класс запроса Mailing_request, принимающий словарь данных. Далее вызвается Mailing_request.make_request. Он совершает отправку строки http запроса по сокету. После отправки строки считывает ответ сервера как поток байт и вызывает с этими данными метод создания ответа. Тем самым возвращет объект Mailing_response.
В программе предусмотрено логирование важных событий. В логфаил записывается информация о входе в программу, действия отправки данных, результаты отправки данных и результаты чтения ответа от сервера. 
Проект также сожержит несколько тестов на pytest. Тесты покрывают функции чтения номера телефона и работы масок ввода. Для этого используются фикстуры и параметры pytest. Есть тесты проверяющие методы создания запроса/ответа по строки байт и обратные им (to_bytes() и from_bytes()). Так же включены тесты для проверки работы программы с сервером. 
Важно что тесты не содержаться в проекте. Для обхода проблемы с импортом проверяемых модулей используется подход временного добавления каталога приложения в sys.path.

Структура проекта:
Папка app содержит приложение.
Файлом конфигурации программы является config.toml. В нём хранятся маршруты сервера [path], пользователи [user], адрес сервера [server] и маска ввода номера телефона в формате строки, она нужна для формирования регулярного выражения. Реализация чтения содержится в get_config.py. 
cli_app.py главный фаил, в нём запускается CLI интерфейс. Фаил verification_function.py содержит функции проверки введёного пароля и сравнение его с хранящимся хэшем md5. number_functions.py содержит функции для чтения и проверки телефона. Creating_mailing.py содержит функцию, создающую рассылку. В нем код чтения данных и создания объекта запроса.
Классы http ответа/запроса описаны в Request/mailing_request, Request/mailing_response. Они наследуются от класс реализованного в Request/func_convert. Данный класс содержит статический метод, с помощью которого из строки байт достаётся информация для создания экземпляров http запроса/ответа.
Для логирования выделана отдельная папка log. В ней хранится фаил с функциями для логирования и фаил для хранения логов logs.txt.

Тесты приложения содержаться в соседней папке test.
В add_peth.py реализована функция добавления пути проекта в sys.path. Фаил mockON_tests содержит тесты, предназначенные для проверки работы с работающим сервером. 
Последние три файла в папке содержат тесты различных процессов приложения, которые не требуют ответа от сервера. 

Инструкция по запуску:
1. Для запуска запустите cli_app.py
2. Введите парол "12345". !!! После ввода пароля терминал будет очищен !!!
3. Следуя пунктам программы создайте рассылку. Программы выведет ответ сервера.
4. 
Инструкция по запуску тестов:
1. Запустите обычные тесты командой pytest из дериктории проекта.
2. Запуските mock сервер из конфигурации sms-platform.yaml.
3. Запустите оставшиеся тесты командой pytest test/mockON_tests.py
Тесты можно запустить без виртуальной среды. Для этого перед pytest добавьте python -m. 
