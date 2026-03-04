# bedrock_client.py

import boto3
import json


class BedrockClient:

    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    def invoke_model(self, prompt: str) -> str:

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": 0.2,  # Low for deterministic RCA
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())

            if "content" in response_body and len(response_body["content"]) > 0:
                return response_body["content"][0]["text"]
            else:
                raise Exception("Unexpected response format from Bedrock.")

        except Exception as e:
            raise Exception(f"Error invoking Bedrock model: {e}")