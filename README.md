## Bots for VK and Telegram

The presented bots for Telegram and VKontakte communicate with the user using Dialogflow.

## Launch

Download the code from [Github](https://github.com/Sharipat/dvmn-support-bot)

Install dependencies with the command

```
  pip install -r requirements.txt
  ```

In the root of the folder, create a file ```.env```, in which write

```BOT_TOKEN``` - the token of your bot in Telegram from [BotFather](https://telegram.me/BotFather)

```CHAT_ID``` - ID for chatting with a bot in Telegram [userinfobot](https://telegram.me/userinfobot)

```PROJECT_ID``` - Project ID specified in the agent properties in Dialogflow

```JSON_PATH``` - path to the json file with questions for the bot, by default ```questions.json```

```GOOGLE_APPLICATION_CREDENTIALS``` - path to the json file with the secret key, example of creation
via [link](https://cloud.google.com/docs/authentication/getting-started)

```VK_ACESS_TOKEN``` - API key for your VKontakte group, located in the “Working with API” section

Launch the bot with the command

**In contact with**

  ```
   python3 vk_bot.py
  ```

**Telegram**

  ```
   python3 tg_bot.py
  ```

To train bots with new phrases, use the script:

  ```
   python3 dialogflow_intent_functions.py
  ```

## Example of bots

### Bot in Telegram

[Link to bot](https://t.me/shdvmnsupportbot)

<img src='screenshots/tg_bot.gif' alt="Vk bot" width="455" height="401"/>

### VKontakte bot

[Link to bot](https://vk.com/im?sel=-207140008)

<img src='screenshots/vk_bot.gif' alt="Vk bot" width="417" height="389"/>

## Project goals

The code is written for educational purposes - this is a lesson in the course on Python and web development on the site [Devman](https://dvmn.org).