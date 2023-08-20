import random
from time import gmtime, strftime
import requests
from PIL import Image, ImageFont, ImageDraw
import textwrap
import urllib.request

def generate_image(author):
    API_URL = f'https://api.openverse.engineering/v1/images/?q={author}'
    res = requests.get(API_URL)

    return res.json()['results']

def generate_quote():
    API_URL = 'https://zenquotes.io/api/quotes'
    res = requests.get(API_URL)


    quote = res.json()

    return quote

def create_image(quote, image_url, color):
    IMAGE_NAME = f'qimage-{strftime("%H:%M:%S", gmtime())}.jpg'
    WIDTH = 1080
    HEIGHT = 1350
    img = Image.new(mode='RGB', size = (WIDTH, HEIGHT), color=color)
    urllib.request.urlretrieve(image_url, IMAGE_NAME)

    qimg = Image.open(IMAGE_NAME)
    qimg = qimg.resize((1080, 877))

    temp = Image.new(mode='RGBA', size=(1080, 877), color=(0, 0, 0, 0))
    temp.putalpha = 0
    mask = Image.open('mask.png')

    qimg = qimg.convert('RGBA')
    qimg = Image.alpha_composite(qimg, mask)

    img.paste(qimg, (0, 0))
    afont = ImageFont.truetype('Montserrat-Bold.ttf', 50)
    qfont = ImageFont.truetype('Montserrat-Regular.ttf', 58)
    ImageDraw.fontmode = 'L'
    ImageDraw.Draw(img).text((382, 719), quote['a'], (0, 0, 0), font=afont, anchor='mm')
    ImageDraw.Draw(img).text((131, 833), textwrap.fill(quote['q'], 30), (0, 0, 0), font=qfont, anchor='mm')
    img.save('quote.jpg')

    


if __name__ == '__main__':
    q = random.choice(generate_quote())
    url = generate_image(q['a'])[0]['url']

    create_image(q, url, (255, 255, 255))