# Otus_rep7
Analyzing web server log

# Описание работы скрипта.

Регулярное выражение (regex_for_parser) задает шаблон для разбора строк лога. 

Функция analyze_log_file анализирует файл с логом по переданному пути. Лог читается построчно, для каждой строки:
   - Применяется регулярное выражение для извлечения данных.
   - Увеличивается счетчик количества запросов.
   - Извлекается метод, ip-адрес и длительность запроса.
   - Обновляются счетчики для методов и ip.
После обработки всех строк выбираются 3 ip-адреса с наибольшим количеством запросов и 3 самых долгих запроса.

Функция print_and_save_results выводит в терминал результаты анализа лога и сохраняет их в JSON-файл с именем: имя файла лога + _stats.json.

Функция analyze_log_directory(directory) анализирует все файлы с расширением .log в переданной директории.
Для каждого файла выполняется функция analyze_log_file и print_and_save_results.

В основной части скрипта создается парсер аргументов командной строки и определяется, указан ли там путь к папке или файлу.
Если к папке - вызывается analyze_log_directory, если к файлу - вызывается analyze_log_file и print_and_save_results.

Запуск скрипта: python parser_web_logs.py path_to_folder_or_file
