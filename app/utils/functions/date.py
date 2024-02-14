from datetime import datetime, timedelta
import calendar
from typing import List, Dict


def parse_date_detection(date_string: str):
    try:
        if date_string is None or date_string.strip() == "":
            return None
        else:
            tanggal_date = datetime.strptime(date_string, "%Y-%m-%d").date()
            return tanggal_date
    except ValueError:
        return None


def get_current_date():
    return datetime.now().date()


def get_current_time():
    return datetime.now().time()


nama_hari_indonesia = {
    'Monday': 'Senin',
    'Tuesday': 'Selasa',
    'Wednesday': 'Rabu',
    'Thursday': 'Kamis',
    'Friday': 'Jumat',
    'Saturday': 'Sabtu',
    'Sunday': 'Minggu'
}


def generate_previous_n_day_violator_statistic_date_range(end_date, days_num=6):
    start_date = end_date - timedelta(days=days_num)
    date_range = [{
        'date': str(start_date + timedelta(days=x)),
        'detectedViolatorTotal': 0,
        'detectedObeyTotal': 0,
        'dayName': nama_hari_indonesia[calendar.day_name[(start_date + timedelta(days=x)).weekday()]]
    } for x in range((end_date - start_date).days + 1)]
    return date_range


# def fill_empty_hours(results: List[Dict[int, int]]):
#     filled_results = {hour: [0, 0] for hour in range(24)}
#     for result in results:
#         filled_results[result['jam']] = [
#             result['detectedViolatorTotal'],
#             result['detectedObeyTotal']
#         ]

#     return [{'detectedViolatorTotal': count[0], 'detectedObeyTotal': count[1]} for hour, count in filled_results.items()]
