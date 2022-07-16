from django.contrib.gis.geoip2 import GeoIP2


def geo_locate(ip):
    geo_helper = GeoIP2()
    country = geo_helper.country(ip)
    city = geo_helper.city(ip)
    lat, lon = geo_helper.lat_lon(ip)
    return country, city, lat, lon


def cordinate_centralise(latA, lonA, latB=None, lonB=None):
    cord = (latA, lonA)
    if latB:
        cord = [(latA+latB)/2, (lonA+lonB)/2]
    return cord


def get_zoom(distane):
    if distane <= 100:
        return 8
    elif distane < 100 and distane <= 5000:
        return 4
    else:
        return 2

