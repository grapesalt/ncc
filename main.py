import io
import tkinter as tk
import urllib.request

from tkinter import ttk
from PIL import ImageTk, Image
from utils.image import create_image
from utils.get import get_images, get_quote
from tkinter.filedialog import askdirectory


if __name__ == "__main__":
    n = 0  # Number of quotes to generate, upto 50

    output = askdirectory()  # User preferred directory

    # Helper function
    def set_n(v):
        global n
        n = int(v)

    # Input UI

    # Display settings
    window = tk.Tk()
    window.title("Empowering Quotes Bot")
    window.geometry("600x200")
    window.minsize(600, 200)

    # Theme
    window.tk.call("source", "submodules/azure-ttk-theme/azure.tcl")
    window.tk.call("set_theme", "light")

    # Prompt text
    prompt = ttk.Label(window, text="Number of quotes to generate?")
    prompt.place(relx=0.5, rely=0.3, anchor="center")

    # Slider
    scale = tk.Scale(
        window, from_=0, to=10, label="", orient="horizontal", command=set_n
    )
    scale.place(relx=0.5, rely=0.5, anchor="center")

    # Submit button
    submit = ttk.Button(window, text="Generate", command=window.destroy)
    submit.place(relx=0.5, rely=0.7, anchor="center")

    window.mainloop()

    # Gallery UI
    for quote in get_quote()[:n]:
        # Display settings
        image_window = tk.Tk()
        image_window.title("Select image")
        image_window.geometry("616x600")
        image_window.minsize(616, 600)

        # Theme
        image_window.tk.call("source", "submodules/azure-ttk-theme/azure.tcl")
        image_window.tk.call("set_theme", "light")

        images = get_images(quote["a"], 20)
        count = -1

        aimages = []

        for image in images:
            raw_data = urllib.request.urlopen(image["url"]).read()
            im = Image.open(io.BytesIO(raw_data))
            im = im.resize((616, 500))  # Resize the image
            aimages.append(ImageTk.PhotoImage(im))

        # Add the image to the GUI
        image_label = ttk.Label(
            image_window,
            image=aimages[count],
            text=quote["a"],
            compound="top",
        )

        image_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Previous button
        def previous():
            global count
            count = (count - 1) % len(aimages)
            image_label.config(image=aimages[count], text="")

        ttk.Button(image_window, text="Previous", command=previous).grid(
            row=1, column=0, sticky="ew", columnspan=1, padx=(5, 5)
        )

        # Next button
        def next():
            global count
            count = (count + 1) % len(aimages)
            image_label.config(image=aimages[count], text="")

        ttk.Button(image_window, text="Next", command=next).grid(
            row=1, column=1, sticky="ew", columnspan=1, padx=(5, 5)
        )

        # Submit button
        ttk.Button(
            image_window,
            style="Accent.TButton",
            text="Submit",
            command=image_window.destroy,
        ).grid(row=2, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="nsew")

        next()

        image_window.mainloop()

        # Get user preferred image
        image_url = images[count]["url"]
        create_image(quote, image_url, output, (255, 235, 165))  # Create the image
