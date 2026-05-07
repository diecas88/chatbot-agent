import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

VALID_STATUS = [
    "PENDIENTE",
    "ENVIADO",
    "ENTREGADO"
]

def lambda_handler(event, context):

    order_id = event.get("order_id")
    status = event.get("status")

    if status not in VALID_STATUS:
        return {
            "message": "status no existe"
        }

    table.update_item(
        Key={
            "order_id": order_id
        },
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={
            "#s": "status"
        },
        ExpressionAttributeValues={
            ":s": status
        }
    )

    return {
        "message": f"Se actualizó la orden {order_id} a {status}"
    }