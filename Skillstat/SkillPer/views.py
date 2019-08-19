from django.shortcuts import render
from .models import SkillPer
from django.http import HttpResponse, JsonResponse
from django.shortcuts import reverse, redirect
from django.db import connection
from rest_framework import serializers
import json


def per_list(request):
    cursor = connection.cursor()
    cursor.execute(
        "select * from skill_person  order by FIELD(`skill_level`,'陌生','了解','掌握','熟练','精通')")
    skills = dict_fetchall(cursor)
    # skills = SkillPer.objects.all().order_by('skill_level').values()
    context = {
        'skills': skills
    }
    return render(request, 'skill_list_person.html', context=context)


def add_skill(request):
    if request.method == 'GET':
        return render(request, 'add_skill_person.html')
    else:
        user = request.POST.get('userId')
        skill = request.POST.get('skillName')
        level = request.POST.get('level')
        category = request.POST.get('category')
        skill_per = SkillPer(user_id=user, skill_name=skill, skill_level=level, category=category)
        skill_per.save()
        return redirect(reverse('SkillPer:perList'))


def delete_item(request):
    if request.method == 'GET':
        return render(request, 'skill_list_person.html')
    else:
        index = request.POST.get('index')
        skill = SkillPer.objects.get(id=index)
        skill.delete()
        return HttpResponse('OK')


def edit_item(request):
    if request.method == 'GET':
        return render(request, 'skill_list_person.html')
    else:
        index = request.POST.get('id')
        name = request.POST.get('name')
        level = request.POST.get('level')
        category = request.POST.get('category')
        skill = SkillPer.objects.get(id=index)
        skill.skill_name = name
        skill.skill_level = level
        skill.category = category
        skill.save()
        return HttpResponse('OK')


def dict_fetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()]
# def test(request):
#     skills = SkillPer.objects.all().order_by('skill_level').values()
#     aaa = list(skills)
#     return JsonResponse(aaa, safe=False)
