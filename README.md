# Weather Monitoring

Простое веб-приложение для отображения текущей погоды с мониторингом на базе Prometheus и Grafana.

## Структура проекта
```
.
├── app.py                # Основное приложение на FastAPI
├── Dockerfile            # Конфигурация Docker образа
├── docker-compose.yml    # Оркестрация контейнеров
├── requirements.txt      # Зависимости Python
├── prometheus.yml        # Конфигурация Prometheus
├── README.md             # Документация
└── grafana-datasources
    └── datasource.yml    # Конфигурация Grafana
```

## Функциональность
- Получение текущей температуры через OpenWeatherMap API
- Экспорт метрик в формате Prometheus
- Health-check эндпоинт для проверки доступности
- Контейнеризация с Docker
- Мониторинг доступности и метрик приложения

## Старт приложения
1. Предварительные требования
- Docker, Docker Compose
- API ключ от OpenWeatherMap (бесплатно на https://openweathermap.org/)
2. Запуск
```bash
# Клонируйте проект
git clone https://github.com/PASTER-G/Weather-monitoring.git
cd Weather-monitoring

# Создайте файл .env
cp .env.example .env

# Отредактируйте .env файл, добавьте ваш API ключ
nano .env

# Запустите все сервисы
docker-compose up -d

# Проверьте запущенные контейнеры
docker-compose ps
```
## Доступные сервисы
- Приложение: http://localhost:8000 
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Автор

[PASTER-G](https://github.com/PASTER-G)  