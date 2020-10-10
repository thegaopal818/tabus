from django.shortcuts import render


# Create your views here.
def show_navigation(request):
    # 경로를 안내한다.
    # 현재 위치 부터 목적지까지를
    # 30초 마다 리젠된다.
    # geolocation으로 마커 표시하기

    # 시각장애인을 위한 음성지도 제작에 관한 연구 - 국토지리학회 에서 말하길 시각 장애인의 보행 속도는 1m / 1초이다.
    # 일반인의 보행 속도는  4km/시  = 4000m / 3600s =1.11m/s 이므로   예상 도착 시간 곱하기 1.11 배 한다

    data = {
        "destination_lat": request.GET['destination_lat'],
        "destination_lon": request.GET['destination_lon'],
        "destination_name": str(request.GET['destination_name'])
    }
    print(data["destination_name"])
    print(data["destination_lat"])
    print(data["destination_lon"])
    return render(request, 'maps/navigation.html', data)


def search_place(request):
    return render(request, 'maps/search_place.html')


def test(request):
    return render(request, 'maps/test.html')
