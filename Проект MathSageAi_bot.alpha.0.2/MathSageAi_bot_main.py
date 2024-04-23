import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from Bot_DB import BOT_DATA_BASE
from Bot_Simple_Prases import SIMPLE_PRASES
from telegram.ext import CommandHandler
import requests
import aiohttp
import time


async def geocoder(update, context):
    context2 = update.message.text.split()[1]
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": context2
    })

    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn(toponym)
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.

    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


def get_ll_spn(toponym):
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = f"{dx},{dy}"

    return ll, span


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def Message_Handler(update, context):
    message = update.message.text.lower()
    if 'посчитай' in message:
        try:
            await update.message.reply_text(eval(''.join(message.split()[1:])))
        except:
            await update.message.reply_text('Извините, но вы указали неверный пример')
    elif 'время' in message:
        await time_command(update, context)
    elif 'дата' in message or 'день' in message:
        await date_command(update, context)
    elif 'покажи' in message:
       # geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
        #                   f"={message.split()[1:]}, 1&format=json"
        await geocoder(update, context)
        #await context.bot.sendPhoto(update.message.chat.id, geocoder_request, caption=update.message.text)
            
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
    elif message in SIMPLE_PRASES.keys():
        await update.message.reply_text(SIMPLE_PRASES[message])
    else:
        await update.message.reply_text('Извините, я вас не понял, повторите запрос')


async def start(update, context):
    await update.message.reply_text(f'Вас приветствует исскуственный интелект MathSageAi')


async def help_command(update, context):
    await update.message.reply_text("Для работы бота нпиши расскажи о ... / что такое ... / посчитай ...")


async def date_command(update, context):
    await update.message.reply_text(f"Текущая дата: {time.asctime().split()[1:3]}")


async def time_command(update, context):
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
