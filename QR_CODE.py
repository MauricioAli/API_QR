import requests, base64, qrcode, random
from credentials import Client_Id, Client_Secret

def obtain_authentication_token(client_id, client_secret):
    url = 'https://oauth.sandbox.nequi.com/oauth2/token'
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        return None

def obtain_qr_code(token, messageID):
    url = 'https://api.sandbox.nequi.com/payments/v2/-services-paymentservice-generatecodeqr'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'x-api-key': 'AZsaFtMDFV6IENgZIZaFSa76xMOnyfwS4pUtpiaB'
    }
    
    data = {
        "RequestMessage": {
            "RequestHeader": {
                "Channel": "PQR03-C001",
                "RequestDate": "2023-07-03T20:26:12.654Z",
                "MessageID": messageID,
                "ClientID": "12345",
                "Destination": {
                    "ServiceName": "PaymentsService",
                    "ServiceOperation": "generateCodeQR",
                    "ServiceRegion": "C001",
                    "ServiceVersion": "1.2.0"
                }
            },
            "RequestBody": {
                "any": {
                    "generateCodeQRRQ": {
                        "code": "NIT_1",
                        "value": "100000",
                        "reference1": "Reference number 1",
                        "reference2": "Reference number 2",
                        "reference3": "Reference number 3"
                    }
                }
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(response)
    
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)

        qr_code_url = response_data.get('ResponseMessage', {}).get('ResponseBody', {}).get('any', {}).get('generateCodeQRRS', {}).get('codeQR')

        return qr_code_url
    else:
        print('Error obtaining QR code:', response.text)
        return None

def show_image(qr_code):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_code)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save("qr_code.png")
    qr_image.show()

Client_Id = Client_Id
Client_Secret = Client_Secret

token = obtain_authentication_token(Client_Id, Client_Secret)

if token:
    messageID = random.randint(0000000000,9999999999)
    qr_code = obtain_qr_code(token, messageID)
    show_image(qr_code)

    if qr_code:
        print('QR code URL:', qr_code)
    else:
        print('Failed to obtain the QR code.')
else:
    print('Failed to obtain authentication token.')
