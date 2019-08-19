from django.shortcuts import render
from .models import SkillPer
from django.http import HttpResponse, JsonResponse
from django.shortcuts import reverse, redirect
from django.db import connection
import datetime, time

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


def constart(request):
    def distinct(a):
        b = []
        for i in a:
            if not i in b:
                b.append(i)
        return b
    c = SkillPer.objects.all().values()

    xAxisData = distinct([i['skill_name'] for i in c]) # x轴坐标
    data1 = [str(i['time']) for i in c]
    legendData = ['trend'] + distinct(data1)  # 时间
    encodeY = list(range(1, len(c)))
    custom = []

    for i in xAxisData:
        data2 = [i for i in SkillPer.objects.filter(skill_name=i).values()]
        custom.append(data2)
    xAxisDataList = []
    for key, value in enumerate(xAxisData):
        xAxisDataList.append([])
        for key2, x in enumerate(legendData[1:]):
            fmt = '%Y-%m-%d'
            time_tuple = time.strptime(x, fmt)
            year, month, day = time_tuple[:3]
            a_date = datetime.date(year, month, day)
            try:
                search_data = SkillPer.objects.filter(skill_name=value, time=a_date).values()[0]['skill_level']
                xAxisDataList[key].append(search_data)
            except:
                index1 = legendData[1:].index(x)
                new_list = legendData[1:][:index1]

                leg = len(new_list)
                num = 0
                xAxisDataList[key].append('null')
                if len(new_list):
                    for skill_time in new_list:
                        try:
                            search_data2 = SkillPer.objects.filter(skill_name=value, time=skill_time).values()[0]['skill_level']
                            del xAxisDataList[key][-1]
                            xAxisDataList[key].append(search_data2)
                        except:
                            pass

    def func(item):
        list_ = []
        for i in item:
            if i == '陌生':
                list_.append(0)
            elif i == '了解':
                list_.append(1)
            elif i == '掌握':
                list_.append(2)
            elif i == '熟练':
                list_.append(3)
            elif i == '精通':
                list_.append(4)
            else:
                list_.append(0)
        return [xAxisDataList.index(item)]+list_

    customData = list(map(func, xAxisDataList))

    count = max([len(i[1:]) for i in customData])
    dataList = []
    for i in range(count):
        dataListChild = []

        for x in customData:

            dataListChild.append(x[1:][i])
        dataList.append(dataListChild)

    content = {
        'xAxisData': json.dumps(xAxisData),
        'customData': json.dumps(customData),
        'legendData': json.dumps(legendData),
        'dataList': json.dumps(dataList),
        'encodeY': json.dumps(encodeY)
               }
    return render(request, 'constrast.html', context=content)
