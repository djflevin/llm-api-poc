from datetime import date

def current_date():
    return date.today().isoformat()

callables = {"TODAY" : current_date}