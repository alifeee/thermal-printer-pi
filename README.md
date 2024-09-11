# Thermal Printing

For more context on the printer, see:

- <https://github.com/alifeee/openbenches-thermal-printer?tab=readme-ov-file#escpos>

## python-escpos

The main Python library used is python-escpos: <https://github.com/python-escpos/python-escpos/>

Here is an example file:

```python
from escpos.printer import Usb

p = Usb(0x0416, 0x5011, profile="ZJ-5870")
p.text("Hello World\n")
p.barcode('4006381333931', 'EAN13', 64, 2, '', '')
p.qr("https://alifeee.co.uk")

p.close()
```

## Installation

```bash
# download files
mkdir -p /usr/alifeee
git clone git@github.com:alifeee/thermal-printer-pi.git /usr/alifeee/thermalprinter
# install python
python3 -m venv env
. env/bin/activate
pip install python-escpos[usb]
# add usb rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="5011", MODE="0666", GROUP="dialout"' > /etc/udev/rules.d/99-escpos.rules
sudo systemctl restart udev
sudo udevadm control --reload-rules && sudo udevadm trigger
# add cgi scripts
mkdir -p /var/www/cgi/do/
sudo ln -s /usr/alifeee/thermalprinter/cgi/qr /var/www/cgi/do/qr
sudo ln -s /usr/alifeee/thermalprinter/cgi/qr.cgi /var/www/cgi/do/qr.cgi
```

## Use

### Test printer

```bash
./env/bin/python test.py
```

### Print QR code

```bash
./env/bin/python qr.py -t title -url "http://raspberrypi.local/do/qr"
```
