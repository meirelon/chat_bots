import requests
from PIL import Image
from io import BytesIO


def get_image(url):
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))
    return img
