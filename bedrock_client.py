# bedrock_client.py

import boto3
import json
import os


class BedrockClient:

    def __init__(self):

        # Read AWS credentials from environment variables
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        # Create Bedrock runtime client
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        # Claude Haiku model (fast + cheap)
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    def invoke_model(self, prompt: str) -> str:

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": 0.2,
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