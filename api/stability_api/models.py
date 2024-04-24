from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
class Request(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        WORKING = "working", _("WORKING")
        SUCCESS =  "success",_("SUCCESS")
        ERROR = "error", _("ERROR")
        PENDING = "pending", _("PENDING")
        NONE = "none", _("NONE")
    # STATUS_CHOICES = (
    # ("WORKING", "working"),
    # ("SUCCESS", "success"),
    # ("ERROR","error"),
    # ("PENDING","pending")
    # )

    request_time = models.DateTimeField(auto_now=True)
    text = models.CharField(null=False, max_length=100)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    media_file = models.ImageField(null=True)
    status  = models.CharField(max_length=9,
                  choices=STATUS_CHOICES, default=STATUS_CHOICES.NONE)

    error = models.TextField(null=True
                             )

