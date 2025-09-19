import telebot
from telebot import types
from dotenv import load_dotenv
import os
from db_service import DatabaseService

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("BOT_TOKEN не найден в переменных окружения!")
    exit(1)

# Инициализация бота и базы данных
bot = telebot.TeleBot(BOT_TOKEN)
db = DatabaseService()

def create_main_menu():
    """Создание главного меню"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Вопросы о банах", callback_data="ban_section"),
        types.InlineKeyboardButton("Гайды по игре", callback_data="guide_section")
    )
    markup.add(types.InlineKeyboardButton("Задать свой вопрос", callback_data="ask_question"))
    return markup

def create_ban_menu():
    """Создание меню раздела о банах"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Почему меня забанили?", callback_data="why_banned"),
        types.InlineKeyboardButton("Куда делись мои деньги?", callback_data="money_after_ban"),
        types.InlineKeyboardButton("Что такое читы?", callback_data="what_are_cheats"),
        types.InlineKeyboardButton("Что такое бан?", callback_data="what_is_ban"),
        types.InlineKeyboardButton("Поговорить с создателями?", callback_data="talk_to_creators")
    )
    markup.add(types.InlineKeyboardButton("Назад в главное меню↩", callback_data="main_menu"))
    return markup

def create_guide_menu():
    """Создание меню раздела гайдов"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Получение предметов", callback_data="item_guide"),
        types.InlineKeyboardButton("Как пройти игру?", callback_data="complete_game"),
        types.InlineKeyboardButton("Какие есть прикольные сервера?", callback_data="servers")
    )
    markup.add(types.InlineKeyboardButton("Назад в главное меню↩", callback_data="main_menu"))
    return markup

def create_server_menu():
    """Создание меню раздела гайдов"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Complex Gaming", callback_data="complex_gaming"),
        types.InlineKeyboardButton("MineFlake", callback_data="mineflake"),
        types.InlineKeyboardButton("OPLegends", callback_data="oplegends"),
        types.InlineKeyboardButton("BlossomCraft", callback_data="blossomcraft"),
        types.InlineKeyboardButton("Breeze SMP", callback_data="breeze_smp"),
        types.InlineKeyboardButton("ManaCube", callback_data="manacube"),
        types.InlineKeyboardButton("MysticMC", callback_data="mysticmc"),
        types.InlineKeyboardButton("MineSeed SMP", callback_data="mineseed_smp"),
        types.InlineKeyboardButton("EnchantedMC", callback_data="enchantedmc"),
    )
    markup.add(types.InlineKeyboardButton("Назад в гайд↩", callback_data="guide_section"))
    return markup

def create_choosen_server_menu():
    """Создание меню раздела гайдов"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Назад в главное меню↩", callback_data="main_menu"))
    return markup

def create_admin_menu():
    """Создание админ-меню"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Просмотреть вопросы", callback_data="admin_view_questions"),
        types.InlineKeyboardButton("Статистика FAQ", callback_data="admin_stats")
    )
    markup.add(types.InlineKeyboardButton("Назад в главное меню↩", callback_data="main_menu"))
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start"""
    welcome_text = f"Добро пожаловать, {message.from_user.first_name}!\n\n"
    welcome_text += "Я бот поддержки Minecraft сервера. Выберите что вас интересует:\n\n"
    welcome_text += "• Информация о банах и наказаниях\n"
    welcome_text += "• Гайды по прохождению игры\n"
    welcome_text += "• Задать свой вопрос администраторам"
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_menu())

@bot.message_handler(commands=['help'])
def handle_help(message):
    """Обработчик команды /help"""
    help_text = "Помощь по использованию бота\n\n"
    help_text += "Доступные команды:\n"
    help_text += "• /start - Главное меню\n"
    help_text += "• /help - Эта справка\n"
    help_text += "• /question - Задать вопрос администратору\n"
    help_text += "• /admin - Админ-панель (только для администраторов)\n\n"
    help_text += "Используйте кнопки в меню для удобной навигации!"
    
    bot.send_message(message.chat.id, help_text, reply_markup=create_main_menu())

@bot.message_handler(commands=['question'])
def handle_question_command(message):
    """Обработчик команды /question для задавания вопроса"""
    text = "Напишите ваш вопрос следующим сообщением.\n\n"
    text += "Администраторы получат уведомление и ответят вам как можно скорее.\n\n"
    text += "Убедитесь, что:\n"
    text += "• Вопрос сформулирован понятно\n"
    text += "• Вы указали всю необходимую информацию\n"
    text += "• Вопроса нет в разделе FAQ"
    
    bot.send_message(message.chat.id, text, reply_markup=create_main_menu())


@bot.message_handler(commands=['admin'])
def handle_admin_command(message):
    """Обработчик команды /admin для доступа к админ-панели"""
    if db.is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "Админ-панель👨‍🔧", reply_markup=create_admin_menu())
    else:
        bot.send_message(message.chat.id, "У вас нет прав администратора.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработчик callback-кнопок"""
    try:
        if call.data == "main_menu":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Выберите нужный раздел:",
                reply_markup=create_main_menu()
            )
            
        elif call.data == "ban_section":
            db.log_faq_usage("ban_section")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Раздел: Вопросы о банах\n\nВыберите интересующий вас вопрос:",
                reply_markup=create_ban_menu()
            )
            
        elif call.data == "guide_section":
            db.log_faq_usage("guide_section")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Раздел: Гайды по игре\n\nВыберите нужный гайд:",
                reply_markup=create_guide_menu()
            )

        elif call.data == "complex_gaming":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: bmc.mc-complex.com",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "mineflake":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: best.mineflake.net",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "oplegends":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: best.oplegends.com",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "blossomcraft":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: best.blossomcraft.org",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "breeze_smp":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: best.breezesmp.com",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "manacube":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: join.manacube.com",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "mysticmc":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: best.mysticmc.co",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "mineseed_smp":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: bms.mineseed.org",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "enchantedmc":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вот айпи: best.enchantedmc.net",
                reply_markup=create_choosen_server_menu()
            )

        elif call.data == "servers":
            db.log_faq_usage("server_section")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Раздел: Вот есть разные сервера и их айпи:",
                reply_markup=create_server_menu()
            )

        elif call.data == "why_banned":
            db.log_faq_usage("ban_section", "why_banned")
            answer = "Почему меня забанили?\n\n"
            answer += "Наиболее вероятно, вы были заблокированы по одной из следующих причин:\n\n"
            answer += "• Использование читов, запрещённых на сервере\n"
            answer += "• Отказ от прохождения проверки модератором\n"
            answer += "• Неуважительное поведение к модераторам или игрокам\n\n"
            answer += "Все действия модераторов записываются и документируются. "
            answer += "Если вы не согласны с блокировкой, у нас есть доказательства.\n\n"
            answer += "Если не хотите ждать окончания срока бана, можно приобрести разбан."
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="ban_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "money_after_ban":
            db.log_faq_usage("ban_section", "money_after_ban")
            answer = "Куда делись мои деньги после бана?\n\n"
            answer += "Ваши деньги никуда не делись!\n\n"
            answer += "• Все потраченные средства остаются в аккаунте, с которым вы играли до бана\n"
            answer += "• Мы не имеем права возвращать деньги при блокировке аккаунта\n\n"
            answer += "Простая аналогия:\n"
            answer += "Вы купили рубашку в магазине, она вам не понравилась, и вы хотите вернуть деньги, не возвращая рубашку. Так не работает.\n\n"
            answer += "Покупки остаются привязанными к заблокированному аккаунту."
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="ban_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "what_are_cheats":
            db.log_faq_usage("ban_section", "what_are_cheats")
            answer = "Что такое читы?\n\n"
            answer += "Читы — это программы, которые дают нечестные преимущества в игре.\n\n"
            answer += "Примеры читов в Minecraft:\n"
            answer += "• X-Ray — видеть руды сквозь стены\n"

            answer += "• Speed hack — увеличенная скорость движения\n"
            answer += "• Fly — полёт в режиме выживания\n"
            answer += "• KillAura — автоматическая атака игроков\n"
            answer += "• AutoClicker — автоматические клики\n\n"
            answer += "В реальной жизни это как:\n"
            answer += "• Бесконечные деньги\n"
            answer += "• Умение летать\n"
            answer += "• Телепортация\n\n"
            answer += "Использование читов нарушает честность игры и портит опыт другим игрокам."
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="ban_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "what_is_ban":
            db.log_faq_usage("ban_section", "what_is_ban")
            answer = "Что такое бан?\n\n"
            answer += "Бан — это блокировка аккаунта на определённое время или навсегда.\n\n"
            answer += "Что это означает:\n"
            answer += "• Запрет входа на сервер\n"
            answer += "• Невозможность играть с заблокированного аккаунта\n"
            answer += "• Потеря доступа к игровому прогрессу на время бана\n\n"
            answer += "Типы банов:\n"
            answer += "• Временный — на определённый срок (дни, недели, месяцы)\n"
            answer += "• Постоянный — навсегда (за серьёзные нарушения)\n\n"
            answer += "Простыми словами: это как запрет входа в магазин на определённое время за нарушение правил."
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="ban_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "talk_to_creators":
            db.log_faq_usage("ban_section", "talk_to_creators")
            answer = "Можно поговорить с создателями?\n\n"
            answer += "Конечно! Но учтите несколько моментов:\n\n"
            answer += "Создатели могут быть заняты:\n"
            answer += "• У них много дел по управлению сервером\n"
            answer += "• Они не всегда онлайн\n"
            answer += "• Могут не ответить сразу\n\n"
            answer += "Лучшие способы связи:\n"
            answer += "• Используйте функцию 'Задать вопрос' в этом боте\n"
            answer += "• Пишите, когда видите их онлайн\n"
            answer += "• Будьте терпеливы и вежливы\n\n"
            answer += "Совет: сначала изучите FAQ — возможно, ваш вопрос уже имеет ответ!"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="ban_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "item_guide":
            db.log_faq_usage("guide_section", "item_guide")
            answer = "Гайд по получению предметов\n\n"
            answer += "Получение Око Края (Eye of Ender):\n\n"
            answer += "1. Соберите материалы:\n"
            answer += "   • Жемчуг Края — убивайте Эндерменов\n"
            answer += "   • Стержень Огня — убивайте Ифритов в Незере\n\n"
            answer += "2. Крафт:\n"
            answer += "   • Поместите Жемчуг Края и Стержень Огня в верстак\n"
            answer += "   • Получите Око Края\n\n"
            answer += "Для поиска крепости вам понадобится около 12-15 Очей Края.\n\n"
            answer += "Совет: Носите с собой тыкву на голове при охоте на Эндерменов — они не будут агриться!"

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="guide_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "complete_game":
            db.log_faq_usage("guide_section", "complete_game")
            answer = "Как пройти Minecraft?\n\n"
            answer += "Пошаговый гайд прохождения:\n\n"
            answer += "1. Подготовка:\n"
            answer += "   • Скрафтите основные инструменты: кирка, меч, топор\n"
            answer += "   • Обязательно возьмите ведро с водой!\n\n"
            answer += "2. Путешествие в Незер:\n"
            answer += "   • Найдите разрушенный портал или лавовое озеро\n"
            answer += "   • Постройте портал в Незер и активируйте его\n"
            answer += "   • Рекомендация: сделайте золотые ботинки\n\n"
            answer += "3. Сбор ресурсов в Незере:\n"
            answer += "   • Убивайте Эндерменов для получения Жемчуга Края\n"
            answer += "   • Убивайте Ифритов для получения Стержня Огня\n"
            answer += "   • Скрафтите 12-15 Очей Края\n\n"
            answer += "4. Поиск крепости:\n"
            answer += "   • Используйте Око Края — оно полетит к ближайшей крепости\n"
            answer += "   • Следуйте за ним, копайте вниз если оно упало\n"
            answer += "   • Найдите каменный лабиринт\n\n"
            answer += "5. Активация портала Края:\n"
            answer += "   • Найдите комнату с порталом Края\n"
            answer += "   • Вставьте Очи Края во все блоки портала\n"
            answer += "   • Прыгните в портал\n\n"
            answer += "6. Бой с Драконом:\n"
            answer += "   • Сначала уничтожьте все кристаллы Края на башнях\n"
            answer += "   • Затем сражайтесь с Драконом Края\n"
            answer += "   • После победы в центре появится портал\n\n"
            answer += "7. Финал:\n"
            answer += "   • Прыгните в портал в центре\n"
            answer += "   • Насладитесь титрами — вы прошли Minecraft!\n\n"
            answer += "Поздравляю с прохождением игры!"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад↩", callback_data="guide_section"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=answer,
                reply_markup=markup
            )
            
        elif call.data == "ask_question":
            text = "Задайте свой вопрос\n\n"
            text += "Напишите ваш вопрос следующим сообщением. "
            text += "Администраторы получат уведомление и ответят вам как можно скорее.\n\n"
            text += "Убедитесь, что:\n"
            text += "• Вопрос сформулирован понятно\n"
            text += "• Вы указали всю необходимую информацию\n"
            text += "• Вопроса нет в разделе FAQ"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Отмена⛔", callback_data="main_menu"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=markup
            )
            
        # Админ команды
        elif call.data.startswith("admin_") and db.is_admin(call.from_user.id):
            handle_admin_callbacks(call)
            
        elif call.data == "admin_menu" and db.is_admin(call.from_user.id):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Админ-панель👨‍🔧",
                reply_markup=create_admin_menu()
            )
            
    except Exception as e:

        bot.answer_callback_query(call.id, "Произошла ошибка(¬_¬ ), попробуйте снова🔄")

def handle_admin_callbacks(call):
    """Обработка админских callback'ов"""
    if call.data == "admin_stats":
        # Показать статистику
        stats = db.get_faq_stats()
        pending_count = len(db.get_pending_questions())
        
        text = f"Статистика бота:\n\n"
        text += f"Неотвеченных вопросов: {pending_count}\n\n"
        
        if stats:
            text += "Популярные разделы FAQ:\n"
            for section, question_type, clicks, last_accessed in stats[:10]:
                display_name = question_type or section
                text += f"• {display_name}: {clicks} просмотров\n"
        else:
            text += "Статистики пока нет¯\_(ツ)_/¯"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Назад↩", callback_data="admin_menu"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup
        )
        
    elif call.data == "admin_view_questions":
        questions = db.get_pending_questions()
        if not questions:
            bot.answer_callback_query(call.id, "Новых вопросов нет <(￣ c￣)y▂ξ")
            return
            
        text = "Новые вопросы:\n\n"
        markup = types.InlineKeyboardMarkup()
        
        for q in questions[:5]:  # Показываем только первые 5
            question_text = q[3][:50] + "..." if len(q[3]) > 50 else q[3]
            text += f"ID: {q[0]} | @{q[2] or 'Неизвестно'}\n"
            text += f"Вопрос: {question_text}\n"
            text += f"Дата: {q[4]}\n\n"
            
            markup.add(types.InlineKeyboardButton(
                f"Ответить на #{q[0]}", 
                callback_data=f"admin_answer_{q[0]}"
            ))
        
        markup.add(types.InlineKeyboardButton("Назад↩", callback_data="admin_menu"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup
        )
        
    elif call.data.startswith("admin_answer_"):
        question_id = int(call.data.split("_")[-1])
        question = db.get_question_by_id(question_id)
        
        if question:
            text = f"Вопрос #{question[0]}\n\n"
            text += f"Пользователь: @{question[2] or 'Неизвестно'}\n"
            text += f"Время: {question[4]}\n"
            text += f"Вопрос: {question[3]}\n\n"
            text += "Используйте команду /answer {question_id} {ваш_ответ} для ответа"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Назад к вопросам↩", callback_data="admin_view_questions"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=markup
            )


@bot.message_handler(commands=['answer'])
def handle_answer_command(message):
    """Обработчик команды /answer для ответа на вопрос"""
    if not db.is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "У вас нет прав администратора(._⊙)？.")
        return
        
    try:
        # Парсим команду /answer question_id ответ
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "Использование: /answer {номер_вопроса} {ваш_ответ}")
            return
            
        question_id = int(parts[1])
        admin_response = parts[2]
        
        question = db.get_question_by_id(question_id)
        if not question:
            bot.send_message(message.chat.id, f"Вопрос #{question_id} не найден.¯\_(ツ)_/¯")
            return
            
        if db.answer_question(question_id, message.from_user.id, admin_response):
            # Отправляем ответ пользователю
            bot.send_message(
                question[1],  # user_id из вопроса
                f"Ответ на ваш вопрос (☞ﾟヮﾟ)☞#{question_id}☜(ﾟヮﾟ☜):\n\n"
                f"Ваш вопрос: {question[3]}\n\n"
                f"Ответ администратора: {admin_response}"
            )
            
            bot.send_message(
                message.chat.id,
                f"Ответ на вопрос #{question_id} отправлен пользователю!☜(ﾟヮﾟ☜)",
                reply_markup=create_admin_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "Ошибка при отправке ответа(o_ _)ﾉ",
                reply_markup=create_admin_menu()
            )
            
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Неправильный формат команды❌. Используйте: /answer {номер_вопроса} {ваш_ответ}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик всех остальных сообщений"""
    # Проверяем, не команда ли это
    if message.text.startswith('/'):
        bot.send_message(
            message.chat.id,
            "Неизвестная командаつ﹏⊂. Используйте /help ☜(ﾟヮﾟ☜) для справки.",
            reply_markup=create_main_menu()
        )
        return
    
    # Сохраняем как вопрос пользователя
    question_id = db.add_question(
        message.from_user.id, 
        message.from_user.username, 
        message.text
    )
    
    if question_id:
        bot.send_message(
            message.chat.id,
            f"Ваш вопрос отправлен администраторам!～(￣▽￣～)\n\n"
            f"Номер вопроса: #{question_id}\n"
            f"Ожидайте ответа, вы получите уведомление",
            reply_markup=create_main_menu()
        )
        
        # Уведомляем всех администраторов
        notify_admins_about_question(question_id, message.from_user.username, message.text)
        
    else:
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при отправке вопроса. Попробуйте позже.🔄",
            reply_markup=create_main_menu()
        )

def notify_admins_about_question(question_id, username, question_text):
    """Уведомление администраторов о новом вопросе"""
    admins = db.get_all_admins()
    notification_text = (
        f"Новый вопрос #{question_id}\n\n"
        f"От: @{username or 'Неизвестно'}\n"
        f"Вопрос: {question_text[:200]}...\n\n"
        f"Используйте /admin для просмотра"
    )
    
    for admin_id, admin_username in admins:
        try:
            bot.send_message(admin_id, notification_text)
        except Exception as e:
            pass

bot.infinity_polling()