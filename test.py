from escpos.printer import Usb

p = Usb(0x0416, 0x5011, profile="ZJ-5870")
p.text("Hello World\n")
p.barcode('4006381333931', 'EAN13', 64, 2, '', '')
p.qr("https://alifeee.co.uk")

p.close()
