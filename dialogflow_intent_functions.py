import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id,  text, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    print("Query text:", response.query_result.query_text)
    print("Fulfillment text:", response.query_result.fulfillment_text)
    return response


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    response = client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    return response


def save_questions(json_path):
    with open(json_path, "r") as json_file:
        file_contents = json.load(json_file)
    return file_contents


def main():
    load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    json_path = os.getenv('JSON_PATH', 'questions.json')
    questions = save_questions(json_path)
    for display_name, question in questions.items():
        training_phrases_parts = question['questions']
        message_texts = question['answer']
        create_intent(project_id, display_name, training_phrases_parts, [message_texts])


if __name__ == '__main__':
    main()
