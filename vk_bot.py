import logging
import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_intent_functions import detect_intent_texts

logger = logging.getLogger('vk_support_bot')


def handle_vk_messages(event, project_id, vk_ru_api):
    response = detect_intent_texts(project_id, f'vk-{event.user_id}', event.text)
    if not response.query_result.intent.is_fallback:
        message = response.query_result.fulfillment_text
        vk_ru_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000))


def main():
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    vk_token = os.getenv('VK_ACESS_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_ru_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_vk_messages(event, project_id, vk_ru_api)


if __name__ == '__main__':
    main()
