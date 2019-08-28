import datetime

# Google Maps Platform Directions API endpoint
import json
import math
from typing import List
from urllib import *
from urllib import parse, request
import matplotlib.pyplot as plt

from math import sin, cos, tan, atan2, acos, pi

import numpy as np

from src.module.hubeny import script

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyCTBYL5tJjHIUdsAsMKKdo--8-3fHWk6MY'

# 出発地、目的地を入力
# origin = input('出発地を入力: ').replace(' ', '+')
# destination = input('目的地を入力: ').replace(' ', '+')
# dep_time = input('出発時間を入力: yyyy/mm/dd hh:mm 形式 ')

origin = '東京駅'
destination = 'スカイツリー'
dep_time = '2019/08/29 11:00'

# UNIX時間の算出
dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
unix_time = int(dtime.timestamp())

nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}' \
    .format(origin, destination, unix_time, api_key)
nav_request = parse.quote_plus(nav_request, safe='=&')

pi = math.pi


class Route:
    def __init__(self, directions):
        leg = directions['routes'][0]['legs'][0]
        self.start_location = Location(leg['start_location'])
        self.end_location = Location(leg['end_location'])
        self.steps = [Step(step) for step in leg['steps']]


class Step:
    def __init__(self, step):
        self.start_location = Location(step['start_location'])
        self.end_location = Location(step['end_location'])
        self.time = step['duration']['value']
        self.distance = int(step['distance']['value']) / 1000


class Location:
    def __init__(self, location):
        self.lat = location['lat']
        self.lng = location['lng']


def split_unit_time(steps: List[Step], unit_time: int):
    time = 0
    unit_steps = []
    for step in steps:
        print()


def calculate_point(point: Location, angle: float, time: int):
    print()


def calculate_theta(start: Location, end: Location):
    x1, y1 = start.lat, start.lng
    x2, y2 = end.lat, end.lng
    # Radian角に修正
    _x1, _y1, _x2, _y2 = x1 * pi / 180, y1 * pi / 180, x2 * pi / 180, y2 * pi / 180
    Δx = _x2 - _x1
    _y = math.sin(Δx)
    _x = math.cos(_y1) * math.tan(_y2) - math.sin(_y1) * math.cos(Δx)

    psi = math.atan2(_y, _x) * 180 / pi
    if psi < 0:
        return 360 + math.atan2(_y, _x) * 180 / pi
    else:
        return math.atan2(_y, _x) * 180 / pi


def distance(start: Location, end: Location):
    x1, y1 = start.lat, start.lng
    x2, y2 = end.lat, end.lng
    _x1, _y1, _x2, _y2 = x1 * pi / 180, y1 * pi / 180, x2 * pi / 180, y2 * pi / 180
    Δx = _x2 - _x1
    val = sin(_y1) * sin(_y2) + cos(_y1) * cos(_y2) * cos(Δx)
    return 6378.137e3 * acos(val) / 1e3


def main():
    # Google Maps Platform Directions APIを実行
    response = None
    with request.urlopen(endpoint + nav_request) as url:
        response = url.read()

    # 結果(JSON)を取得
    route = Route(json.loads(response))

    script(route.steps)

    for step in route.steps:

        print(step.distance)
        print(distance(step.start_location, step.end_location))
        break


if __name__ == '__main__':
    main()
