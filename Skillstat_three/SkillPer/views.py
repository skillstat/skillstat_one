import datetime
import json
import time
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import reverse, redirect
from django.views.generic import ListView
from .models import SkillPer


# 个人增加技能
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
        return redirect(reverse('SkillPer:list'))


# 个人删除技能
def delete_item(request):
    if request.method == 'GET':
        return render(request, 'skill_list_person.html')
    else:
        index = request.POST.get('index')
        skill = SkillPer.objects.get(id=index)
        skill.delete()
        return HttpResponse('OK')


# 个人编辑技能
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


# Mysql转字典
def dict_fetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()]


# def test(request):
#     skills = SkillPer.objects.all().order_by('skill_level').values()
#     aaa = list(skills)
#     return JsonResponse(aaa, safe=False)

#  个人技能对比
def contrast(request):
    def distinct(a):
        b = []
        for i in a:
            if not i in b:
                b.append(i)
        return b

    c = SkillPer.objects.all().values()
    xAxisData = distinct([i['skill_name'] for i in c])  # x轴坐标
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
                            search_data2 = SkillPer.objects.filter(skill_name=value, time=skill_time).values()[0][
                                'skill_level']
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
        return [xAxisDataList.index(item)] + list_

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
    return render(request, 'contrast.html', context=content)


# 分页功能
class SkillListView(ListView):
    model = SkillPer
    template_name = 'skill_list_person.html'
    context_object_name = 'skills'
    paginate_by = 10
    page_kwarg = 'p'

    def get_queryset(self):
        cursor = connection.cursor()
        cursor.execute(
            "select * from skill_person  order by time,FIELD(`skill_level`,'陌生','了解','掌握','熟练','精通')")
        skills = dict_fetchall(cursor)
        return skills

    def get_context_data(self, **kwargs):
        context = super(SkillListView, self).get_context_data(*kwargs)
        # context['username'] = 'zhiliao'
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj, 3)
        context.update(pagination_data)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }
