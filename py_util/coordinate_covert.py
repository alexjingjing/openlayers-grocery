import math as Math

x_PI = 3.14159265358979324 * 3000.0 / 180.0
PI = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323

"""
这个文件提供了一些坐标转换的方法，适用于中国的一些地图供应商，如百度、高德等。
百度使用的坐标系是bd09
高德使用的坐标系是gcj02
通用的坐标系是wgs84
在OpenLayers中：
wgs84的代号是EPSG:4326
最终转换到OpenLayers的坐标是球面坐标系，EPSG:3857
我们可以使用OpenLayers的坐标转换方法，将wgs84的坐标呈现在地图上。
ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857')
"""

def bd09togcj02(bd_lon, bd_lat):
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * x_PI)
    theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_PI)
    gg_lng = z * Math.cos(theta)
    gg_lat = z * Math.sin(theta)
    return gg_lng, gg_lat


def gcj02tobd09(lng, lat):
    """
       * 火星坐标系 (GCJ-02) 与百度坐标系 (BD-09) 的转换
       * 即谷歌、高德 转 百度
       * @param lng
       * @param lat
       * @returns {*[]}
    """
    z = Math.sqrt(lng * lng + lat * lat) + 0.00002 * Math.sin(lat * x_PI)
    theta = Math.atan2(lat, lng) + 0.000003 * Math.cos(lng * x_PI)
    bd_lng = z * Math.cos(theta) + 0.0065
    bd_lat = z * Math.sin(theta) + 0.006
    return bd_lng, bd_lat


def wgs84togcj02(lng, lat):
    """
       * WGS84转GCj02
       * @param lng
       * @param lat
       * @returns {*[]}
       """
    if out_of_china(lng, lat):
        return lng, lat
    else:
        dlat = transformlat(lng - 105.0, lat - 35.0)
        dlng = transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * PI
        magic = Math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = Math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (a / sqrtmagic * Math.cos(radlat) * PI)
        mglat = lat + dlat
        mglng = lng + dlng
        return mglng, mglat


def gcj02towgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    else:
        dlat = transformlat(lng - 105.0, lat - 35.0)
        dlng = transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * PI
        magic = Math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = Math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (a / sqrtmagic * Math.cos(radlat) * PI)
        mglat = lat + dlat
        mglng = lng + dlng
        return lng * 2 - mglng, lat * 2 - mglat


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * Math.sqrt(abs(lng))
    ret += (20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * Math.sin(lat * PI) + 40.0 * Math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * Math.sin(lat / 12.0 * PI) + 320 * Math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * Math.sqrt(abs(lng))
    ret += (20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * Math.sin(lng * PI) + 40.0 * Math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * Math.sin(lng / 12.0 * PI) + 300.0 * Math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    return not lng > 73.66 and lng < 135.05 and 3.86 < lat < 53.55