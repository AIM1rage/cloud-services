# cloud-services

## Инструкция по запуску скриптов

**Важно: перед запуском скриптов убедитесь, что находитесь в директории проекта (возможно, потребуется запускать скрипты от имени администратора).**

Для запуска скриптов необходимо выполнить следующие шаги:

1. Запустить скрипт `scripts/db.ps1` с параметром `name`, указав название базы данных:
   ```
   ./scripts/db.ps1 -name <название_базы_данных>
   ```

2. Затем запустить скрипт `scripts/table.ps1` для создания бессерверной функции `create-messages` создания и заполнения таблицы с указанием IAM токена в диалоговом окне:
   ```
   ./scripts/table.ps1
   ```
   
3. После этого запустить скрипт `scripts/api.ps1` для создания бессерверной функции `get-message` с указанием IAM токена в диалоговом окне:
   ```
   ./scripts/api.ps1
   ```

4. Изменить значение константы в `script.js`, заменив `getMessagesUrl` на URL для вызова функции `get-messages` (достаете из вывода последнего скрипта).
   
5. Наконец, запустить последний скрипт `scripts/bucket.ps1` с параметром `name`, указав название бакета для статики:
   ```
   ./scripts/bucket.ps1 -name <название_бакета>
   ```
После выполнения всех шагов, вы можете посетить [рабочий сайт](https://nekohtur.tech) для проверки функционала.