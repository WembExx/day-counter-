import json
import os
from datetime import datetime ,date

FILE = "tracker.json"

def load_start():
    """Читает стартовую дату из файла. Если файла нет — создаёт."""
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return datetime.fromisoformat(data["start"])

    # Первый запуск — старт с текущего момента
    start = datetime.now()
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({"start": start.isoformat()}, f, ensure_ascii=False)
    return start

def start_date():
    return load_start().strftime('%d.%m.%Y %H:%M:%S')

def current_date():
    return datetime.now().strftime('%d.%m.%Y %H:%M:%S')

def reset_date():
    os.remove(FILE)
    load_start()

def format_delta(diff):
    """Превращает timedelta в дни/часы/минуты/секунды."""
    total = int(diff.total_seconds())

    days    = total // 86400
    hours   = (total % 86400) // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60

    return days, hours, minutes, seconds

def show():
    """Выводит прошедшее время."""
    start = load_start()
    diff = datetime.now() - start
    d, h, m, s = format_delta(diff)

    line = f"⏱  {d}д {h:02d}:{m:02d}:{s:02d}"
    return line

def string_to_date(date_str, time):
    try:
        _date = datetime.strptime(f'{date_str} {time}', '%d.%m.%Y %H:%M')

        if _date > datetime.now():
            print('Невозможная дата!')
        else: 
            with open(FILE, "w", encoding="utf-8") as f:
                json.dump({"start": _date.isoformat()}, f, ensure_ascii=False)
            return True
    except ValueError as error:
        if date_str == '' or time == '':
            print('Введите значения!')
        else: 
            print('Неверное значение!')
            return False

def main():
    start = load_start()
    print(f"📅 Старт: {start.strftime('%d.%m.%Y %H:%M:%S')}")
    show(start)
