# Руководство по развертыванию TSPRTG Tag Manager

## Быстрый старт - 3 варианта развертывания

### Вариант 1: Docker (Рекомендуется - Самый простой) 🐳

Это самый простой способ развернуть систему на сервере.

#### Шаг 1: Подготовка сервера

```bash
# Установите Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose

# Клонируйте репозиторий
cd /opt
sudo git clone https://github.com/Anastasiia804/GTM_RT.git tsprtg
cd tsprtg
```

#### Шаг 2: Настройка окружения

```bash
# Создайте файл конфигурации
cd backend
sudo cp .env.example .env

# Откройте и отредактируйте .env
sudo nano .env
```

Установите безопасный токен администратора:
```bash
# Сгенерируйте безопасный токен
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Скопируйте результат в .env как ADMIN_TOKEN
```

#### Шаг 3: Запуск

```bash
cd /opt/tsprtg

# Запустите все сервисы
sudo docker-compose up -d

# Проверьте статус
sudo docker-compose ps
sudo docker-compose logs -f
```

**Готово!** Система запущена:
- Backend API: `http://your-server:8000`
- Frontend: `http://your-server:3000`
- API Docs: `http://your-server:8000/docs`

---

### Вариант 2: Установка на сервер (Linux) 🖥️

Для Ubuntu 20.04+ или Debian.

#### Шаг 1: Установка зависимостей

```bash
# Обновите систему
sudo apt-get update
sudo apt-get upgrade -y

# Установите Python 3.11
sudo apt-get install python3.11 python3.11-venv python3-pip -y

# Установите Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install nodejs -y

# Установите Nginx
sudo apt-get install nginx -y
```

#### Шаг 2: Клонирование репозитория

```bash
cd /opt
sudo git clone https://github.com/Anastasiia804/GTM_RT.git tsprtg
cd tsprtg
sudo chown -R $USER:$USER /opt/tsprtg
```

#### Шаг 3: Настройка Backend

```bash
cd /opt/tsprtg/backend

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Настройте конфигурацию
cp .env.example .env
nano .env  # Отредактируйте настройки

# Сгенерируйте безопасный токен
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Добавьте его в .env как ADMIN_TOKEN
```

#### Шаг 4: Настройка Frontend

```bash
cd /opt/tsprtg/frontend

# Установите зависимости
npm install

# Соберите для продакшена
npm run build
```

#### Шаг 5: Настройка Systemd сервиса

```bash
# Скопируйте файл сервиса
sudo cp /opt/tsprtg/deployment/tsprtg-backend.service /etc/systemd/system/

# Отредактируйте пути (если нужно)
sudo nano /etc/systemd/system/tsprtg-backend.service

# Запустите сервис
sudo systemctl daemon-reload
sudo systemctl enable tsprtg-backend
sudo systemctl start tsprtg-backend

# Проверьте статус
sudo systemctl status tsprtg-backend
```

#### Шаг 6: Настройка Nginx

```bash
# Создайте конфигурацию Nginx
sudo nano /etc/nginx/sites-available/tsprtg.com
```

Вставьте следующую конфигурацию (замените `tsprtg.com` на ваш домен):

```nginx
server {
    listen 80;
    server_name tsprtg.com www.tsprtg.com;

    # Frontend (собранные файлы)
    location / {
        root /opt/tsprtg/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Публичный загрузчик контейнеров
    location /c/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # CORS заголовки
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS' always;
        
        # Кэширование на 5 минут
        proxy_cache_valid 200 5m;
    }
}
```

```bash
# Активируйте сайт
sudo ln -s /etc/nginx/sites-available/tsprtg.com /etc/nginx/sites-enabled/

# Проверьте конфигурацию
sudo nginx -t

# Перезапустите Nginx
sudo systemctl restart nginx
```

#### Шаг 7: Настройка SSL (Let's Encrypt)

```bash
# Установите Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Получите SSL сертификат
sudo certbot --nginx -d tsprtg.com -d www.tsprtg.com

# Автообновление сертификата настраивается автоматически
```

#### Шаг 8: Настройка файрвола

```bash
# Разрешите HTTP и HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

**Готово!** Откройте `https://tsprtg.com` в браузере.

---

### Вариант 3: Локальная разработка 💻

Для тестирования на локальном компьютере.

#### Быстрый запуск

```bash
# Клонируйте репозиторий
git clone https://github.com/Anastasiia804/GTM_RT.git
cd GTM_RT

# Запустите скрипт быстрого старта
./start.sh
```

Или вручную:

```bash
# Terminal 1 - Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

Откройте:
- Frontend: `http://localhost:3000`
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

---

## Использование системы

### 1. Доступ к админ-панели

После развертывания откройте в браузере:
- Docker: `http://your-server:3000`
- Production: `https://tsprtg.com`

### 2. Создание рекламодателя

1. Перейдите в раздел "Advertisers"
2. Нажмите "+ Create Advertiser"
3. Заполните:
   - **Name**: Название рекламодателя
   - **Domains**: Разрешенные домены (по одному на строку)
   - **Active**: Включить контейнер
4. Нажмите "Save"

### 3. Получение кода контейнера

1. Откройте детали рекламодателя
2. Скопируйте сгенерированный код
3. Вставьте в `<head>` вашего сайта:

```html
<!-- TSPRTG Container -->
<script type="text/javascript">
(function(w,d,c){
    var r=d.readyState;
    if(r!=='interactive'&&r!=='complete'){
        return setTimeout(function(){arguments.callee(w,d,c)},100);
    }
    var s=d.createElement('script');
    s.async=true;
    s.src='//tsprtg.com/c/'+c+'/l.js?v='+(+new Date());
    (d.body||d.head).appendChild(s);
    w._tsprtg=w._tsprtg||{};
    w._tsprtg.cid=c;
})(window,document,'adv_xxxxx');
</script>
```

### 4. Добавление скриптов

#### Глобальные скрипты (для всех рекламодателей)
1. Перейдите в "Global Scripts"
2. Нажмите "+ Add Global Script"
3. Настройте скрипт
4. Сохраните

#### Скрипты рекламодателя
1. Откройте детали рекламодателя
2. Перейдите в раздел "Container Scripts"
3. Нажмите "+ Add Script"
4. Выберите тип:
   - **External**: URL внешнего скрипта
   - **Inline**: JavaScript код
5. Установите приоритет (меньше = выше приоритет)
6. Сохраните

### 5. Мониторинг работоспособности

1. Перейдите в "Health Monitor"
2. Смотрите статусы контейнеров:
   - 🟢 **Активен** - загружен за последние 24 часа
   - 🟡 **Неактивен** - не загружался более 24 часов
   - 🔴 **Никогда** - еще не загружался
3. Просматривайте логи активности

---

## Обслуживание

### Просмотр логов

```bash
# Docker
sudo docker-compose logs -f

# Systemd
sudo journalctl -u tsprtg-backend -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Обновление приложения

```bash
cd /opt/tsprtg
sudo git pull

# Docker
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d

# Systemd
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart tsprtg-backend

cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

### Резервное копирование базы данных

```bash
# SQLite
cp /opt/tsprtg/backend/tsprtg.db /backup/tsprtg.db.$(date +%Y%m%d)

# Автоматическое резервное копирование (cron)
# Добавьте в crontab:
0 2 * * * cp /opt/tsprtg/backend/tsprtg.db /backup/tsprtg.db.$(date +\%Y\%m\%d)
```

---

## Решение проблем

### Backend не запускается

```bash
# Проверьте статус
sudo systemctl status tsprtg-backend

# Просмотрите логи
sudo journalctl -u tsprtg-backend -n 50

# Проверьте конфигурацию
cat /opt/tsprtg/backend/.env
```

### Frontend не работает

```bash
# Проверьте сборку
cd /opt/tsprtg/frontend
npm run build

# Проверьте права доступа
ls -la dist/
```

### Nginx ошибки

```bash
# Проверьте конфигурацию
sudo nginx -t

# Просмотрите логи ошибок
sudo tail -f /var/log/nginx/error.log
```

### Docker проблемы

```bash
# Проверьте контейнеры
sudo docker-compose ps

# Просмотрите логи
sudo docker-compose logs backend
sudo docker-compose logs frontend

# Пересоберите
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
```

---

## Безопасность

### Контрольный список

- [x] Установить безопасный `ADMIN_TOKEN` в `.env`
- [x] Настроить файрвол (`ufw`)
- [x] Включить SSL/TLS (Let's Encrypt)
- [x] Настроить автоматическое резервное копирование
- [x] Регулярно обновлять систему
- [x] Использовать сильные пароли для базы данных
- [x] Ограничить доступ к админ-панели (опционально)

### Генерация безопасного токена

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Добавьте результат в `/opt/tsprtg/backend/.env`:
```
ADMIN_TOKEN=ваш_безопасный_токен_здесь
```

---

## Поддержка

### Документация
- **README.md** - Основная документация
- **QUICK_REFERENCE.md** - Быстрый справочник
- **deployment/DEPLOYMENT.md** - Детальное руководство по развертыванию
- **SECURITY.md** - Информация о безопасности

### API документация
После запуска откройте: `http://your-server:8000/docs`

### Вопросы
Откройте issue на GitHub: https://github.com/Anastasiia804/GTM_RT/issues

---

## Рекомендации по производительности

### Для высокой нагрузки

1. **Используйте PostgreSQL вместо SQLite**

```bash
# Установите PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Создайте базу данных
sudo -u postgres psql
CREATE DATABASE tsprtg;
CREATE USER tsprtg WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE tsprtg TO tsprtg;
\q

# Обновите .env
DATABASE_URL=postgresql://tsprtg:strong_password@localhost/tsprtg
```

2. **Настройте кэширование Nginx**

Уже настроено в конфигурации (5 минут для `/c/` endpoints)

3. **Используйте CDN**

Разместите frontend на CDN (Cloudflare, AWS CloudFront)

4. **Масштабирование**

Запустите несколько инстансов backend за load balancer

---

**Готово!** Ваша система TSPRTG Tag Manager развернута и готова к использованию! 🎉
