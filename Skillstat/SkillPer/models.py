from django.db import models
from django.contrib.auth.models import User


class SkillPer(models.Model):
    """个人技能表"""
    user_id = models.CharField(max_length=3, null=False)
    skill_name = models.CharField(max_length=20, null=False)
    skill_level = models.CharField(max_length=10, null=False)
    category = models.CharField(max_length=10)
    time = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'skill_person'


# class LevelPer(models.Model):
#     """个人熟练度表"""
#     user_id = models.CharField(max_length=3, null=False)
#     name = models.CharField(max_length=10, null=False)
#
#     class Meta:
#         db_table = 'level_person'
