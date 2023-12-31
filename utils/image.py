"""
name: generate.py
author: Aditya Chaturvedi <aditya.chaturvedi1608@gmail.com>
license: MIT

Create final image with quote and author image
"""

import textwrap
import urllib.request

from os import makedirs, path
from tempfile import gettempdir
from time import gmtime, strftime
from PIL import Image, ImageFont, ImageDraw


def create_image(quote: str, image_url: str, output: str, color: tuple) -> None:
    """
    Create the quote image

    Parameters
    ----------

    quote: str
    image_url: str
    color: tuple
    """

    TIMESTAMP = strftime("%H:%M:%S", gmtime())

    # Temporary image. Stored in temporary directory
    T_IMG_NAME = path.join(gettempdir(), f"qimage-{TIMESTAMP}.jpg")

    # Image attributes
    WIDTH = 1080
    HEIGHT = 1350

    # Create new image
    img = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=color)

    # Download the author image
    urllib.request.urlretrieve(image_url, T_IMG_NAME)

    # Resize the author image to fit the generated image
    qimg = Image.open(T_IMG_NAME)
    qimg = qimg.resize((1080, 877))

    mask = Image.open("assets/images/mask.png")

    # Convert the image to RGBA so that we can composite the mask and the image
    qimg = qimg.convert("RGBA")
    qimg = Image.alpha_composite(qimg, mask)

    # Add the image
    img.paste(qimg, (0, 0))

    # Load fonts
    afont = ImageFont.truetype(
        "assets/fonts/Montserrat-Bold.ttf", 50
    )  # Font for the author
    qfont = ImageFont.truetype(
        "assets/fonts/Montserrat-Regular.ttf", 58
    )  # Font for the quote

    ImageDraw.fontmode = "L"  # Enable anti-aliasing for fonts

    ImageDraw.Draw(img).text(
        (382, HEIGHT / 2), quote["a"], (0, 0, 0), font=afont
    )  # Add author
    ImageDraw.Draw(img).text(
        (131, 833), textwrap.fill(quote["q"], 30), (0, 0, 0), font=qfont
    )  # Add quote

    # Save the final image

    if not path.exists(output):
        makedirs(output)

    img.save(path.join(output, f'quote-{quote["a"]}-{TIMESTAMP}.jpg'))
