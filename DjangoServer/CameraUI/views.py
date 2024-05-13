import cv2
import numpy as np
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
import project_settings as p_settings
from .models import Person, Sighting

def persons_table_view(request):
    query = request.GET.get('query')
    if query:
        persons = Person.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        persons = Person.objects.all()
    return render(request, 'persons_table.html', {'persons': persons})


def sighting_list_view(request, person_id):
    sightings = Sighting.objects.filter(person_id=person_id).order_by('sighting_time')
    return render(request, 'sighting_list.html', {'sightings': sightings})


def main(request):
    return render(request, 'index.html')


def webcam_page(request):
    if request.method == 'POST':
        # Получаем данные из POST запроса
        last_name = request.POST.get('last_name', '')
        first_name = request.POST.get('first_name', '')
        patronymic = request.POST.get('patronymic', '')
        photo_data = request.FILES['photo'].read()  # Получаем данные файла

        # Преобразуем фото для распознавания
        photo_array = np.frombuffer(photo_data, np.uint8)
        photo = cv2.imdecode(photo_array, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        faces = p_settings.face_detector

        if len(faces) == 0:
            return HttpResponse('Лица на фотографии не обнаружены!')

        # Получаем дескриптор лица
        landmarks = p_settings.shape_predictor(gray, faces[0])
        face_descriptor = p_settings.face_recognizer(photo, landmarks)
        face_descriptor = np.array(face_descriptor).tobytes()

        # Сохраняем данные в модель Person
        person = Person.objects.create(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            face_descriptor=face_descriptor,
            photo=photo_data
        )
        person.save()

        # Перенаправляем на другую страницу или выводим сообщение об успешном сохранении
        return HttpResponse('Данные успешно сохранены!')

    else:
        # Если запрос не методом POST, просто отображаем страницу
        return render(request, 'webcam.html')
