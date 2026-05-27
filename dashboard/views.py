from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import TypeAlias

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# ── Типовые псевдонимы ────────────────────────────────────────────────────────
Track: TypeAlias = dict[str, str | float | int]
Playlist: TypeAlias = list[Track]


# ─────────────────────────────────────────────────────────────────────────────
# Утилиты
# ─────────────────────────────────────────────────────────────────────────────

def _load_tracks() -> Playlist:
    """Читает и возвращает треки из MUSIC_JSON_PATH."""
    path: Path = settings.MUSIC_JSON_PATH
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _total_listening_time(tracks: Playlist) -> dict[str, int]:
    """Суммарное прослушанное время: Σ duration_minutes × listens."""
    total_min = sum(t["duration_minutes"] * t["listens"] for t in tracks)
    hours, minutes = divmod(int(total_min), 60)
    return {"hours": hours, "minutes": minutes, "total_min": round(total_min, 1)}


def _top_genre(tracks: Playlist) -> str:
    """Жанр, встречающийся среди треков чаще всего."""
    return Counter(t["genre"] for t in tracks).most_common(1)[0][0]


def _most_played(tracks: Playlist) -> Track:
    """Трек с максимальным числом прослушиваний."""
    return max(tracks, key=lambda t: t["listens"])


def _chart_data(tracks: Playlist) -> dict:
    """
    Данные для двух графиков ApexCharts:
      • bar  — топ-треки по прослушиваниям (сортировка по убыванию)
      • donut — суммарное время по жанрам
    Возвращает словарь, который сериализуется в JSON прямо в шаблоне.
    """
    # Бар-чарт: сортируем по listens desc
    sorted_tracks = sorted(tracks, key=lambda t: t["listens"], reverse=True)
    bar_labels = [f"{t['track_name']} – {t['artist']}" for t in sorted_tracks]
    bar_values = [t["listens"] for t in sorted_tracks]

    # Пончик: агрегируем total_time по жанру
    genre_time: dict[str, float] = {}
    for t in tracks:
        genre_time[t["genre"]] = round(
            genre_time.get(t["genre"], 0) + t["duration_minutes"] * t["listens"], 1
        )
    donut_labels = list(genre_time.keys())
    donut_values = list(genre_time.values())

    return {
        "bar": {"labels": bar_labels, "values": bar_values},
        "donut": {"labels": donut_labels, "values": donut_values},
    }


# ─────────────────────────────────────────────────────────────────────────────
# View
# ─────────────────────────────────────────────────────────────────────────────

def index(request: HttpRequest) -> HttpResponse:
    tracks = _load_tracks()

    # Добавляем вычисляемое поле к каждому треку для таблицы
    for t in tracks:
        t["total_time"] = round(t["duration_minutes"] * t["listens"], 1)

    context = {
        "tracks": tracks,
        "listening_time": _total_listening_time(tracks),
        "top_genre": _top_genre(tracks),
        "most_played": _most_played(tracks),
        "total_tracks": len(tracks),
        # JSON-строка для JS — безопасная передача данных в шаблон
        "chart_data_json": json.dumps(_chart_data(tracks)),
    }
    return render(request, "dashboard/index.html", context)
