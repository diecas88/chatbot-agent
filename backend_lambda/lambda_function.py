import json
import boto3
import os


client = boto3.client(service_name="bedrock-agent-runtime", region_name="us-east-2")
AGENT_ID = os.getenv('AGENT_ID')
AGENT_ALIAS = os.getenv('AGENT_ALIAS')



def lambda_handler(event, context):
    try:
       
        body = json.loads(event.get("body", "{}"))
        user_input = body.get("query")
        
        session_id = body.get("sessionId", "session_123") 

        if not user_input:
            return response(400, {"error": "Falta el query del usuario"})

        # Invocación al Agente de Bedrock
        agent_res = client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS,
            sessionId=session_id,
            inputText=user_input
        )

        # Procesar la respuesta (Bedrock responde en chunks/pedazos)
        full_answer = ""
        for event in agent_res.get("completion"):
            chunk = event.get("chunk")
            if chunk:
                full_answer += chunk.get("bytes").decode("utf-8")

        return response(200, {
            "answer": full_answer,
            "sessionId": session_id
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return response(500, {"error": str(e)})

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }