# Сервис анализа патентной активности компаний Москвы

[Сайт документации](https://doster-d.github.io/SfAPAoMC/)

## Требования к запуску проекта

Для меня требуется lfs, скачайте меня - ``` git lfs install```

## Процедура запуска

Запуск Docker - ```docker-compose --project-name="SfAPAoMC" up -d --build```

## Загрузка базы по ЮЛ, ФЛ и ИП.

Распакуйте архив с данным в папку ```data```, все наименования файлов должны быть на английском.

Воспользуйтесь файлом ```sql/scv_migrations``` для получения файлов csv базы.

Воспользуйтесь pgAdmin и загрузите в базу данные при помощи этих csv.

## Лицензия

Исходный код SfAPAoMC находится под лицензией [GNU Affero General Public License v3](http://www.gnu.org/licenses/agpl.html), полный текст которой можно найти в файле LICENSE-AGPL3.

Весь код, который был внесен до коммита `fc4a9990b497f7213672dbc2991e7cbe9ed3f604` (2024/06/16 11:42:39 +0300) находится под лицензией [GNU Affero General Public License v3](http://www.gnu.org/licenses/agpl.html) при единогласном согласие авторов коммитов.