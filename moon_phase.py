import ephem

def get_moon_phase(date_str, lat='0', lon='0'):
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.date = date_str
    moon = ephem.Moon(observer)
    return moon.phase