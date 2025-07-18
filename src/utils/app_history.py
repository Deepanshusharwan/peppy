import datetime
import json
import os
from pathlib import Path
from typing import TypedDict


class AppOpenCounts(TypedDict):
    open_count: int
    recent_open: str


_app_open_counts_cache = None


def get_app_count_file_path() -> Path:
    p = Path(f"{os.environ.get('HOME', '~')}/.local/share/peppy/app_open_count.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def get_app_open_counts_dict() -> dict[str, AppOpenCounts]:
    global _app_open_counts_cache
    if _app_open_counts_cache is None:
        try:
            _app_open_counts_cache = json.loads(get_app_count_file_path().read_text())
        except Exception:
            _app_open_counts_cache = {}

    datetime_30d_ago = datetime.datetime.now() - datetime.timedelta(days=30)

    # Remove entries older than 30 days
    for app_exec in list(_app_open_counts_cache.keys()):
        obj = _app_open_counts_cache[app_exec]
        recent_open = datetime.datetime.strptime(
            obj["recent_open"], "%Y-%m-%d %H:%M:%S"
        )
        if recent_open < datetime_30d_ago:
            _app_open_counts_cache.pop(app_exec, None)

    return _app_open_counts_cache


def get_app_open_count(app_exec: str) -> int:
    return get_app_open_counts_dict().get(app_exec, {}).get("open_count", 0)


def increment_app_open_count(app_exec: str):
    app_open_counts = get_app_open_counts_dict()
    app_open_counts[app_exec] = {
        "open_count": app_open_counts.get(app_exec, {}).get("open_count", 0) + 1,
        "recent_open": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    get_app_count_file_path().write_text(json.dumps(app_open_counts))
