from dotenv import load_dotenv
import os

# import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from azure.ai.projects.models import MCPTool



def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('PROJECT_ENDPOINT')
        agent_name = os.getenv('AGENT_NAME')
        model_deployment = os.getenv('MODEL_DEPLOYMENT')
        language_endpoint = os.getenv('LANGUAGE_ENDPOINT') or os.getenv('AZURE_AI_SERVICE_ENDPOINT')
        if not model_deployment:
            raise ValueError('Set MODEL_DEPLOYMENT in .env to your Azure OpenAI model deployment name.')
        if not language_endpoint:
            raise ValueError(
                'Set LANGUAGE_ENDPOINT in .env to your Azure AI Language/Cognitive Services endpoint.'
            )

        credential = DefaultAzureCredential()
        
        # Get project client
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=credential,
            allow_preview=True
        )

        language_token = credential.get_token("https://cognitiveservices.azure.com/.default")
        
        mcp_tool = MCPTool(
            server_label="azure-language",
            server_url=f"{language_endpoint.rstrip('/')}/language/mcp?api-version=2025-11-15-preview",
            headers={"Authorization": f"Bearer {language_token.token}"},
            require_approval="never",
        )
        
        
        # Get an OpenAI client
        openai_client = project_client.get_openai_client()
        

        
        # Use the agent to get a response
        prompt = input("User prompt: ")
        response = openai_client.responses.create(
            model=model_deployment,
            instructions=f"You are {agent_name}, an assistant that uses Azure AI Language when text analysis is needed.",
            input=[{"role": "user", "content": prompt}],
            tools=[mcp_tool.as_dict()],
        )

        print(f"{agent_name}: {response.output_text}")


        
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
