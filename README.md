# Recipe Manager (Django + PostgreSQL + Docker)

Приложение для управления рецептами с возможностью сохранения данных в файлы (JSON/XML) или в базу данных. Реализован AJAX-поиск, CRUD-операции, проверка на дубликаты и валидация.

## Стек технологий
* Python 3.12 / Django 4.2
* PostgreSQL 16
* Docker / Docker Compose
* Gunicorn (Production WSGI сервер)
* Bootstrap 5

## Запуск проекта (Docker)

### Требования
- Установленный Docker Desktop.
- Установленный Git.

### Инструкция для разработки / production
1. Клонируйте репозиторий:
   ```bash
   git clone <ССЫЛКА_НА_ВАШ_GITHUB>
   cd <папка_проекта>