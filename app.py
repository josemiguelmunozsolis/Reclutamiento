from authlib.integrations.requests_client import OAuth2Session
import requests
import json
###Configuración OAuth2###
client_id = '65b6c90bc86df184047084904db99264bd6bf2b7a67aea4539caa3307231d445'
client_secret = 'e46faf944ccaddbee6e1fca2eb0f702cb9126972bae7085a57726e5b75c80385'
authorization_endpoint = 'https://www.centry.cl/oauth/token'
token_endpoint = 'https://www.centry.cl/oauth/token'
scope = "public read_orders write_orders read_products write_products read_integration_config write_integration_config read_user write_user read_webhook write_webhook read_warehouses write_warehouses"
code = "f4f9a779293b3e78f3b0fab17a3d2d79a2afa75ce67357113e683dfd40322626"
###Fin configuración OAuth2###

###Conexión OAuth2###
client = OAuth2Session(client_id, client_secret,redirect_uri="urn:ietf:wg:oauth:2.0:oob", scope=scope)
uri, state = client.create_authorization_url(authorization_endpoint, grant_type="authorization_code" , code=code)
token = client.fetch_token(token_endpoint ,state=state)
client = OAuth2Session(client_id, client_secret, token=token)
###Fin Conexión OAuth2###

headers = {
  'Authorization': 'Bearer ' + token['access_token'],
  'Content-Type': 'application/json;charset=utf-8',
}

url = " https://www.centry.cl/conexion/v1/products/5f8fa2e21e390148a0e93604.json"
payload = {}
response = requests.request("GET", url, headers=headers, data = payload)
response = response.text.encode('utf8')
prePayload = json.loads(response.decode('utf-8'))["variants"]

#Tercer requerimiento, se agregan 50 ítmes a todas la variantes 
for variants in prePayload:
    variants["quantity"] = 50
    
url = "https://centry.cl/conexion/v1/products/5f8fa2e21e390148a0e93604.json"

#Primer y segundo requerimeinto, se cambia el título del ítem y se cambia el precio
payload = {
    "name" : "José Miguel Muñoz Solís",
    "price_compare": 9990,
    "variants": prePayload
}

payload = json.dumps(payload).encode('utf-8')
response = requests.request("PUT", url, headers=headers, data = payload)