from datetime import date

def current_date():
    return date.today().isoformat()

def current_time():
    return date.today().isoformat()

def location_stub():
    return "London, GB"

callables = {"TODAY" : current_date, "TIME" : current_time, "LOCATION" : location_stub}