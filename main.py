import urllib.request
from utils.get import get_images, get_quote
from utils.image import create_image
from PIL import ImageTk, Image
import io
import tkinter as tk

if __name__ == "__main__":
    n = 0  # Number of quotes to generate, upto 50

    def set_n(v):
        global n
        n = int(v)

    window = tk.Tk()
    window.title("Empowering Quotes Bot")
    window.geometry("600x200")
    window.minsize(600, 200)

    prompt = tk.Label(text="Number of quotes to generate?")
    prompt.place(relx=0.5, rely=0.3, anchor="center")

    scale = tk.Scale(window, from_=0, to=10, orient="horizontal", command=set_n)
    scale.place(relx=0.5, rely=0.5, anchor="center")

    submit = tk.Button(window, text="Generate", command=window.destroy)
    submit.place(relx=0.5, rely=0.7, anchor="center")

    window.mainloop()

    for quote in get_quote()[:n]:
        image_window = tk.Tk()
        image_window.title("Select image")
        image_window.geometry("600x800")
        image_window.minsize(600, 700)

        images = get_images(quote["a"], 20)
        count = -1

        aimages = []
        for image in images:
            raw_data = urllib.request.urlopen(image["url"]).read()
            im = Image.open(io.BytesIO(raw_data))
            im.thumbnail((600, 600))
            aimages.append(ImageTk.PhotoImage(im))

        def left():
            global count
            count = (count - 1) % len(aimages)
            image_label.config(image=aimages[count], text="")

        def right():
            global count
            count = (count + 1) % len(aimages)
            image_label.config(image=aimages[count], text="")

        image_label = tk.Label(
            image_window,
            image=aimages[count],
            text=quote['a'],
            compound="top",
        )
        image_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        tk.Button(image_window, text="previous", command=left).grid(
            row=1, column=0, sticky="ew"
        )
        tk.Button(image_window, text="next", command=right).grid(
            row=1, column=1, sticky="ew"
        )
        
        tk.Button(image_window, text="submit", command=image_window.destroy).grid(
            row=2, column=1, sticky="ew"
        )

        right()

        image_window.mainloop()

        image_url = get_images(quote["a"])[count]["url"]
        create_image(quote, image_url, (255, 235, 165))
