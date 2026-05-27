# Music Dashboard

Веб-приложение на Django для анализа истории прослушивания музыки.  
Читает данные из `music.json`, считает метрики и отображает интерактивный дашборд в браузере.

---

## Возможности

- **4 карточки-метрики** — суммарное время, топ-жанр, самый прослушиваемый трек, количество треков
- **Интерактивные графики** (ApexCharts) — бар-чарт по прослушиваниям и пончиковая диаграмма по жанрам
- **Таблица треков** с живым поиском и сортировкой по любому столбцу
- Тёмная тема в стиле Spotify

---

## Структура проекта

```
musicapp/
├── manage.py
├── music.json                        # Данные о треках
├── requirements.txt
├── musicapp/                         # Конфигурация Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── dashboard/                        # Основное приложение
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    ├── views.py                      # Логика + аналитика
    └── templates/
        └── dashboard/
            └── index.html            # UI + графики
```

---

## Установка и запуск

**1. Клонируй или скопируй проект**

```bash
cd musicapp
```

**2. Создай виртуальное окружение (опционально, но рекомендуется)**

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

**3. Установи зависимости**

```bash
pip install -r requirements.txt
```

**4. Запусти сервер**

```bash
python manage.py runserver
```

**5. Открой в браузере**

```
http://127.0.0.1:8000
```

---

## Формат данных (`music.json`)

Файл должен лежать рядом с `manage.py`. Каждый объект — один трек:

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

| Поле               | Тип    | Описание                        |
|--------------------|--------|---------------------------------|
| `track_name`       | string | Название трека                  |
| `artist`           | string | Исполнитель                     |
| `genre`            | string | Жанр                            |
| `duration_minutes` | float  | Длительность трека в минутах    |
| `listens`          | int    | Количество прослушиваний        |

---

## Рассчитываемые метрики

| Метрика                    | Формула                                      |
|----------------------------|----------------------------------------------|
| Суммарное время            | `Σ (duration_minutes × listens)`             |
| Топ-жанр                   | Жанр с наибольшим числом треков              |
| Самый прослушиваемый трек  | Трек с максимальным значением `listens`      |
| Время на жанр (график)     | `Σ duration_minutes × listens` по каждому жанру |

---

## Стек технологий

| Слой       | Технология                  |
|------------|-----------------------------|
| Backend    | Python 3.14, Django 6.x     |
| Данные     | JSON (встроенный модуль)    |
| Frontend   | HTML5, CSS3, JavaScript     |
| Графики    | ApexCharts (CDN)            |
| Шрифты     | Syne + DM Sans (Google Fonts) |

---

## Зависимости

```
django>=5.0
```

Все остальные зависимости (ApexCharts, Google Fonts) подключаются через CDN — интернет при запуске обязателен.

---

## Возможные ошибки

**`TemplateDoesNotExist: dashboard/index.html`**  
Убедись, что шаблон лежит по пути `dashboard/templates/dashboard/index.html` (две вложенные папки `dashboard`).

**`WSGI application could not be loaded`**  
Замени содержимое `musicapp/wsgi.py` на:
```python
import os
import django
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musicapp.settings")
django.setup()
application = WSGIHandler()
```

**`FileNotFoundError: music.json`**  
Файл `music.json` должен находиться в одной папке с `manage.py`.
