import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):

    order_id = event.get("order_id")

    response = table.get_item(
        Key={
            "order_id": order_id
        }
    )

    item = response.get("Item")

    if not item:
        return {
            "message": "Order not found"
        }

    return {
        "message": "Order found",
        "order_id": item["order_id"],
        "customer_code": item["customer_code"],
        "date_created": item["date_created"],
        "status": item["status"],
        "delivered": item["delivered"],
        "date_delivered": item["date_delivered"],
        "observations": item["observations"]
    }