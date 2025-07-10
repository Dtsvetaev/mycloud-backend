# MyCloud

**MyCloud** — полнофункциональное облачное хранилище на Django + React с загрузкой, скачиванием и публичными ссылками. Подходит для локальной работы и продакшн-развёртывания.

## 🔧 Стек технологий

- **Backend**: Django, Django REST Framework, SimpleJWT, PostgreSQL
- **Frontend**: React + Vite
- **Аутентификация**: JWT (access/refresh)
- **Хранилище**: локальное MEDIA
- **Продакшн**: NGINX + gunicorn, деплой на REG.RU/VPS

---

## ⚙️ Возможности

- 👤 Регистрация и авторизация пользователей
- 🔐 Аутентификация через JWT
- 📁 Загрузка файлов (с комментариями)
- 🖼 Просмотр файлов
- 📦 Скачивание и удаление
- ✏️ Редактирование имени и комментария
- 🔗 Публичная ссылка без авторизации
- 👮‍♂️ Администрирование пользователей (удаление, назначение admin)
- 📊 Тесты backend и frontend

---

## 🚀 Установка локально

### 🔙 Backend

```bash
cd mycloud-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # или создайте вручную
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

📄 Пример `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=mycloud
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
CORS_ORIGIN_ALLOW_ALL=True
```

### 🔝 Frontend

```bash
cd mycloud-frontend
npm install
npm run dev
```

---

## 🧪 Тестирование

### Backend

```bash
cd mycloud-backend
venv\Scripts\activate
python manage.py test
```

### Frontend

```bash
cd mycloud-frontend
npm test
```

---

## 🌐 Развёртывание на сервере (REG.RU / VPS)

### 1. 📦 Сборка frontend

```bash
cd mycloud-frontend
npm run build
```

➡️ Создастся папка `dist/`

### 2. 📁 Django backend

```bash
cd mycloud-backend
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3. 🧯 Gunicorn

```bash
gunicorn mycloud_backend.wsgi:application --bind 127.0.0.1:8000
```

### 4. ⚙️ Настройка NGINX

```
server {
    server_name yourdomain.ru;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        include proxy_params;
    }

    location / {
        root /path/to/mycloud-frontend/dist;
        index index.html;
        try_files $uri /index.html;
    }

    location /media/ {
        alias /path/to/mycloud-backend/media/;
    }

    location /static/ {
        alias /path/to/mycloud-backend/static/;
    }
}
```

---

## 📁 Структура проекта

```
mycloud-backend/
├── storage/
├── mycloud_backend/
├── .env.example
├── manage.py

mycloud-frontend/
├── src/components/
├── src/__tests__/
├── public/
└── dist/
```

---

## ✅ Статус

Проект успешно протестирован, покрыт тестами, подготовлен к продакшн. Все замечания устранены.

