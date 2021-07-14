# check_esphome


Nagios plugin to check availability of [ESPHome](https://esphome.io) devices. Checks if the ESPHome device is online

## Installation

The installation requires Python 3.

I usually install additional plugins under `/usr/local/nagios/libexec`.

```
mkdir -p /usr/local/nagios/libexec
cd /usr/local/nagios/libexec
wget https://raw.githubusercontent.com/mdiazgoncalves/check_esphome/main/check_esphome.py
chmod +x check_esphome.py
```

The [aioesphomeapi](https://github.com/esphome/aioesphomeapi) module is required.

It can be installed using:

```
pip3 install aioesphomeapi
```

## Parameters

```
usage: check_esphome.py [-h] [-P <port>] <hostname> <password>

optional arguments:
  -h, --help            show this help message and exit
  <hostname>
                        The hostname of the ESPHome device
  <password>
                        The device ESPHome api password
  -P <port>, --port <port>
                        Network port to connect to (defaults to 6053)
```

## Support

Feel free to submit any issues and PR's'.

## License

The project is licensed under GPL license. Happy monitoring.
