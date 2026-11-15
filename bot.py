import html
import telebot
from telebot import types
from config import token, DATABASE
from db_manager import DB_Manager

bot = telebot.TeleBot(token)
manager = DB_Manager(DATABASE)


PORTFOLIO_USER_ID = 1


ABOUT_TEXT = """\
<b>👋 Привет, меня зовут Матвей!</b>

Я Night Kai, ночной разработчик, который каждый день продолжает учиться и расти. Лучше всего я работаю в тишине ночью, поэтому большая часть моего кода пишется после заката, с чашкой чая и большим любопытством. 🌙

Я пока не эксперт, и меня это устраивает. Каждый исправленный баг и каждый законченный проект делают меня лучше как программиста.

<b>🐍 Python</b>
Python — мой главный инструмент, чтобы быстро создавать вещи. С его помощью я:
• изучаю основы: переменные, функции, классы и модули
• пишу небольшие скрипты, автоматизирующие скучные задачи
• делаю плагины для exteraGram, настраиваемого Telegram-клиента

<b>🔌 Плагины exteraGram</b>
Мне нравится делать плагины, которые добавляют мессенджеру новые функции. Это учит меня:
• читать и понимать чужой код
• работать с API и хуками
• тестировать, отлаживать и улучшать свои проекты
• думать о людях, которые будут этим пользоваться

<b>🧱 Pascal</b>
Pascal — мой любимый язык, потому что он сложный и интересный. Его строгая структура заставляет внимательно думать о типах, логике и устройстве программы. Pascal научил меня дисциплине и сделал лучше во всех остальных языках.

<b>🎯 Над чем работаю</b>
• становлюсь сильнее в Python и Pascal
• создаю и улучшаю плагины exteraGram
• учусь чистому коду и хорошей структуре проектов
• исследую новые идеи, по одному небольшому проекту

<b>🌱 Моя философия</b>
Трудным вещам стоит учиться. Каждая ошибка — это урок. Продолжай делать, даже в 3 часа ночи.

<b>📫 Давай общаться</b>
Я рад знакомству с другими учениками, обмену идеями, отзывам и помощи с плагинами. Если тебе нравятся Python, Pascal или моды для Telegram — пиши!

Night Kai 🌙: кодим при лунном свете.

🌍 Живу в Нью-Йорке
🧠 Сейчас изучаю Rust

🔗 <a href="https://github.com/NightKaiDEV">Мой GitHub</a>
"""


def main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('👤 Про меня', callback_data='about'))
    markup.add(types.InlineKeyboardButton('📁 Мои проекты', callback_data='projects'))
    return markup


def projects_menu():
    markup = types.InlineKeyboardMarkup()
    for project in manager.get_projects(PORTFOLIO_USER_ID):
        project_id, project_name = project[0], project[2]
        markup.add(types.InlineKeyboardButton(project_name, callback_data=f'project_{project_id}'))
    markup.add(types.InlineKeyboardButton('⬅️ В меню', callback_data='menu'))
    return markup


def project_text_and_markup(project_id):
    """Возвращает (текст, клавиатура) для одного проекта или None, если проекта нет."""
    project = next((p for p in manager.get_projects(PORTFOLIO_USER_ID) if p[0] == project_id), None)
    if project is None:
        return None
    name, description, url, status = manager.get_project_info(PORTFOLIO_USER_ID, project[2])[0]
    skills = manager.get_project_skills(name)

    text = f'<b>{html.escape(name)}</b>\n\n'
    if description:
        text += f'{html.escape(description)}\n\n'
    text += f'📌 Статус: {html.escape(status)}\n'
    if skills:
        text += f'🛠 Навыки: {html.escape(skills)}\n'

    markup = types.InlineKeyboardMarkup()
    if url:
        markup.add(types.InlineKeyboardButton('🔗 Открыть на GitHub', url=url))
    markup.add(types.InlineKeyboardButton('⬅️ К проектам', callback_data='projects'))
    return text, markup


def show(call, text, markup):
    """Заменяет текст сообщения с кнопками, не создавая новое."""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode='HTML',
                              disable_web_page_preview=True)
    except telebot.apihelper.ApiTelegramException:
        pass  


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! 👋 Я бот-визитка Матвея (Night Kai).\nВыбери, что хочешь посмотреть:',
                     reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    bot.answer_callback_query(call.id)

    if call.data == 'menu':
        show(call, 'Выбери, что хочешь посмотреть:', main_menu())

    elif call.data == 'about':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('⬅️ В меню', callback_data='menu'))
        show(call, ABOUT_TEXT, markup)

    elif call.data == 'projects':
        show(call, '📁 <b>Мои проекты</b>\nВыбери проект, чтобы узнать подробнее:', projects_menu())

    elif call.data.startswith('project_'):
        result = project_text_and_markup(int(call.data.split('_')[1]))
        if result:
            show(call, *result)
        else:
            show(call, 'Проект не найден 😕', projects_menu())


if __name__ == '__main__':
    manager.create_tables()
    manager.default_insert()
    manager.import_my_projects(PORTFOLIO_USER_ID) 
    print('Бот запущен...')
    bot.infinity_polling()
