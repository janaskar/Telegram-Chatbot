# Telegram Reminder Bot

This Telegram bot helps you set reminders. It processes user input to extract the action and time for reminders using SpaCy.

## Features

- **Set Reminders**: Tell the bot what you want to be reminded about and when.
- **Help Command**: Provides instructions on how to use the bot.
- **Cancel Command**: Ends the conversation.

## Prerequisites

- Python 3.8+
- Telegram API token (place it in a `.env` file with the key `API_TOKEN`)
- Install dependencies using pip:

  ```bash
  pip install python-telegram-bot spacy python-dotenv
  python -m spacy download en_core_web_sm
  ```

## Running the Bot

1. Clone the repository or download the code.
2. Create a `.env` file in the root directory with the following content:

   ```dotenv
   API_TOKEN=your_telegram_bot_token_here
   ```

3. Run the bot:

   ```bash
   python main.py
   ```

## Verifying the Solution

1. **Start the Bot**: Send the `/start` command to initiate the conversation.
2. **Set a Reminder**: Send a message in the format "Remind me to <action> in <time>". For example, "Remind me to call mom in 5 hours".
3. **Check Response**: The bot should confirm the reminder and display the details.
4. **Help Command**: Send `/help` to get usage instructions.
5. **Cancel Command**: Send `/cancel` to end the conversation.

### Example Interaction

1. **User**: `/start`
2. **Bot**: "Hi! I'm your reminder bot. Just tell me what you want to be reminded about!"
3. **User**: "Remind me to call mom in 5 hours"
4. **Bot**: "Got it! I'll remind you to call mom in 5 hours."

## Limitations

- **Pattern Matching**: The bot uses a simple pattern matching for "remind me to". If the input does not follow this exact pattern, the bot might not recognize the reminder.
- **Time Extraction**: The bot relies on SpaCy's named entity recognition for time extraction. It may not always correctly identify times, especially in non-standard formats.
- **Time Format**: The bot only accepts time in hours. It does not support minutes or other time formats, so reminders must be specified in whole hours.
- **No Actual Reminder Functionality**: The bot does not actually set or manage reminders. It only processes and acknowledges reminder requests but does not notify users when the time comes. Users will need to manually track their reminders.
- **Error Handling**: If the bot encounters unexpected input or fails to extract the reminder, it will ask the user to rephrase their request without providing detailed error messages. The bot's ability to handle ambiguous or complex inputs is limited.