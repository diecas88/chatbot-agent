import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):

    # Extraemos info necesaria para la respuesta obligatoria
    action_group = event.get("actionGroup")
    function = event.get("function")

    try:
        order_id = None

        # Extracción de parámetros
        if "parameters" in event:
            for param in event["parameters"]:
                if param["name"] == "order_id":
                    order_id = param["value"]
        elif "requestBody" in event:
            body = event.get("requestBody", {}).get("content", {}).get("application/json", {})
            order_id = body.get("order_id")
        else:
            order_id = event.get("order_id")

        print("order_id:", order_id)

        if not order_id:
            result = {"error": "No hay order id"}
        else:
            response = table.get_item(Key={"order_id": order_id})
            result = response.get("Item", {"message": "Orden no encontrada"})


        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": action_group,
                "function": function,
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(result, default=str) 
                        }
                    }
                }
            }
        }

    except Exception as e:
        
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": action_group,
                "function": function,
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": f"Error procesando la solicitud: {str(e)}"
                        }
                    }
                }
            }
        }