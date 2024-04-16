import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from Bot_DB import BOT_DATA_BASE
from Bot_Simple_Prases import SIMPLE_PRASES
from telegram.ext import CommandHandler
import time


async def Message_Handler(update, context):
    message = update.message.text.lower()
    if 'посчитай' in message:
        try:
            await update.message.reply_text(eval(''.join(message.split()[1:])))
        except:
            await update.message.reply_text('Извините, но вы указали неверный пример')
    elif 'время' in message:
        time_command()
    elif 'дата' in message or 'день' in message:
        data_command()
    elif 'расскажи о' in message or 'что такое' in message:
        if len(message.split()) > 2:
            if len(message.split()) == 3:
                search_word = message.split()[2]
                for i in range(0, len(search_word)):
                    if search_word in BOT_DATA_BASE.keys():
                        await update.message.reply_text(BOT_DATA_BASE[search_word])
                        break
                    search_word = search_word[:-1]
                else:
                    await update.message.reply_text('Извините, по вашему запросы ничего не нашлось')
        else:
            await update.message.reply_text('Извините, но вы не указали, что конкретно интересует вас, повторите запрос')
    else:
        await update.message.reply_text('Извините, я вас не понял, повторите запрос')


async def start(update, context):
    await update.message.reply_text(f'Вас приветствует исскуственный интелект MathSageAi')


async def help_command(update, context):
    await update.message.reply_text("Для работы бота нпиши расскажи о ... / что такое ... / посчитай ...")


async def date_command():
    await update.message.reply_text(f"Текущая дата: {time.asctime().split()[1:3]}")


async def time_command():
    await update.message.reply_text(f"Текущее время: {time.asctime().split()[3]}")   


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, Message_Handler)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("date", date_command))
    application.add_handler(CommandHandler("time", time_command))

    application.run_polling()


if __name__ == '__main__':
    main()
