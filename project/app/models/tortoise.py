# project/app/models/tortoise.py

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator  # new


#class TextSummary(models.Model):
#    url = fields.TextField()
#    summary = fields.TextField()
#    created_at = fields.DatetimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.url

class User(models.Model):
    id = fields.IntField(pk=True)
    full_name= fields.TextField()
    email= fields.TextField()
    phone=fields.TextField()

    def __str__(self):
        return self.full_name
        
class Task(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField("models.User", related_name='tasks')
    name = fields.TextField()
    completed = fields.BooleanField()
    completion_time = fields.IntField()
    rank = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    tags = fields.TextField()
    timer = fields.IntField()

    def __str__(self):
        return self.name

#SummarySchema = pydantic_model_creator(TextSummary)
UserSchema = pydantic_model_creator(User)
TaskSchema = pydantic_model_creator(Task)
