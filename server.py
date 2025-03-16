
"""a server to listen to printing requests
"""

import os
import sys
from io import BytesIO
import cairosvg
from flask import Flask, render_template, request, send_file
from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError, DeviceNotFoundError, ImageWidthError
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/status_image")
def status_image():
    try:
        p = Usb(0x0416, 0x5011, profile="ZJ-5870")
        p.set(normal_textsize=True)
        p.close()
        colour = "green"
    except (USBNotFoundError, DeviceNotFoundError):
        colour = "red"

    img = Image.new("RGB", [10, 10], colour)
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")


@app.route("/printtext", methods=["POST"])
def text():
    form = request.form
    text = form.get("text", "")

    try:
        # https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.set
        p = Usb(0x0416, 0x5011, profile="ZJ-5870")

        p.set(
            align=form.get("align", "center"),
            font=form.get("font", "a"),
            bold=form.get("bold", False),
            underline=form.get("underline", False),
            double_height=form.get("double_height", False),
            double_width=form.get("double_width", False),
            invert=form.get("invert", False),
            flip=form.get("flip", False),
        )

        p.text(text)
        p.ln()

        if form.get("after_padding", True):
            p.ln()
            p.ln()
            p.ln()

    except (USBNotFoundError, DeviceNotFoundError):
        p.close()
        return "USB thermal printer not found... is it plugged in?"

    p.close()
    return f"done! printed:<br> {text}"


@app.route("/printqr", methods=["POST"])
def qr():
    form = request.form
    link = form.get("link", "")

    try:
        # https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.qr
        p = Usb(0x0416, 0x5011, profile="ZJ-5870")
        size = 16
        while True:
            try:
                p.qr(
                    link,
                    size=size,
                    ec=1,
                    native=False,
                    center=False,
                )
                break
            except ImageWidthError:
                size -= 1
            if size == 1:
                break
        p.set(normal_textsize=True)
        p.textln(link)
        p.ln(3)
        p.close()

    except (USBNotFoundError, DeviceNotFoundError):
        p.close()
        return "USB thermal printer not found... is it plugged in?"

    return f"done! printed:<br> {link}"


@app.route("/printimage", methods=["POST"])
def image():
    form = request.form
    image = request.files["image"]

    if image.content_type == "image/svg+xml":
        out = BytesIO()
        cairosvg.svg2png(file_obj=image, write_to=out)
        image = out

    # pillow
    try:
        img = Image.open(image)
    except UnidentifiedImageError:
        return (
            "couldn't open image with PIL <br>"
            f"I see the filetype is {image.content_type}. Is it a weird filetype? <br>"
            "I'm expecting image/png or image/jpeg or image/svg+xml or something like that"
        )

    # max width of 384 px
    if img.width > 384 or img.height > 1100:
        img.thumbnail([384, 1100])

    try:
        p = Usb(0x0416, 0x5011, profile="ZJ-5870")
        p.ln()
        p.image(
            img,
            center=True,
            fragment_height=500,
        )

        p.ln(4)
        p.close()
    except (USBNotFoundError, DeviceNotFoundError):
        p.close()
        return "USB thermal printer not found... is it plugged in?"

    return "done maybe !"
