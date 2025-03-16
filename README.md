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

## Using Flask server

### nginx configuration

```nginx
server {
                listen 80 default_server;
                listen [::]:80 default_server;

                index index.html;

                server_name _;

                # return homepage even if Flask server is off
                location = / {
                        alias /usr/alifeee/thermalprinter/templates/;
                        try_files index.html =404;
                }

                # otherwise use Flask server
                location / {
#                       root /var/www/html;
#                       try_files $uri $uri/ =404;

                        proxy_pass http://localhost:5000;
                        proxy_redirect off;
                        proxy_set_header Host $http_host;
                        proxy_set_header X-Real-IP $remote_addr;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_read_timeout 900;
                        client_max_body_size 20M;
                }

                location /do/ {
                        root /var/www/cgi;
                        index index.cgi;
                        fastcgi_intercept_errors on;
                        include fastcgi_params;
                        fastcgi_param SCRIPT_FILENAME /var/www/cgi$fastcgi_script_name;
                        fastcgi_pass unix:/var/run/fcgiwrap.socket;
                }
        }
```

### test for debugging

./env/bin/flask --app server run --host 0.0.0.0

### enable service

```bash
# install modules
python3 -m venv env
./env/bin/pip install -r requirements.txt

# enable systemd
sudo cp thermalprinter.service /etc/systemd/system/thermalprinter.service
sudo systemctl enable thermalprinter.service
sudo systemctl start thermalprinter.service
sudo systemctl status thermalprinter.service
```
