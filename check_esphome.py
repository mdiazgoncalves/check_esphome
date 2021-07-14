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
    api = aioesphomeapi.APIClient(running_loop, args.Address, args.Port, args.Password)
    await api.connect(login=True)

    # Get device info
    info = await api.device_info()
    print(info)
    return info

# Create the argument parser
my_parser = argparse.ArgumentParser(description='Check ESPHome node')

# Add the arguments
my_parser.add_argument('Address', metavar='address', type=str, help='The host ip address')
my_parser.add_argument('Port', metavar='port', type=str, help='The service port number to connect to')
my_parser.add_argument('Password', metavar='password', type=str, help='The esphome api password')

# Execute the parse_args() method
args = my_parser.parse_args()

# Check logic starts here
loop = asyncio.get_event_loop()

try:
    data = loop.run_until_complete(device_info())
except Exception as e:
    status = 2
    message = str(e)
else:
    status = 0
    message = "name:{} mac_address:{} model:{} version:{}".format(data.name,data.mac_address,data.model,data.esphome_version)

# Print the message for nagios
print("{} - {}".format(codes[status], message))

# Exit with status code
raise SystemExit(status)
