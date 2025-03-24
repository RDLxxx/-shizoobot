import logging
import telebot
from telebot import types
from google import genai
import asyncio
from func import *
# LOGS
logging.basicConfig(level=logging.INFO)
# API
API_TOKEN = 'APITOKEN'
bot = telebot.TeleBot(API_TOKEN)

user_queries = {}
zsc_opti = 0
zsc_ALLopti = 0
def ask_gemi(prompt):
    global zsc_opti
    global zsc_ALLopti
    zsc_opti += 1
    zsc_ALLopti += 1
    client = genai.Client(api_key="apiHuiMeni")
    answer = "У тебя лимит 3500 символов, чтобы ответить на это: " + prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=answer
    )
    zsc_opti -= 1
    return str(response.text) + "\n" + "gemini-2.0-flash! @shizoobot ♥" + "\n" + "*Сгенерировано нейросетью, только для справки* *"
@bot.inline_handler(func=lambda query: True)
def inline_query(inline_query):
    try:
        query = inline_query.query
        if not inline_query.query:
            results = [
                types.InlineQueryResultArticle(
                    id='1',
                    title="Получить рыночные данные",
                    description="Текущее состояние крипторынка",
                    thumbnail_url="https://i.imgur.com/Br8Ve1D.jpeg",
                    input_message_content=types.InputTextMessageContent(analyze())
                )
            ]
            bot.answer_inline_query(inline_query.id, results)
            return
        query_id = str(inline_query.id)
        user_queries[query_id] = query

        result = types.InlineQueryResultArticle(
            id='1',
            title="GOOGLEAI gemma2!!",
            description="Этот инструмент поможет вам получить ответы от модели gemma2:GOOGLEAI.",
            thumbnail_url="https://i.imgur.com/Br8Ve1D.jpeg",
            input_message_content=types.InputTextMessageContent("Нажмите на кнопку ниже для отправки запроса..."),
            reply_markup=types.InlineKeyboardMarkup().row(
                types.InlineKeyboardButton("Получить ответ от gemma2:GOOGLEAI", callback_data=f"getgemi:{query_id}")
            )
        )

        bot.answer_inline_query(inline_query.id, [result], cache_time=1)
    except Exception as e:
        logging.error(f"Ошибка в inline_query: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("getgemi:"))
def callback_query(call):
    try:
        query_id = call.data.split(":", 1)[1]

        query = user_queries.get(query_id)
        if not query:
            bot.answer_callback_query(call.id, "Запрос не найден! Попробуйте снова...")
            return

        bot.answer_callback_query(call.id, "Запрос Получен!")
        tx = "-" + query + "\n" + "Загрузка запроса..."
        bot.edit_message_text(
            chat_id=None,  # Не требуется для inline-сообщений
            message_id=None,  # Не требуется для inline-сообщений
            inline_message_id=call.inline_message_id,  # ID inline-сообщения
            text=tx
        )
        if zsc_opti == 0:
            user_queries.clear()
        response = ask_gemi(query)
        print("NOW: ", zsc_opti, "ALLWTIME: ", zsc_ALLopti)

        if "Ошибка" in response:
            bot.answer_callback_query(call.id, "Запрос устарел. Попробуйте снова.")
            return

        print("dict: ", user_queries)
        bot.edit_message_text(
            chat_id=None,
            message_id=None,
            inline_message_id=call.inline_message_id,
            text=response
        )
    except Exception as e:
        logging.error(f"Ошибка в callback_query: {e}")
        bot.answer_callback_query(call.id, "Ошибка при обновлении. Попробуйте снова.")

if __name__ == '__main__':
    logging.info("Бот запущен")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.polling())