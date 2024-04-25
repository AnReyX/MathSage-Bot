from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, InputMediaPhoto
from BOT_TOKEN import BOT_TOKEN
from Bot_DB import BOT_DATA_BASE
from Bot_Simple_Prases import SIMPLE_PRASES
from telegram.ext import CommandHandler
import time
import sqlite3
from random import choice

current_theme = ''
is_in_task = [False, '', 0]
d = {'logarithms': range(1, 4), 'exponents': range(4, 7), 'derivatives': range(7, 10), 'probability': range(10, 13),
     'stereometry': range(13, 16), 'trigonometry': range(16, 19)}
con = sqlite3.connect('DATA/DB_tasks/tasks_db.sqlite')
cur = con.cursor()
theory = {'logarithms': {'definition': (open('DATA/logarithms/definition.txt', encoding='UTF-8'),
                              open('DATA/logarithms/log.png', 'rb')),
                         'equations': (open('DATA/logarithms/equations.txt', encoding='UTF-8'),
                              open('DATA/logarithms/logarithming.jpg', 'rb')),
                         'properties': (open('DATA/logarithms/properties.txt', encoding='UTF-8'),
                              open('DATA/logarithms/properties.jpg', 'rb'))},
          'exponents': {'definition': (open('DATA/exponents/definition.txt', encoding='UTF-8'),
                             open('DATA/exponents/def.jpg', 'rb')),
                        'differentiating': open('DATA/exponents/differentiating.txt', encoding='UTF-8'),
                        'properties': (open('DATA/exponents/properties.txt', encoding='UTF-8'), '')},
          'derivatives': {'derivative': (open('DATA/derivatives/derivative.txt', encoding='UTF-8'),
                                         open('DATA/derivatives/table_1.jpg', 'rb')),
                          'integral': [InputMediaPhoto(open('DATA/derivatives/integral.png', 'rb'),
                                                       caption=open('DATA/derivatives/integral.txt',
                                                                    encoding='UTF-8').read()),
                                       InputMediaPhoto(open('DATA/derivatives/table_2.jpg', 'rb'))],
                           'formulas': (open('DATA/derivatives/formulas.txt', encoding='UTF-8'),
                               open('DATA/derivatives/formulas.png', 'rb')),
                          'min_max': open('DATA/derivatives/min_max.txt', encoding='UTF-8')},
          'probability': {'definition': (open('DATA/probability/definition.txt', encoding='UTF-8'), ''),
                          'complex_prob': open('DATA/probability/complex.txt', encoding='UTF-8'),
                          'box': [InputMediaPhoto(open('DATA/probability/box_1.png', 'rb'),
                                                       caption=open('DATA/probability/box.txt',
                                                                    encoding='UTF-8').read()),
                                    InputMediaPhoto(open('DATA/probability/box_2.png', 'rb'))],
                          'coin': [InputMediaPhoto(open('DATA/probability/coin_1.png', 'rb'),
                                                       caption=open('DATA/probability/coin.txt',
                                                                    encoding='UTF-8').read()),
                                    InputMediaPhoto(open('DATA/probability/coin_2.png', 'rb')),
                                    InputMediaPhoto(open('DATA/probability/coin_3.png', 'rb'))],
                          'dice': [InputMediaPhoto(open('DATA/probability/dice_1.png', 'rb'),
                                                       caption=open('DATA/probability/dice.txt',
                                                                    encoding='UTF-8').read()),
                                       InputMediaPhoto(open('DATA/probability/dice_2.png', 'rb'))],
                          'games': open('DATA/probability/game.txt', encoding='UTF-8'),
                          'lines': open('DATA/probability/lines.txt', encoding='UTF-8'),
                          'production': open('DATA/probability/production.txt', encoding='UTF-8'),
                          'shooter': open('DATA/probability/shooter.txt', encoding='UTF-8')},
          'trigonometry': {'definition': (open('DATA/trigonometry/definition.txt', encoding='UTF-8'),
                                          open('DATA/trigonometry/funcs.png', 'rb')),
                           'circle': [InputMediaPhoto(open('DATA/trigonometry/t_circle_1.jpg', 'rb'),
                                                       caption=open('DATA/trigonometry/circle.txt',
                                                                    encoding='UTF-8').read()),
                                       InputMediaPhoto(open('DATA/trigonometry/t_circle_2.png', 'rb'))],
                           'equations': (open('DATA/trigonometry/equations.txt', encoding='UTF-8'),
                                         open('DATA/trigonometry/table.jpg', 'rb')),
                           'formulas': (open('DATA/trigonometry/formulas.txt', encoding='UTF-8'),
                               open('DATA/trigonometry/r_formulas.jpg', 'rb'))},
          'stereometry': {'definition': (open('DATA/stereometry/definition.txt', encoding='UTF-8'),
                               open('DATA/stereometry/def.jpg', 'rb')),
                          'plain': [InputMediaPhoto(open('DATA/stereometry/plain_0.png', 'rb'),
                                                       caption=open('DATA/stereometry/plain.txt',
                                                                    encoding='UTF-8').read())] +
                                [InputMediaPhoto(open(f'DATA/stereometry/plain_{i}.png', 'rb')) for i in range(1, 6)],
                          'simple': [InputMediaPhoto(open('DATA/stereometry/parallelogram.png', 'rb'),
                                                       caption=open('DATA/stereometry/simple.txt',
                                                                    encoding='UTF-8').read()),
                                     InputMediaPhoto(open('DATA/stereometry/tetrahedron.png', 'rb'))],
                          'complex': [open('DATA/stereometry/complex.txt',encoding='UTF-8'),
                                      InputMediaPhoto(open('DATA/stereometry/pyramids.png', 'rb')),
                                      InputMediaPhoto(open('DATA/stereometry/cylinder.png', 'rb')),
                                      InputMediaPhoto(open('DATA/stereometry/cone.jpg', 'rb')),
                                      InputMediaPhoto(open('DATA/stereometry/sphere.jpg', 'rb'))],
                          'sdl': [open('DATA/stereometry/sdl.txt', encoding='UTF-8'),
                                  InputMediaPhoto(open('DATA/stereometry/sections_2.png', 'rb')),
                                  InputMediaPhoto(open('DATA/stereometry/angle_plain.png', 'rb')),
                                  InputMediaPhoto(open('DATA/stereometry/two-sided angle.png', 'rb'))],
                          'facts': [open('DATA/stereometry/facts.txt', encoding='UTF-8')] +
                                [InputMediaPhoto(open(f'DATA/stereometry/fact_{i}.png', 'rb')) for i in range(5)],
                          'ttask': (open('DATA/stereometry/ttask.txt', encoding='UTF-8'),
                               open('DATA/stereometry/task.png', 'rb'))}}
graphics = {'logarithms': [InputMediaPhoto(open('DATA/logarithms/y=log(x)_1.png', 'rb'),
                                           caption=open('DATA/logarithms/graph.txt', encoding='UTF-8').read()),
                           InputMediaPhoto(open('DATA/logarithms/y=log(x)_2.png', 'rb'))],
            'exponents': [InputMediaPhoto(open('DATA/exponents/y=√x.png', 'rb'),
                                          caption=open('DATA/exponents/graphs.txt', encoding='UTF-8').read()),
                          InputMediaPhoto(open('DATA/exponents/y=3^^√x.png', 'rb')),
                          InputMediaPhoto(open('DATA/exponents/y=a^x_1.png', 'rb')),
                          InputMediaPhoto(open('DATA/exponents/y=a^x_2.png', 'rb')),
                          InputMediaPhoto(open('DATA/exponents/y=e^x.png', 'rb'))],
            'trigonometry': [InputMediaPhoto(open('DATA/trigonometry/y=sinx.png', 'rb'),
                                             caption=open('DATA/trigonometry/graphs.txt', encoding='UTF-8').read()),
                             InputMediaPhoto(open('DATA/trigonometry/y=cosx.png', 'rb')),
                             InputMediaPhoto(open('DATA/trigonometry/y=tgx.png', 'rb')),
                             InputMediaPhoto(open('DATA/trigonometry/y=ctgx.png', 'rb')),
                             InputMediaPhoto(open('DATA/trigonometry/y=arcsinx.jpg', 'rb')),
                             InputMediaPhoto(open('DATA/trigonometry/y=arccosx.jpg', 'rb')),
                             InputMediaPhoto(open('DATA/trigonometry/y=arctgx.png', 'rb')),
                             InputMediaPhoto(open('DATA/trigonometry/y=arcctgx.png', 'rb'))]}

rk_start = [['/commands', '/maths']]
rk_commands = [['/comm_list', '/back_start']]
rk_math = [['/algebra', '/stereometry', '/back_start']]
rk_algebra = [['/logarithms', '/exponents', '/derivatives'], ['/probability', '/trigonometry', '/back_math']]
rk_logarithms = [['/definition', '/properties', '/graphs'], ['/equations', '/tasks', '/back_algebra']]
rk_exponents = [['/definition', '/properties', '/graphs'], ['/differentiating', '/tasks', '/back_algebra']]
rk_derivatives = [['/derivs', '/integral', '/formulas'], ['/min_max', '/tasks', '/back_algebra']]
rk_probability = [['/definition', '/complex_prob', '/coin', '/dice'], ['/games', '/shooter', '/boxes', '/production'],
                  ['/lines', '/tasks', '/back_algebra']]
rk_trigonometry = [['/definition', '/circle', '/equations'],
                   ['/graphs', '/formulas', '/tasks', '/back_algebra']]
rk_stereometry = [['/definition', '/plain', '/simple'], ['/sections', '/complex', '/facts'],
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


async def tasks(update, context):
    global is_in_task
    if not current_theme:
        await update.message.reply_text(f"Выберите тему.")
    elif not is_in_task[0]:
        t = choice(d[current_theme])
        task, answer, image = cur.execute(f"""SELECT t.task, t.answer, t.images_link FROM
                                          Tasks_Data t WHERE t.id = {t}""").fetchone()
        if image != '-':
            await context.bot.send_photo(update.message.chat_id, photo=open(f'DATA/DB_tasks/{image}', 'rb'),
                                         caption=f"Задача №{t}. {task}")
        else:
            await update.message.reply_text(f"Задача №{t}. {task}")
        is_in_task = [True, answer, t]
    else:
        await update.message.reply_text(f"Чтобы решить следующую задачу, дайте ответ на эту.")


async def definition(update, context):
    if not current_theme:
        await update.message.reply_text("Не могу понять, о каком определении рассказать. Сначала выберите тему.")
    else:
        if theory[current_theme]['definition'][1]:
            await context.bot.send_photo(update.message.chat_id, photo=theory[current_theme]['definition'][1],
                                         caption=theory[current_theme]['definition'][0].read())
        else:
            await update.message.reply_text(theory[current_theme]['definition'][0].read())


async def graphs(update, context):
    if not current_theme:
        await update.message.reply_text("Не могу понять, о каких графиках рассказать. Сначала выберите тему.")
    else:
        await context.bot.send_media_group(chat_id=update.message.chat_id, media=graphics[current_theme])


async def properties(update, context):
    if not current_theme:
        await update.message.reply_text("Не могу понять, о каких свойствах рассказать. Сначала выберите тему.")
    else:
        if theory[current_theme]['properties'][1]:
            await context.bot.send_photo(update.message.chat_id, photo=theory[current_theme]['properties'][1],
                                         caption=theory[current_theme]['properties'][0].read())
        else:
            await update.message.reply_text(theory[current_theme]['properties'][0].read())


async def equations(update, context):
    if not current_theme:
        await update.message.reply_text("Не могу понять, о каких уравнениях рассказать. Сначала выберите тему.")
    else:
        await context.bot.send_photo(update.message.chat_id, photo=theory[current_theme]['equations'][1],
                                     caption=theory[current_theme]['equations'][0].read())


async def formulas(update, context):
    if not current_theme:
        await update.message.reply_text("Не могу понять, о каких формулах рассказать. Сначала выберите тему.")
    else:
        await context.bot.send_photo(update.message.chat_id, photo=theory[current_theme]['formulas'][1],
                                         caption=theory[current_theme]['formulas'][0].read())


async def differentiating(update, context):
    await update.message.reply_text(theory['exponents']['differentiating'].read())


async def derivs(update, context):
    await update.message.reply_text(theory['derivatives']['derivative'][0].read())
    await context.bot.send_photo(update.message.chat_id, photo=theory['derivatives']['derivative'][1])


async def integral(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['derivatives']['integral'])


async def min_max(update, context):
    await update.message.reply_text(theory['derivatives']['min_max'].read())


async def complex_prob(update, context):
    await update.message.reply_text(theory['probability']['complex_prob'].read())


async def coin(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['probability']['coin'])


async def dice(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['probability']['dice'])


async def games(update, context):
    await update.message.reply_text(theory['probability']['games'].read())


async def shooter(update, context):
    await update.message.reply_text(theory['probability']['shooter'].read())


async def boxes(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['probability']['box'])


async def production(update, context):
    await update.message.reply_text(theory['probability']['production'].read())


async def lines(update, context):
    await update.message.reply_text(theory['probability']['lines'].read())


async def circle(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['trigonometry']['circle'])


async def plain(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['stereometry']['plain'])


async def simple(update, context):
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['stereometry']['simple'])


async def sections(update, context):
    await update.message.reply_text(theory['stereometry']['sdl'][0].read())
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['stereometry']['sdl'][1:])


async def complex(update, context):
    await update.message.reply_text(theory['stereometry']['complex'][0].read())
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['stereometry']['complex'][1:])


async def facts(update, context):
    await update.message.reply_text(theory['stereometry']['facts'][0].read())
    await context.bot.send_media_group(chat_id=update.message.chat_id, media=theory['stereometry']['facts'][1:])


async def trial_task(update, context):
    await context.bot.send_photo(update.message.chat_id, photo=theory['stereometry']['ttask'][1],
                                 caption=theory['stereometry']['ttask'][0].read())


async def math(update, context):
    global current_theme
    current_theme = ''
    await update.message.reply_text("Выберите, о чём хотите узнать - об алгебре или стереометрии?",
                                    reply_markup=mu_maths)


async def algebra(update, context):
    global current_theme
    current_theme = ''
    await update.message.reply_text("Выберите раздел!\n1.Логарифмы\n2.Показательные и степенные"
                                    "\n3.Производная и интеграл\n4.Теория вероятности\n5.Тригонометрия",
                                    reply_markup=mu_algebra)


async def logarithms(update, context):
    global current_theme
    current_theme = 'logarithms'
    await update.message.reply_text("Выберите тему:", reply_markup=mu_logarithms)


async def exponents(update, context):
    global current_theme
    current_theme = 'exponents'
    await update.message.reply_text("Выберите тему:", reply_markup=mu_exponents)


async def derivatives(update, context):
    global current_theme
    current_theme = 'derivatives'
    await update.message.reply_text("Выберите тему:", reply_markup=mu_derivatives)


async def probability(update, context):
    global current_theme
    current_theme = 'probability'
    await update.message.reply_text("Выберите тему:", reply_markup=mu_probability)


async def trigonometry(update, context):
    global current_theme
    current_theme = 'trigonometry'
    await update.message.reply_text("Выберите тему:", reply_markup=mu_trigonometry)


async def stereometry(update, context):
    global current_theme
    current_theme = 'stereometry'
    await update.message.reply_text("Выберите тему:", reply_markup=mu_stereometry)


async def date_command(update, context):
    await update.message.reply_text(f"Текущая дата: {time.asctime().split()[1:3]}")


async def time_command(update, context):
    await update.message.reply_text(f"Текущее время: {time.asctime().split()[3]}")


async def Message_Handler(update, context):
    global is_in_task
    message = update.message.text.lower()
    if is_in_task[0]:
        if message.strip() == is_in_task[1]:
            await update.message.reply_text('Верно! Вы молодцы!')
            cur.execute(f'UPDATE Tasks_Data SET is_solved = "True" WHERE ID = {is_in_task[2]}')
            con.commit()
            is_in_task = [False, '', 0]
        else:
            await update.message.reply_text('Неправильно, попробуйте позже.')
            is_in_task = [False, '', 0]
    else:
        if 'посчитай' in message:
            try:
                await update.message.reply_text(eval(''.join(message.split()[1:])))
            except Exception:
                await update.message.reply_text('Извините, но вы указали неверный пример')
        elif 'время' in message:
            await update.message.reply_text(f"Текущее время: {', '.join(time.asctime().split()[3])}")
        elif 'дата' in message or 'день' in message:
            await update.message.reply_text(f"Текущая дата: {time.asctime().split()[1:3]}")
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
                        await update.message.reply_text('Извините, по вашему запросу ничего не нашлось.')
            else:
                await update.message.reply_text('Извините, но я не понял, что именно вы хотите узнать.'
                                                ' Повторите запрос.')
        else:
            await update.message.reply_text('Извините, я вас не понял. Повторите запрос.')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, Message_Handler)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("maths", math))
    application.add_handler(CommandHandler("commands", commands))
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
    application.add_handler(CommandHandler("definition", definition))
    application.add_handler(CommandHandler("graphs", graphs))
    application.add_handler(CommandHandler("tasks", tasks))
    application.add_handler(CommandHandler("properties", properties))
    application.add_handler(CommandHandler("equations", equations))
    application.add_handler(CommandHandler("formulas", formulas))
    application.add_handler(CommandHandler("differentiating", differentiating))
    application.add_handler(CommandHandler("derivs", derivs))
    application.add_handler(CommandHandler("integral", integral))
    application.add_handler(CommandHandler("min_max", min_max))
    application.add_handler(CommandHandler("complex_prob", complex_prob))
    application.add_handler(CommandHandler("coin", coin))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("games", games))
    application.add_handler(CommandHandler("shooter", shooter))
    application.add_handler(CommandHandler("boxes", boxes))
    application.add_handler(CommandHandler("production", production))
    application.add_handler(CommandHandler("lines", lines))
    application.add_handler(CommandHandler("circle", circle))
    application.add_handler(CommandHandler("plain", plain))
    application.add_handler(CommandHandler("simple", simple))
    application.add_handler(CommandHandler("sections", sections))
    application.add_handler(CommandHandler("complex", complex))
    application.add_handler(CommandHandler("facts", facts))
    application.add_handler(CommandHandler("trial_task", trial_task))

    application.run_polling()


if __name__ == '__main__':
    main()
