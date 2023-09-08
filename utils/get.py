"""
name: generate.py
author: Aditya Chaturvedi <aditya.chaturvedi1608@gmail.com>
license: MIT

Get images from OpenVerse and quotes from zenquotes.io.
All images have creative common license.
"""

import requests


def get_images(author: str, n: int = 10):
    """
    Get images of the author

    Parameters
    ----------
    author: str
        The name of the author of the quote
    n: int
        The number of images to be returned
    """

    # Openverse API
    IMAGES_URL = (
        f"https://api.openverse.engineering/v1/images/?q={author}&page_size={n}"
    )

    res = requests.get(IMAGES_URL)
    images = res.json()["results"]

    return images


def get_quote():
    """
    Get random quotes
    """
    API_URL = "https://zenquotes.io/api/quotes"
    res = requests.get(API_URL)

    quote = res.json()

    return quote
