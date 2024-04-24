import base64
import os
from celery import shared_task
import requests
from django.conf import settings
from stability_api.models import Request
from django.core.files.base import ContentFile


@shared_task
def add(x,y):
    print(x+y)
    return x+y

@shared_task
def generate_image(id):
    r = Request.objects.get(pk=id)
    r.status = Request.STATUS_CHOICES.WORKING
    r.save()


    api_key=os.getenv("API_KEY")or None
    endpoint = "https://api.stability.ai"
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    # api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        r.status = Request.STATUS_CHOICES.ERROR
        r.error = "Missing API Key"
        r.save()
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text":r.text
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        r.status= Request.STATUS_CHOICES.ERROR
        r.error = str(response.text)
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        img_str = image["base64"]
        full_file_name = f'image_generated_{r.pk}_{i}.png'
        img_data = ContentFile(base64.b64decode(img_str), name=full_file_name)
        r.media_file = img_data
        r.status = Request.STATUS_CHOICES.SUCCESS
        r.save()
        # with open(settings.MEDIA_ROOT+f"v1_txt2img_{i}.png", "wb") as f:
        #     f.write(base64.b64decode(image["base64"]))