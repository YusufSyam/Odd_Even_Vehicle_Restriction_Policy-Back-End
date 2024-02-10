from datetime import datetime

def parse_date_detection(date_string:str):
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