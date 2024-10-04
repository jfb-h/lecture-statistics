import random

def simulate_latlon():
    # Germany
    ger_lat_min = 47.2701
    ger_lat_max = 55.0581
    ger_lon_min = 5.8663
    ger_lon_max = 15.0419

    # Munich
    muc_lat_min = 48.028
    muc_lat_max = 48.227
    muc_lon_min = 11.450
    muc_lon_max = 11.686

    lat_current = random.uniform(muc_lat_min, muc_lat_max)
    lon_current = random.uniform(muc_lon_min, muc_lon_max)

    lat_before = random.uniform(ger_lat_min, ger_lat_max)
    lon_before = random.uniform(ger_lon_min, ger_lon_max)

    return {
        'lat_current': lat_current, 'lon_current': lon_current,
        'lat_before': lat_before, 'lon_before': lon_before
    }

