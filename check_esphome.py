#!/usr/bin/python3

# https://nagios-plugins.org/doc/guidelines.html

# Import required libs for your plugin
import asyncio
import argparse
import aioesphomeapi

# Return codes expected by Nagios
codes = [ 'OK', 'WARNING', 'CRITICAL', 'UNKNOWN' ]

# Connect to device and get info
async def device_info():
    """Connect to an ESPHome device and get device info."""
    running_loop = asyncio.get_running_loop()

    # Establish connection
    api = aioesphomeapi.APIClient(running_loop, args.hostname, args.port, args.password)
    await api.connect(login=True)

    # Get device info
    info = await api.device_info()
    return info

# Create the argument parser
my_parser = argparse.ArgumentParser(description='Check ESPHome node')

# Add the arguments

my_parser.add_argument('hostname', metavar='<hostname>', type=str, help='The hostname of the device')
my_parser.add_argument('-P', '--port', metavar="<port>", help="Network port to connect to (defaults to 6053)", dest='port', default=6053, type=int)
my_parser.add_argument('password', metavar='<password>', type=str, help='The esphome api password')

# Execute the parse_args() method
args = my_parser.parse_args()

# Check logic starts here
loop = asyncio.get_event_loop()

try:
    data = loop.run_until_complete(device_info())
except Exception as e:
    STATUS = 2
    MESSAGE = str(e)
else:
    STATUS = 0
    MESSAGE = "name:{} mac_address:{} model:{} version:{}".format(data.name,data.mac_address,data.model,data.esphome_version)

# Print the MESSAGE for nagios
print("{} - {}".format(codes[STATUS], MESSAGE))

# Exit with status code
raise SystemExit(STATUS)
