#!/usr/bin/python3

# https://nagios-plugins.org/doc/guidelines.html

# Import required libs for your plugin
import argparse
import asyncio

import aioesphomeapi

# Return codes expected by Nagios
codes = ['OK', 'WARNING', 'CRITICAL', 'UNKNOWN']


# Connect to device and get info
async def device_info():
    """Connect to an ESPHome device and get device info."""

    # Establish connection
    if args.auth == "password":
        api = aioesphomeapi.APIClient(args.hostname, args.port, args.password)
    else:
        api = aioesphomeapi.APIClient(args.hostname, args.port, None, noise_psk=args.password)
    await api.connect(login=True)

    # Get device info
    info = await api.device_info()
    return info

# Create the argument parser
my_parser = argparse.ArgumentParser(description='Check ESPHome node')

# Add the arguments

my_parser.add_argument('hostname', metavar='<hostname>', type=str, help='The hostname of the device')
my_parser.add_argument('-P', '--port', metavar="<port>", help="Network port to connect to (defaults to 6053)", dest='port', default=6053, type=int)
my_parser.add_argument('-a', '--auth', metavar="<auth>", help="Auth type 'password' or 'encryption' (defaults to password)", dest='auth', default="password", type=str)
my_parser.add_argument('password', metavar='<password>', type=str, help='The esphome api password')

# Execute the parse_args() method
args = my_parser.parse_args()

# Check logic starts here

try:
    data = asyncio.run(device_info())
except Exception as e:
    STATUS = 2
    MESSAGE = str(e)
else:
    STATUS = 0
    MESSAGE = f"name:{data.name} mac_address:{data.mac_address} model:{data.model} version:{data.esphome_version}"

# Print the MESSAGE for nagios
print(f"{codes[STATUS]} - {MESSAGE}")

# Exit with status code
raise SystemExit(STATUS)
