"""thermally print a qr code"""

import argparse
from escpos.printer import Usb
from escpos.exceptions import ImageWidthError


def main(
    url: str,
    title: str,
):
    p = Usb(0x0416, 0x5011, profile="ZJ-5870")

    if title != "":
        p.set(
            align="center",
            bold=True,
            double_height=True,
            double_width=True,
        )
        p.text(title)

    size = 16
    while True:
        try:
            p.qr(
                url,
                size=size,  # pixels
                ec=1,  # error correction
                native=False,  # do natively (doesn't work I think)
                center=True,
            )
            break
        except ImageWidthError:
            size -= 1
        if size == 1:
            break

    p.set(normal_textsize=True)
    p.textln(url)
    p.ln(3)
    p.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "--url", help="url to qr", required=True, type=str)
    parser.add_argument("-t", "--title", help="title of QR code", type=str)
    args = parser.parse_args()
    main(args.url, args.title)
