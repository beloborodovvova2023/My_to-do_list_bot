import telebot
import datetime

token = '' #Необходимо добавить токен телеграм-бота
bot = telebot.TeleBot(token)

HELP = """
/help - вывести список доступных команд.
/add - добавить задачу в список.
/print или /show - напечатать список задач на выбранную дату.
/delete - удалить выполненную задачу из списка задач."""

tasks = dict()
completed_tasks = dict()

#Функция для перевода даты в стандартую запись
def translate_to_date(date):
    d = datetime.date.today()
    d_day = d.day
    d_month = d.month
    d_year = d.year
    date_list = date.split(".")
    if len(date_list) == 3:
        new_date = ".".join(date_list)
    elif len(date_list) == 2:
        date_list.append(str(d.year))
        new_date = ".".join(date_list)
    elif len(date_list) == 1:
        if date == "сегодня":
            d_day = d_day
        elif date == "завтра":
            d_day = d_day + 1
        elif date == "послезавтра":
            d_day = d_day + 2
        else:
            d_day = date_list[0]
        date_list = [str(d_day), str(d_month), str(d_year)]
        new_date = ".".join(date_list)
    return new_date

#Функция для добавления задачи
def to_add(date, task):
  if date not in tasks:
    tasks[date] = [task]
  else:
    tasks[date].append(task)

#Функция для удаления задачи
def to_delete(date, task):
    if date in tasks and task in tasks[date]:
        tasks[date].remove(task)
        if date not in completed_tasks:
            completed_tasks[date] = [task]
        else:
            completed_tasks[date].append(task)
        text = f"Задача - {task} удалена с даты - {date}"
    else:
        text = "Введены неправильные данные"
    return text

#Действия при получении команды help
@bot.message_handler(commands=["help"])
def help(message):
     bot.send_message(message.chat.id, HELP)

#Действия при получении команды add
@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    new_date = translate_to_date(date)
    task = command[2]
    to_add(new_date, task)
    text = f"Задача - {task} добавлена на дату - {new_date}"
    bot.send_message(message.chat.id, text)

#Действия при получении команды delete
@bot.message_handler(commands=["delete"])
def delete(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    new_date = translate_to_date(date)
    task = command[2]
    text = to_delete(new_date, task)
    bot.send_message(message.chat.id, text)

#Действия при получении команды completed
@bot.message_handler(commands=["completed"])
def completed(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    new_date = translate_to_date(date)
    text = ""
    if new_date in completed_tasks:
        text = new_date.upper() + "\n"
        for task in completed_tasks[new_date]:
            text = text + "<>" + task + "\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

#Действия при получении команды print или show
@bot.message_handler(commands=["show", "print"])
def show(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    new_date = translate_to_date(date)
    text = ""
    if new_date in tasks:
        text = new_date.upper() + "\n"
        for task in tasks[new_date]:
            text = text + "<>" + task + "\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
