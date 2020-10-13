from django.shortcuts import render
import json
import requests
from bs4 import BeautifulSoup


# Create your views here.
def search_busstop_by_name(request):
    pass


def search_busstop_by_location(request):
    pass


def findBusstopIdsByLocation(x, y):
    url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice/searcharound?serviceKey=1234567890&x=' + x + '&y=' + y
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    stationName = soup.select('stationName')
    stationId = soup.select('stationId')
    x = soup.select('x')
    y = soup.select('y')
    stationName_Id_x_y = list(zip(stationId, stationName, x, y))
    bus_stops = []
    for stationId, stationName, x, y in stationName_Id_x_y:
        bus_stops.append([stationId.text, stationName.text, x.text, y.text])
    return bus_stops


def findBusstopIdsByName(keyword):
    url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=1234567890&keyword=' + keyword
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    stationName = soup.select('stationName')
    stationId = soup.select('stationId')
    x = soup.select('x')
    y = soup.select('y')

    stationName_Id_x_y = list(zip(stationId, stationName, x, y))
    bus_stops = []
    for stationId, stationName, x, y in stationName_Id_x_y:
        bus_stops.append([stationId.text, stationName.text, x.text, y.text])
    return bus_stops


def findBusRoutedIdAndTimeByBusstopId(stationId):
    url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=1234567890&stationId=' + stationId
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 첫번째 도착예정 차량 routeId
    routeId = soup.select('routeId')
    predictTime1 = soup.select('predictTime1')
    routeAndPredict = list(zip(routeId, predictTime1))
    will_arrivals = []
    for route, predictTime in routeAndPredict:
        will_arrivals.append([findBusNumberByRoutedId(route.text), predictTime.text])
        # print(f"{findBusNumber(route.text)}번 버스는 " + predictTime.text + "분 후에 옵니다.")
    return will_arrivals


def findBusNumberByRoutedId(routeId):
    # routeId 와 버스 노선 mapping
    url = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=1234567890&routeId=' + routeId
    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    routeId = soup.select('routeId')[0].text
    routeName = soup.select('routename')[0].text
    # print(f"routeId {routeId} 의 버스 번호는 {routeName} 번입니다.")
    return routeName
