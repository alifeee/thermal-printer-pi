from escpos.printer import Usb
from escpos.exceptions import ImageWidthError

def main(
	url: str,
	title: str,
):
	p = Usb(0x0416, 0x5011, profile="ZJ-5870")

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
				"https://alifeee.co.uk",
				size=size, # pixels
				ec=1, # error correction
				native=False, # do natively (doesn't work I think)
				center=True,
			)
			break
		except ImageWidthError as e:
			size -= 1
		if size == 1:
			break

	p.set(normal_textsize=True)
	p.textln(url)
	p.ln(3)
	p.close()

if __name__ == "__main__":
  main(
		"https://alifeee.co.uk",
		"alifeee's website"
	)
