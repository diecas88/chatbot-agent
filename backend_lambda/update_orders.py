import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

VALID_STATUS = [
    "PENDIENTE",
    "ENVIADO",
    "ENTREGADO"
]

def lambda_handler(event, context):

    # 1. Variables obligatorias para la respuesta de Bedrock
    action_group = event.get("actionGroup")
    function = event.get("function")
    
    try:
        # 2. Extracción de parámetros desde el evento de Bedrock
        # Bedrock envía los parámetros en una lista dentro de 'parameters'
        params = {p['name']: p['value'] for p in event.get('parameters', [])}
        
        order_id = params.get("order_id")
        status = params.get("status", "").upper() # Normalizamos a mayúsculas

        # 3. Validaciones de negocio
        if not order_id or not status:
            result_text = "Faltan parámetros requeridos (order_id o status)."
        elif status not in VALID_STATUS:
            result_text = f"El estado '{status}' no es válido. Los estados permitidos son: {', '.join(VALID_STATUS)}."
        else:
            # 4. Operación en DynamoDB
            table.update_item(
                Key={"order_id": order_id},
                UpdateExpression="SET #s = :s",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":s": status}
            )
            result_text = f"Éxito: Se actualizó la orden {order_id} al estado {status}."

    except Exception as e:
        
        result_text = f"Hubo un error al intentar actualizar la orden: {str(e)}"

    # 5. Formato de respuesta requerido por Amazon Bedrock
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "function": function,
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": result_text
                    }
                }
            }
        }
    }