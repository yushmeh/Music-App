# 🎵 Music Dashboard — Аналитика истории прослушивания

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![ApexCharts](https://img.shields.io/badge/Charts-ApexCharts-FF6C37?style=for-the-badge)](https://apexcharts.com)
[![Style](https://img.shields.io/badge/UI-Spotify%20Dark%20Theme-1DB954?style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/CSS)

**Music Dashboard** — веб-приложение на **Django** для анализа истории прослушивания музыки. Читает данные из `music.json`, рассчитывает метрики и отображает интерактивный дашборд с графиками прямо в браузере.

---

## 📋 Содержание

- [🚀 Ключевые особенности](#-ключевые-особенности)
- [📂 Структура проекта](#-структура-проекта)
- [🛠 Инструкция по запуску](#-инструкция-по-запуску)
- [📊 Формат данных](#-формат-данных-musicjson)
- [📐 Рассчитываемые метрики](#-рассчитываемые-метрики)

---

## 🚀 Ключевые особенности

### 📊 Аналитика и визуализация
- **4 карточки-метрики** — суммарное время прослушивания, топ-жанр, самый популярный трек, общее количество треков.
- **Бар-чарт** — сравнение треков по количеству прослушиваний через **ApexCharts**.
- **Пончиковая диаграмма** — распределение времени прослушивания по жанрам.

### 🎛 Интерактивная таблица треков
- **Живой поиск** — фильтрация треков по любому полю в реальном времени без перезагрузки страницы.
- **Сортировка** — по любому столбцу таблицы одним кликом.

### 🏗 Архитектура
- Вся аналитическая логика сосредоточена в `views.py` — Django-шаблон получает уже готовые метрики.
- Данные читаются из плоского `music.json` через встроенный модуль `json` — без базы данных и ORM.
- Все внешние зависимости (ApexCharts, Google Fonts) подключаются через CDN.

---

## 📂 Структура проекта

```text
musicapp/
├── manage.py
├── music.json                   # Данные о треках
├── requirements.txt
├── musicapp/                    # Конфигурация Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── dashboard/                   # Основное приложение
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    ├── views.py                 # Логика чтения данных и расчёт метрик
    └── templates/
        └── dashboard/
            └── index.html       # UI, графики ApexCharts
```

---

## 🛠 Инструкция по запуску

Для работы приложения необходим **Python 3.14+**.

```bash
# 1. Перейти в папку проекта
cd musicapp

# 2. Создать виртуальное окружение (рекомендуется)
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить сервер
python manage.py runserver

# 5. Открыть в браузере
# http://127.0.0.1:8000
```

> ApexCharts и Google Fonts подключаются через CDN — для корректного отображения необходим доступ в интернет.

---

## 📊 Формат данных (`music.json`)

Файл должен находиться рядом с `manage.py`. Каждый объект массива — один трек:

```json
[
  {
    "track_name": "Blinding Lights",
    "artist": "The Weeknd",
    "genre": "Synth-pop",
    "duration_minutes": 3.45,
    "listens": 87
  }
]
```

| Поле | Тип | Описание |
| :--- | :---: | :--- |
| `track_name` | `string` | Название трека |
| `artist` | `string` | Исполнитель |
| `genre` | `string` | Жанр |
| `duration_minutes` | `float` | Длительность трека в минутах |
| `listens` | `int` | Количество прослушиваний |

---

## 📐 Рассчитываемые метрики

| Метрика | Формула |
| :--- | :--- |
| Суммарное время | `Σ (duration_minutes × listens)` |
| Топ-жанр | Жанр с наибольшим числом треков |
| Самый прослушиваемый трек | Трек с максимальным значением `listens` |
| Время на жанр (график) | `Σ (duration_minutes × listens)` по каждому жанру |

---

## 👥 Авторы

[@yushmeh](https://github.com/yushmeh)
