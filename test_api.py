import httpx

# The API URL you provided
url = "https://preassembly-referencing-api-prod.eu-de-1.icp.infineon.com//simple_search?user=None&Basistypen=P5151E&modus=hfgst&key=nfh848h_Su843hTfhg_r82z&id=1620496430&PA_number=69000000&loc=All&milestone=0&differ_pa_baunumbers=False"

# Disable SSL verification for development
response = httpx.get(url, verify=False)

print("Status code:", response.status_code)
print("Response JSON:")
print(response.json())
