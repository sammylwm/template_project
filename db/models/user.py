from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(default="", max_length=128)

    class Meta:
        table = "users"

UserSchema = pydantic_model_creator(User)