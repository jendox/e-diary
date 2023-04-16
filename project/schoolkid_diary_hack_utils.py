import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation


def fix_marks(schoolkid_name: str) -> bool:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print(f"ERROR: There is no schoolkid named '{schoolkid_name}'")
        return False
    except MultipleObjectsReturned:
        print(f"ERROR: Found a lot of schoolkids named '{schoolkid_name}'")
        return False
    kid_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in kid_marks:
        mark.points = 5
        mark.save()
    print(f"Good job! {schoolkid_name}'s marks successfully fixed!")
    return True


def remove_chastisements(schoolkid_name: str) -> bool:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print(f"ERROR: There is no schoolkid named '{schoolkid_name}'")
        return False
    except MultipleObjectsReturned:
        print(f"ERROR: Found a lot of schoolkids named '{schoolkid_name}'")
        return False
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()
    print(f"Good job! {schoolkid_name}'s chastisements successfully removed!")
    return True


def get_random_commendation_text() -> str:
    return random.choice([
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ])


def create_commendation(schoolkid_name: str, subject_name: str) -> Commendation | None:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print(f"ERROR: There is no schoolkid named '{schoolkid_name}'")
        return None
    except MultipleObjectsReturned:
        print(f"ERROR: Found a lot of schoolkids named '{schoolkid_name}'")
        return None
    try:
        subject = Subject.objects.get(title=subject_name, year_of_study=schoolkid.year_of_study)
    except ObjectDoesNotExist:
        print(f"ERROR: There is no school subject named {subject_name}")
        return None

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('-date').first()
    commendation = Commendation.objects.create(
        text=get_random_commendation_text(),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=lesson.teacher
    )
    print(f"Good job! A commendation successfully added!")
    return commendation
