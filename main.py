from utils.get import get_images, get_quote
from utils.image import create_image

if __name__ == "__main__":
    n = 5  # Number of quotes to generate, upto 50

    for quote in get_quote()[:n]:
        image_url = get_images(quote["a"])[0]["url"]
        create_image(quote, image_url, (255, 255, 255))
