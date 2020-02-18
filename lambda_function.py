import requests

def lambda_handler(event, context):
    if not 'headers' in event or not 'Authorization' in event['headers']:
        return {
            'statusCode': 400,
            'body': 'Missing Authorization'
        }

    auth = event['headers']['Authorization']
    http_method = event['httpMethod']
    path = event['path'].split('/')

    service_id = path[1]
    passthrough_path = '/'.join(path[2:])

    service = requests.get(f'https://api.solace.cloud/api/v0/services/{service_id}', headers={'Authorization': auth}).json()
    soladmin = [item for item in service['data']['managementProtocols'] if item['name'] == 'SolAdmin'][0]
    username = soladmin['username']
    password = soladmin['password']
    url = [item for item in soladmin['endPoints'] if item['name'] == 'Secured Management'][0]['uris'][0]

    request_url = f'{url}/{passthrough_path}'
    semp_auth = requests.auth.HTTPBasicAuth(username, password)

    if http_method == 'GET':
        response = requests.get(request_url, auth=semp_auth)
    elif http_method == 'POST':
        response = requests.post(request_url, auth=semp_auth, data=event['body'])
    elif http_method == 'PUT':
        response = requests.put(request_url, auth=semp_auth, data=event['body'])
    elif http_method == 'DELETE':
        response = requests.delete(request_url, auth=semp_auth)
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid method'
        }

    return {
        'statusCode': response.status_code,
        'body': json.dumps(response.json())
    }