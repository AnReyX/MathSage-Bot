import logging
from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from BOT_TOKEN import BOT_TOKEN
from Bot_DB import BOT_DATA_BASE
from Bot_Simple_Prases import SIMPLE_PRASES
from telegram.ext import CommandHandler
import time

rk_start = [['/commands', '/maths']]
rk_commands = [['/comm_list', '/back_start']]
rk_math = [['/algebra', '/stereometry', '/back_start']]
rk_algebra = [['/logarithms', '/exponents', '/derivatives'], ['probability', 'trigonometry', '/back_math']]
rk_logarithms = [['/definition', '/properties', '/graphs'], ['/equations', '/tasks', '/back_algebra']]
rk_exponents = [['/definition', '/properties', '/graphs'], ['/differentiating', '/tasks', '/back_algebra']]
rk_derivatives = [['/derivatives', '/integral', '/formulas'], ['/min-max', '/tasks', '/back_algebra']]
rk_probability = [['/easy', '/complex', '/coin', '/dice'], ['/games', '/shooter', '/boxes', '/production'],
                  ['/lines', '/tasks', '/back_algebra']]
rk_trigonometry = [['/functions', '/degrees', '/circle', '/equations'],
                   ['/graphs', '/formulas', '/tasks', '/back_algebra']]
rk_stereometry = [['/definition', '/plane', '/easy_figs'], ['/sections', '/complex_figs', '/facts'],
                  ['/trial_task', '/tasks', '/back_math']]
mu_start = ReplyKeyboardMarkup(rk_start, one_time_keyboard=False)
mu_commands = ReplyKeyboardMarkup(rk_commands, one_time_keyboard=False)
mu_maths = ReplyKeyboardMarkup(rk_math, one_time_keyboard=False)
mu_stereometry = ReplyKeyboardMarkup(rk_stereometry, one_time_keyboard=False)
mu_algebra = ReplyKeyboardMarkup(rk_algebra, one_time_keyboard=False)
mu_logarithms = ReplyKeyboardMarkup(rk_logarithms, one_time_keyboard=False)
mu_exponents = ReplyKeyboardMarkup(rk_exponents, one_time_keyboard=False)
mu_derivatives = ReplyKeyboardMarkup(rk_derivatives, one_time_keyboard=False)
mu_probability = ReplyKeyboardMarkup(rk_probability, one_time_keyboard=False)
mu_trigonometry = ReplyKeyboardMarkup(rk_trigonometry, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text('Вас приветствует искусственный интеллект MathSageAi. Что бы вы хотели сделать?',
                                    reply_markup=mu_start)


async def commands(update, context):
    await update.message.reply_text("Для работы бота напиши расскажи о ... / что такое ... / посчитай ..."
                                    " Нажми на /comm_list, чтобы получить информацию о командах!")


async def math(update, context):
    await update.message.reply_text("Выберите, о чём хотите узнать - об алгебре или стереометрии?",
                                    reply_markup=mu_maths)


async def algebra(update, context):
    await update.message.reply_text("Выберите раздел!\n1.Логарифмы\n2.Показательные и степенные"
                                    "\n3.Производная и интеграл\n4.Теория вероятности\n5.Тригонометрия",
                                    reply_markup=mu_algebra)


async def logarithms(update, context):
    await update.message.reply_text("Выберите тему:", reply_markup=mu_logarithms)


async def exponents(update, context):
    await update.message.reply_text("Выберите тему:", reply_markup=mu_exponents)


async def derivatives(update, context):
    await update.message.reply_text("Выберите тему:", reply_markup=mu_derivatives)


async def probability(update, context):
    await update.message.reply_text("Выберите тему:", reply_markup=mu_probability)


async def trigonometry(update, context):
    await update.message.reply_text("Выберите тему:", reply_markup=mu_trigonometry)


async def stereometry(update, context):
    await update.message.reply_text("Выберите тему:", reply_markup=mu_stereometry)


async def date_command(update, context):
    await update.message.reply_text(f"Текущая дата: {time.asctime().split()[1:3]}")


async def time_command(update, context):
    await update.message.reply_text(f"Текущее время: {time.asctime().split()[3]}")


async def Message_Handler(update, context):
    message = update.message.text.lower()
    if 'посчитай' in message:
        try:
            await update.message.reply_text(eval(''.join(message.split()[1:])))
        except:
            await update.message.reply_text('Извините, но вы указали неверный пример')
    elif 'время' in message:
        await time_command()
    elif 'дата' in message or 'день' in message:
        await date_command()
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


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, Message_Handler)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("maths", math))
    application.add_handler(CommandHandler("help", commands))
    application.add_handler(CommandHandler("date", date_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("back_start", start))
    application.add_handler(CommandHandler("back_math", math))
    application.add_handler(CommandHandler("back_algebra", algebra))
    application.add_handler(CommandHandler("algebra", algebra))
    application.add_handler(CommandHandler("stereometry", stereometry))
    application.add_handler(CommandHandler("logarithms", logarithms))
    application.add_handler(CommandHandler("exponents", exponents))
    application.add_handler(CommandHandler("derivatives", derivatives))
    application.add_handler(CommandHandler("probability", probability))
    application.add_handler(CommandHandler("trigonometry", trigonometry))

    application.run_polling()


if __name__ == '__main__':
    main()
