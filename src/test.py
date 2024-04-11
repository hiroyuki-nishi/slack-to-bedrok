import json

escaped_string = "\\u3053\\u3093\\u306b\\u3061\\u306f\\uff01"

# Unicodeエスケープシーケンスを解読
decoded_string = escaped_string.encode('utf-8').decode('unicode-escape')

print(decoded_string)

event = {'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': '',
         'headers': {'content-length': '932', 'x-amzn-tls-version': 'TLSv1.3', 'x-forwarded-proto': 'https',
                     'x-forwarded-port': '443', 'x-forwarded-for': '54.87.253.76', 'accept': '*/*',
                     'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256',
                     'x-amzn-trace-id': 'Root=1-661660f5-2f767805654a0b077258c720',
                     'host': 'm4qoh25v2shhgcvurt7d6kjb5e0gxjnv.lambda-url.us-east-1.on.aws',
                     'content-type': 'application/json', 'x-slack-request-timestamp': '1712742645',
                     'x-slack-signature': 'v0=0e0107a0f0689efae9bea499fdf5e83be383e4f84b46c20dbc18ee377fd0fa70',
                     'accept-encoding': 'gzip,deflate', 'user-agent': 'Slackbot 1.0 (+https://api.slack.com/robots)'},
         'requestContext': {'accountId': 'anonymous', 'apiId': 'm4qoh25v2shhgcvurt7d6kjb5e0gxjnv',
                            'domainName': 'm4qoh25v2shhgcvurt7d6kjb5e0gxjnv.lambda-url.us-east-1.on.aws',
                            'domainPrefix': 'm4qoh25v2shhgcvurt7d6kjb5e0gxjnv',
                            'http': {'method': 'POST', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '54.87.253.76',
                                     'userAgent': 'Slackbot 1.0 (+https://api.slack.com/robots)'},
                            'requestId': '98141eec-801e-41af-98f6-f93e59c487c1', 'routeKey': '$default',
                            'stage': '$default', 'time': '10/Apr/2024:09:50:45 +0000', 'timeEpoch': 1712742645164},
         'body': '{"token":"6kvb23KEFPjfOlqF1DBkZpSR","team_id":"T06TNMM61HS","api_app_id":"A06TDKPEKL6","event":{"user":"U06TL4EGLMR","type":"app_mention","ts":"1712742644.805489","client_msg_id":"5dc90b12-a16d-476b-b4ee-fd90b1c385ef","text":"<@U06TYUGNYAD> \\u3053\\u3093\\u306b\\u3061\\u306f\\uff01","team":"T06TNMM61HS","blocks":[{"type":"rich_text","block_id":"I\\/yel","elements":[{"type":"rich_text_section","elements":[{"type":"user","user_id":"U06TYUGNYAD"},{"type":"text","text":" \\u3053\\u3093\\u306b\\u3061\\u306f\\uff01"}]}]}],"channel":"C06TDJP9B6J","event_ts":"1712742644.805489"},"type":"event_callback","event_id":"Ev06TQ8MNFQU","event_time":1712742644,"authorizations":[{"enterprise_id":null,"team_id":"T06TNMM61HS","user_id":"U06TYUGNYAD","is_bot":true,"is_enterprise_install":false}],"is_ext_shared_channel":false,"event_context":"4-eyJldCI6ImFwcF9tZW50aW9uIiwidGlkIjoiVDA2VE5NTTYxSFMiLCJhaWQiOiJBMDZUREtQRUtMNiIsImNpZCI6IkMwNlRESlA5QjZKIn0"}',
         'isBase64Encoded': False}
body = json.loads(event['body'])
print(body)
