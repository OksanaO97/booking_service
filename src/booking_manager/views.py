from django.shortcuts import render, HttpResponse

def main_view(request):
    return HttpResponse(
        '<h1>Brils Booking</h1>'
        '<p>С помощью нашего сервиса вы сможете онлайн забронировать удобное время к вашему любимому мастеру.</p>'
        '<h3>Наши преимущества:</h3>'
        '<ul>'
        '<li>Актуальное расписание 24/7.</li>'
        '<li>Выбор специалиста и конкретной услуги.</li>'
        '<li>Подтверждение за пару кликов.</li>'
        '</ul>'

        '<p><a href="/booking_manager/schedule/"><b>Забронировать</b></a></p>'
    )

def schedule_view(request):
    return HttpResponse(
        '<h1>Brils Booking</h1>'
        '<p>Доступное время для записи на сегодня:</p>'
        '<ul>'
        '<li>12:00 - Свободно - <a href="#">Забронировать</a></li>'
        '<li>14:00 - Занято</li>'
        '<li>15:00 - Свободно - <a href="#">Забронировать</a></li>'
        '<li>17:00 - Свободно - <a href="#">Забронировать</a></li>'
        '</ul>'

    )

