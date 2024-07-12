import fastf1
from datetime import datetime

def get_session_data(year, grand_prix, session):
    session_data = fastf1.get_session(year, grand_prix, session)
    session_data.load()
    return session_data

def get_driver_names(session_data):
    drivers = session_data.drivers
    return {driver: session_data.get_driver(driver)['Abbreviation'] for driver in drivers}

def get_telemetry_data(session_data, driver, lap_number):
    lap = session_data.laps.pick_driver(driver).pick_lap(lap_number)
    telemetry = lap.get_telemetry()
    telemetry_data = {
        'Time': telemetry['Date'].tolist(),
        'Speed': telemetry['Speed'].tolist(),
        'Throttle': telemetry['Throttle'].tolist(),
        'Brake': telemetry['Brake'].tolist(),
        'Gear': telemetry['nGear'].tolist(),
        'DRS': telemetry['DRS'].tolist()
    }
    return telemetry_data

def get_available_grand_prix(year):
    schedule = fastf1.get_event_schedule(year)
    current_date = datetime.now()
    past_events = schedule[schedule['EventDate'] <= current_date]
    return past_events['EventName'].tolist()
