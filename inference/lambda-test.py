import json
from lambda_handler import lambda_handler

event = {
    "body": json.dumps({
        "review": "This movie was terrible"
    })
}

response = lambda_handler(event, None)

print(response)