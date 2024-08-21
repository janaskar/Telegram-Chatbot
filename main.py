import asyncio
import logging
import spacy
from spacy.matcher import Matcher
import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv
from enum import Enum

State = Enum('State', ['REMINDER'])

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
load_dotenv()

reminders = []

class ReminderExtractor:
    def __init__(self, vocab):
        self.matcher = Matcher(vocab)
        # Define patterns to match reminders
        self.matcher.add("REMINDER", [[{"LOWER": "remind"}, {"LOWER": "me"}, {"LOWER": "to"}]])

    def __call__(self, doc):
        matches = self.matcher(doc)
        if not matches:
            return None, None

        action = None
        when = None
        for match_id, start, end in matches:
            span = doc[end:]
            # Find the verb after the "remind me to" phrase
            for token in span:
                if token.pos_ == "VERB":
                    action = token.text
                    break
            # Find the time after the verb
            for token in span:
                if token.ent_type_ == "TIME":
                    when = token.text
                    break
            if action and when:
                break

        return action, when

async def handle_reminder(update, context):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(update.message.text)
    reminder_extractor = ReminderExtractor(nlp.vocab)
    
    action, when = reminder_extractor(doc)
    if action and when:
        # Print the reminder details in blue
        print("\033[94mAction:\033[0m " + action)
        print("\033[94mWhen:\033[0m " + when)        
        reminders.append((action, when))
        print(reminders)
        await update.message.reply_text(f"Got it! I'll remind you to {action} in {when} hours.")
    else:
        print(f"Failed to extract reminder from: {update.message.text}")
        await update.message.reply_text("I didn't catch that. Please tell me what you'd like to be reminded about.")

    return

async def start(update, context):
    #Start the conversation
    await update.message.reply_text("Hi! I'm your reminder bot. Just tell me what you want to be reminded about!")
    return State.REMINDER

async def cancel(update, context):
    #Exit the conversation
    await update.message.reply_text("Goodbye! I'll remember your reminders.")
    return ConversationHandler.END

async def help(update, context):
    #Provide help
    await update.message.reply_text("You can ask me to remind you about something. For example: 'Remind me to call mom at 5 PM'.")
    return

def main():
    #The bot's main message loop is set up and run from here
    application = Application.builder().token(os.getenv('API_TOKEN')).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            State.REMINDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reminder)],
        },
        fallbacks=[CommandHandler(['cancel', 'stop', 'exit'], cancel),
                   CommandHandler('help', help)]
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()