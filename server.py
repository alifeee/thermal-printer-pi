"""a server to listen to printing requests
"""

import os
import sys
from flask import Flask, render_template, request
from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError, DeviceNotFoundError, ImageWidthError

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


#  return "<p>Hello world</p>"


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

    print(image)

    image.save("/tmp/89175891.png")

    p = Usb(0x0416, 0x5011, profile="ZJ-5870")
    p.image(
        "/tmp/89175891.png",
        center=True,
    )

    p.ln(4)
    p.close()

    return "done maybe"
