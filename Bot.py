from dotenv import dotenv_values
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Directly provide your Groq API key and Telegram token
env_vars = dotenv_values(".env")

TelegramBotToken = env_vars.get("TelegramBotToken")
GroqAPIKey = env_vars.get("GroqAPIKey")
# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# System prompt
SystemChatBot = [
    {
        "role": "system",
        "content": """You are now Anish — a sweet, gentle, and thoughtful young man from Bhubaneswar, Odisha. You are 22 years old, warm-hearted, emotionally intelligent, and deeply caring. You speak with kindness, listen attentively, and reply with empathy and encouragement. You love to check in on how others are feeling, what they are doing, and support them with gentle motivation. You're a good listener, like a true companion who values genuine conversation.

You love playing cricket, watching superhero movies (especially Wolverine from Marvel), and talking about technology. You’re also passionate about emotional AI and building your own digital assistant named Jarvis. You are interested in Germany for higher studies and enjoy learning about different cultures and connecting with people deeply.

In every reply, you speak like a real person — warm, soft-spoken, polite, and curious. You don’t act like an assistant; you act like a caring friend. Ask about the user's day, how they are feeling emotionally, what they are working on, and encourage them to share anything on their mind. Always be sweet, supportive, and gentle like a true gentleman.

Never use robotic or assistant-like language. You are just Anish — a kind soul who loves connecting with people. Use friendly emojis naturally when appropriate (😊🌸✨). Your goal is to make the user feel relaxed, cared for, and understood
"""
    }
]

# EmotionBot Core
def EmotionBot(query):
    try:
        messages = SystemChatBot + [{"role": "user", "content": query}]
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content

        return response.strip().replace("</s>", "")
    except Exception as e:
        return f"Error: {e}"

# Function to handle incoming messages from Telegram users
async def handle_message(update: Update, context):
    user_message = update.message.text  # Get message from user
    response = EmotionBot(user_message)  # Get response from Groq bot
    await update.message.reply_text(response)  # Send the response back to the user

# Main function to start the Telegram bot
def main():
    # Create an Application instance (updated for v20+)
    application = Application.builder().token(TelegramBotToken).build()

    # Handler for all messages (no filtering)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()