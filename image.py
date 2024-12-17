"""thermally print a qr code"""

import argparse
from escpos.printer import Usb
from escpos.exceptions import ImageWidthError


def main(
    image_fname: str,
    name: str,
):
    p = Usb(0x0416, 0x5011, profile="ZJ-5870")

    p.image(
        image_fname,
        center=True,
    )
    p.ln()
    p.ln()
    p.ln()
    p.ln()

    p.set(
        align="center",
        font="a",
        bold=True,
        double_height=True,
        double_width=True,
        invert=False,
    )
    p.text(name)

    p.ln()
    p.ln()
    p.ln()
    p.ln()
    p.ln()
    p.ln()

    p.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--image-fname",
        help="filename of image to print",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-n",
        "--name",
        help="name",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.image_fname, args.name)
