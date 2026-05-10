from dotenv import load_dotenv
import os

# import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        language_endpoint = os.getenv('LANGUAGE_ENDPOINT') or os.getenv('AZURE_AI_SERVICE_ENDPOINT')
        if not language_endpoint:
            raise ValueError(
                'Set LANGUAGE_ENDPOINT in .env to your Azure AI Language/Cognitive Services endpoint.'
            )


        # Create client using endpoint
        credential = DefaultAzureCredential()
        ai_client = TextAnalyticsClient(endpoint=language_endpoint, credential=credential)


        # Analyze each text file in the reviews folder
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        reviews_folder = os.path.join(cur_dir, 'reviews')
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))


            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))



            # Get PII
            pii_result = ai_client.recognize_pii_entities(documents=[text])[0]
            pii_entities = pii_result.entities
            if len(pii_entities) > 0:
                print("\nPII Entities")
                for pii_entity in pii_entities:
                    print('\t{} ({})'.format(pii_entity.text, pii_entity.category)) 
                print("Redacted Text:\n {}".format(pii_result.redacted_text))



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
