#!../env/bin/python
# test locally
#   printf "text=alfie" | ./text.py
# test with curl
#   curl localhost/do/printer/text.py -d "text=alfie"

import os
import sys
from urllib.parse import parse_qs
from pprint import pprint
from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError, DeviceNotFoundError

def error(msg):
  print("Content-type: text/plain")
  print("")
  print("error!")
  print(msg)

form_urlencoded = sys.stdin.read()
data = parse_qs(form_urlencoded)

text = data.get("text", [])
if text == []:
  error('"text" is empty')
  sys.exit(1)

text = text[0]

print("printing text!", file=sys.stderr)
print(text, file=sys.stderr)

p = Usb(0x0416, 0x5011, profile="ZJ-5870")

try:
  # https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.set
  p.set(
    align = data.get("align", "center"),
    font = data.get("font", "a"),
    bold = data.get("bold", False),
    underline = data.get("underline", False),
    double_height = data.get("double_height", False),
    double_width = data.get("double_width", False),
    invert = data.get("invert", False),
    flip = data.get("flip", False),
  )

  p.text(text)
  p.ln()

  if data.get("after_padding", True):
    p.ln()
    p.ln()
    p.ln()

except (USBNotFoundError, DeviceNotFoundError) as ex:
  error("USB thermal printer not found... is it plugged in?")
  sys.exit(1)
