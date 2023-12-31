import ssl
import sys

import json
import urllib.request

import paho.mqtt.client

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='#', qos=2)

def on_message(client, userdata, message):
	msg = message.payload
	decodedmsg = msg.decode()
	try:
		result = json.loads(decodedmsg)
	except:
		print('------------------------------')
		print("A JSON Decode Error Occured... message isn't JSON")
		print('------------------------------')
		result = decodedmsg
	finally:
		print('------------------------------')
		print('topic: %s' % message.topic)
		print('payload: %s' % msg)
		print('decoded: %s' % decodedmsg)
		print('json: %s' % result)
		print('qos: %d' % message.qos)

def loop():
	client = paho.mqtt.client.Client()
	# client.username_pw_set('[username]', '[password]')
	client.on_connect = on_connect
	client.on_message = on_message
	# client.tls_set('/etc/ssl/certs/DST_Root_CA_X3.pem', tls_version=ssl.PROTOCOL_TLSv1_2)
	client.connect(host='10.1.5.254', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	loop()
	sys.exit(0)