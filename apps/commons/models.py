import uuid
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Bank(BaseModel):
    name = models.CharField(max_length=50)
