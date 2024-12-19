"""thermally print a qr code"""

import argparse
from escpos.printer import Usb


def main(
    message: str,
):
    p = Usb(0x0416, 0x5011, profile="ZJ-5870")

    p.set(
        align="center",
        font="a",
        bold=True,
        double_height=True,
        double_width=True,
        invert=False,
    )
    p.text(message)

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
        "message",
        help="message to print",
        type=str,
    )
    args = parser.parse_args()
    main(args.message)
