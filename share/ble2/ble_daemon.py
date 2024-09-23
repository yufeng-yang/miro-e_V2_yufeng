#!/usr/bin/python3 -u

"""
Copyright (c) 2019, Douglas Otwell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import dbus
import subprocess

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor

# don't know what this is but it googles
GATT_CHARACTERISTIC_IFACE = "org.bluez.GattCharacteristic1"

# at this interval, check for pending data to send upstream
NOTIFY_TIMEOUT = 100

# these are the miro2/3 UUIDs that we have been using since miro2
# was first released
ENDPOINT_SERVICE_UUID = "ff51b30e-d7e2-4d93-8842-a7c4a57dfb07"
ENDPOINT_CHARACTERISTIC_UUID = "ff51b30e-d7e2-4d93-8842-a7c4a57dfb0a"

def encode_manuf_data(text):

	# encode string to array
	value = []
	for c in text:
		value.append(ord(c))
	return value

class EndpointAdvertisement(Advertisement):

	def __init__(self, index):

		# construct local name
		local_name = "miro3"
		serial_number = os.getenv("MIRO_SERIAL_NUMBER")
		if len(serial_number) == 10:
			print("found serial number", serial_number)
			local_name += "/" + serial_number

		# init advert
		Advertisement.__init__(self, index, "peripheral")
		self.add_local_name(local_name)
		self.include_tx_power = True
		self.add_service_uuid(ENDPOINT_SERVICE_UUID)
		self.add_manufacturer_data(0x0001, encode_manuf_data("miro3"))

class EndpointService(Service):

	def __init__(self, index):
		Service.__init__(self, index, ENDPOINT_SERVICE_UUID, True)
		self.add_characteristic(EndpointCharacteristic(self))

class EndpointCharacteristic(Characteristic):

	def __init__(self, service):

		# initialise
		self.response = ""
		self.ping_counter = 0
		self.notifying = False
		Characteristic.__init__(
				self, ENDPOINT_CHARACTERISTIC_UUID,
				["read", "write", "notify"], service)

	def encode_response(self, response):

		# encode string to dbus format
		value = []
		for c in response:
			value.append(dbus.Byte(c.encode()))
		return value

	def notify_callback(self):

		# if not notifying, end timeout
		if not self.notifying:
			return False

		# if any response is pending
		if len(self.response) > 0:

			# return line-by-line so as not to confuse receiver
			f = self.response.find('\n')
			if f == -1:
				print("    !!!", self.response, "(bad response stored, not sending...)")
			else:
				response = self.response[0:(f+1)]
				self.response = self.response[(f+1):]
				print("    >>>", response[0:-1])
				value = self.encode_response(response)
				self.PropertiesChanged(GATT_CHARACTERISTIC_IFACE, {"Value": value}, [])

		# otherwise, consider a ping
		else:

			# count ping interval
			self.ping_counter += 1
			if self.ping_counter >= 5:

				# perform a ping
				if self.SendRequest("@/ping¬"):
					return True

				# perform an async ping
				if self.SendRequest("@/async/ping¬"):
					return True

				# reset counter
				self.ping_counter = 0

		# continue timeout
		return True

	def StartNotify(self):

		# report
		print("---- start notify")

		# clear ping state on new connection
		self.SendRequest("@/system/refresh¬")

		# start notifications
		if self.notifying:
			return
		self.notifying = True
		self.add_timeout(NOTIFY_TIMEOUT, self.notify_callback)

	def StopNotify(self):

		# report
		print("---- stop notify")

		# stop notifications
		self.notifying = False

	def ReadValue(self, options):

		# we don't use this, but here's a sensible response, just say ok
		response = "@/read/ok\n"
		value = self.encode_response(response)
		print("    RRR", value)
		return value

	def WriteValue(self, value, options):

		# recover and format message
		request = ""
		for b in value:
			request += chr(int(b))
		if request[-1] != '\n':
			print(" !!!   ", request, "(malformed request received, not responding...)")
		request = request[0:-1]
		request += "¬"

		# report
		print(" <<<   ", request)

		# send request
		self.SendRequest(request)

	def SendRequest(self, request):

		# send request
		cmd = "bash -c 'cd ../ble; ./request.sh " + request + "'"
		stdout = subprocess.check_output(cmd, shell=True, text=True)

		# find response line (first line starting with '@')
		for line in stdout.splitlines():
		        if len(line) == 0:
		                continue
		        if line[0] != "@":
		                continue

			# add response to return data, with newline
		        self.response += line + "\n"
		        return True

		# no response
		return False


app = Application()
app.add_service(EndpointService(0))
app.register()

adv = EndpointAdvertisement(0)
adv.register()

try:
	app.run()
except KeyboardInterrupt:
	app.quit()
