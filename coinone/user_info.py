import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time

ACCESS_TOKEN = '0fd27ac4-a404-4bb1-b052-f05d6b533944'
SECRET_KEY = 'ac1873c7-fc35-4274-b94a-771e7a17505a'

URL = 'https://api.coinone.co.kr/v1/order/limit_orders/'
PAYLOAD = {
  "access_token": ACCESS_TOKEN,
}

def get_encoded_payload(payload):
  payload[u'nonce'] = int(time.time()*1000)

  dumped_json = json.dumps(payload)
  encoded_json = base64.b64encode(dumped_json)
  return encoded_json

def get_signature(encoded_payload, secret_key):
  signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
  return signature.hexdigest()

def get_response(url, payload):
  encoded_payload = get_encoded_payload(payload)
  headers = {
    'Content-type': 'application/json',
    'X-COINONE-PAYLOAD': encoded_payload,
    'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
  }
  http = httplib2.Http()
  response, content = http.request(URL, 'POST', headers=headers, body=encoded_payload)
  return content

def get_result():
  content = get_response(URL, PAYLOAD)
  content = json.loads(content)

  return content

if __name__   == "__main__":
    print get_result()
