from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import datetime as dt
import random
import string
import time
import os
import json  # <--- Илова шуд: Барои кор бо файлҳо

# ===================== CONFIG =====================
TOKEN = "8524676045:AAE7Eb_BDZKaB98-SHis2t4Pdrjgi-UodzY"
ADMIN_IDS = [8436218638]

ADMIN_TELEGRAM = "https://t.me/MARZBON_TJ"
ADMIN_INSTAGRAM = "https://www.instagram.com/marzbontj?igsh=MW9yaG9lcm93YjRueA=="

FREE_UC_CHANNEL = "@marzbon_media"
VISA_NUMBER = "4439200020432471"
SBER_NUMBER = "2202208496090011"
DB_FILE = "database.json"  # <--- Номи файли базаи маълумот

ITEMS = {
    1: {"name": "60 UC", "price": 10},
    2: {"name": "325 UC", "price": 50},
    3: {"name": "660 UC", "price": 100},
    4: {"name": "1800 UC", "price": 250},
    5: {"name": "3850 UC", "price": 500},
    6: {"name": "8100 UC", "price": 1000},
}

VOUCHERS = {
    101: {"name": "Elite Pass", "price": 110},
    102: {"name": "Elite Pass Plus", "price": 260},
    103: {"name": "Bonus Pass", "price": 150},
}

# ===================== LANGUAGES =====================
LANGS = {
    "tj": {
        "lang_name": "🇹🇯 Тоҷикӣ",
        "choose_lang": "🌐 Забонро интихоб кунед:",
        "choose_lang_hint": "Барои идома забонро интихоб кунед:",
        "send_phone": "🔐 Барои истифодаи бот рақами телефони худро фиристед:",
        "phone_btn": "📱 Ворид шудан бо рақам",
        "registered": "✅ Сабт шудед!\n🎁 10 UC бонус гирифтед.",
        "menu_title": "Менюи асосӣ:",
        "menu_products": "🛍 Маҳсулот",
        "menu_wishlist": "❤️ Дилхоҳҳо",
        "menu_cart": "🛒 Сабад",
        "menu_admin_profile": "💬 Профили админ",
        "menu_info": "ℹ Маълумот",
        "menu_free_uc": "🎁 UC ройгон",
        "menu_admin_panel": "👑 Панели админ",
        "menu_lang": "🌐 Забон",
        "use_menu": "🤖 Аз меню истифода баред.",
        "back": "⬅️ Бозгашт",
        "select": "интихоб кунед",
        "product_not_found": "⚠️ Маҳсулот ёфт нашуд.",
        "added_wish": "❤️ Ба дилхоҳҳо илова шуд!",
        "wish_empty": "❤️ Дилхоҳҳо холист.",
        "added_cart": "✅ {name} ба сабад илова шуд!",
        "cart_empty": "🛒 Сабад холист.",
        "cart_cleared": "🗑️ Сабад пок шуд.",
        "checkout": "📦 Фармоиш",
        "clear": "🗑️ Пок",
        "wait_slow": "⏳ Лутфан тез-тез нанависед. 1-2 сония сабр кунед.",
        "blocked": "🚫 Шумо муваққатан блок ҳастед.\n⏰ {m} дақиқаи дигар интизор шавед.",
        "math_prompt": "🔐 Санҷиш: {expr} = ?\n(фақат рақам)\nШумо 3 кӯшиш доред.",
        "math_ok": "✅ Офарин! Санҷиш гузашт.",
        "math_wrong": "❌ Нодуруст. {left} кӯшиш монд.",
        "math_blocked_10": "🚫 Шумо 3 маротиба хато кардед!\nДастрасӣ барои 10 дақиқа маҳдуд шуд.",
        "enter_game_id": "🎮 ID-и бозиро ворид кунед (8–15 рақам):",
        "bad_game_id": "⚠️ ID хатост (8–15 рақам). Дубора ворид кунед:",
        "choose_payment": "Тарзи пардохтро интихоб кунед:",
        "receipt_send": "✅ Пас аз пардохт квитанцияро ҳамчун акс ё файл фиристед.",
        "receipt_received": "✅ Квитанция қабул шуд. Мунтазир шавед, админ месанҷад.",
        "admin_only": "🚫 Танҳо админ!",
        "order_not_found": "⚠️ Фармоиш ёфт нашуд.",
        "order_not_yours": "⚠️ Ин фармоиш барои шумо нест.",
        "sub_first": "📢 Барои гирифтани UC ройгон, аввал ба канал обуна шавед:",
        "check": "🔄 Санҷиш",
        "channel": "📢 Канал",
        "free_menu": "🎁 Менюи UC ройгон:",
        "daily_uc": "🎲 UC рӯзона",
        "my_uc": "📊 UC-и ман",
        "invite_friends": "🔗 Даъвати дӯстон",
        "not_enough_uc": "❌ UC кофӣ нест.",
        "enter_pubg_id": "🎮 ID-и PUBG-ро ворид кунед (8–15 рақам):",
        "request_sent": "✅ Дархост фиристода шуд! №{id}",
        "admin_profile": "Админ:",
        "tg": "✈️ Telegram",
        "ig": "📸 Instagram",
    },
    "ru": {
        "lang_name": "🇷🇺 Русский",
        "choose_lang": "🌐 Выберите язык:",
        "choose_lang_hint": "Чтобы продолжить, выберите язык:",
        "send_phone": "🔐 Для использования бота отправьте свой номер телефона:",
        "phone_btn": "📱 Войти по номеру",
        "registered": "✅ Вы зарегистрированы!\n🎁 Вы получили 10 UC.",
        "menu_title": "Главное меню:",
        "menu_products": "🛍 Товары",
        "menu_wishlist": "❤️ Избранное",
        "menu_cart": "🛒 Корзина",
        "menu_admin_profile": "💬 Профиль админа",
        "menu_info": "ℹ Информация",
        "menu_free_uc": "🎁 Бесплатные UC",
        "menu_admin_panel": "👑 Панель админа",
        "menu_lang": "🌐 Язык",
        "use_menu": "🤖 Используйте меню.",
        "back": "⬅️ Назад",
        "select": "выберите",
        "product_not_found": "⚠️ Товар не найден.",
        "added_wish": "❤️ Добавлено в избранное!",
        "wish_empty": "❤️ Избранное пусто.",
        "added_cart": "✅ {name} добавлено в корзину!",
        "cart_empty": "🛒 Корзина пуста.",
        "cart_cleared": "🗑️ Корзина очищена.",
        "checkout": "📦 Оформить",
        "clear": "🗑️ Очистить",
        "wait_slow": "⏳ Пожалуйста, не пишите слишком часто. Подождите 1–2 секунды.",
        "blocked": "🚫 Вы временно заблокированы.\n⏰ Подождите ещё {m} мин.",
        "math_prompt": "🔐 Проверка: {expr} = ?\n(только цифры)\nУ вас 3 попытки.",
        "math_ok": "✅ Отлично! Проверка пройдена.",
        "math_wrong": "❌ Неверно. Осталось попыток: {left}.",
        "math_blocked_10": "🚫 Вы ошиблись 3 раза!\nДоступ ограничен на 10 минут.",
        "enter_game_id": "🎮 Введите игровой ID (8–15 цифр):",
        "bad_game_id": "⚠️ Неверный ID (8–15 цифр). Введите снова:",
        "choose_payment": "Выберите способ оплаты:",
        "receipt_send": "✅ После оплаты отправьте чек как фото или файл.",
        "receipt_received": "✅ Чек получен. Ожидайте, админ проверит.",
        "admin_only": "🚫 Только админ!",
        "order_not_found": "⚠️ Заказ не найден.",
        "order_not_yours": "⚠️ Это не ваш заказ.",
        "sub_first": "📢 Чтобы получить бесплатные UC, сначала подпишитесь на канал:",
        "check": "🔄 Проверить",
        "channel": "📢 Канал",
        "free_menu": "🎁 Меню бесплатных UC:",
        "daily_uc": "🎲 Ежедневные UC",
        "my_uc": "📊 Мои UC",
        "invite_friends": "🔗 Пригласить друзей",
        "not_enough_uc": "❌ Недостаточно UC.",
        "enter_pubg_id": "🎮 Введите PUBG ID (8–15 цифр):",
        "request_sent": "✅ Заявка отправлена! №{id}",
        "admin_profile": "Админ:",
        "tg": "✈️ Telegram",
        "ig": "📸 Instagram",
    },
    "en": {
        "lang_name": "🇬🇧 English",
        "choose_lang": "🌐 Choose a language:",
        "choose_lang_hint": "To continue, please choose a language:",
        "send_phone": "🔐 To use the bot, send your phone number:",
        "phone_btn": "📱 Login with phone",
        "registered": "✅ You are registered!\n🎁 You received 10 UC.",
        "menu_title": "Main menu:",
        "menu_products": "🛍 Products",
        "menu_wishlist": "❤️ Wishlist",
        "menu_cart": "🛒 Cart",
        "menu_admin_profile": "💬 Admin profile",
        "menu_info": "ℹ Info",
        "menu_free_uc": "🎁 Free UC",
        "menu_admin_panel": "👑 Admin panel",
        "menu_lang": "🌐 Language",
        "use_menu": "🤖 Please use the menu.",
        "back": "⬅️ Back",
        "select": "choose",
        "product_not_found": "⚠️ Product not found.",
        "added_wish": "❤️ Added to wishlist!",
        "wish_empty": "❤️ Wishlist is empty.",
        "added_cart": "✅ {name} added to cart!",
        "cart_empty": "🛒 Cart is empty.",
        "cart_cleared": "🗑️ Cart cleared.",
        "checkout": "📦 Checkout",
        "clear": "🗑️ Clear",
        "wait_slow": "⏳ Please slow down. Wait 1–2 seconds.",
        "blocked": "🚫 You are temporarily blocked.\n⏰ Please wait {m} more minutes.",
        "math_prompt": "🔐 Check: {expr} = ?\n(numbers only)\nYou have 3 tries.",
        "math_ok": "✅ Great! Check passed.",
        "math_wrong": "❌ Wrong. Tries left: {left}.",
        "math_blocked_10": "🚫 You failed 3 times!\nAccess is limited for 10 minutes.",
        "enter_game_id": "🎮 Enter your game ID (8–15 digits):",
        "bad_game_id": "⚠️ Invalid ID (8–15 digits). Try again:",
        "choose_payment": "Choose a payment method:",
        "receipt_send": "✅ After payment, send the receipt as a photo or file.",
        "receipt_received": "✅ Receipt received. Please wait for admin review.",
        "admin_only": "🚫 Admin only!",
        "order_not_found": "⚠️ Order not found.",
        "order_not_yours": "⚠️ This order is not yours.",
        "sub_first": "📢 To get free UC, please subscribe to the channel first:",
        "check": "🔄 Check",
        "channel": "📢 Channel",
        "free_menu": "🎁 Free UC menu:",
        "daily_uc": "🎲 Daily UC",
        "my_uc": "📊 My UC",
        "invite_friends": "🔗 Invite friends",
        "not_enough_uc": "❌ Not enough UC.",
        "enter_pubg_id": "🎮 Enter PUBG ID (8–15 digits):",
        "request_sent": "✅ Request sent! №{id}",
        "admin_profile": "Admin:",
        "tg": "✈️ Telegram",
        "ig": "📸 Instagram",
    },
    "fa": {
        "lang_name": "🇮🇷 فارسی",
        "choose_lang": "🌐 لطفاً زبان را انتخاب کنید:",
        "choose_lang_hint": "برای ادامه، زبان را انتخاب کنید:",
        "send_phone": "🔐 برای استفاده از ربات، شماره تلفن خود را ارسال کنید:",
        "phone_btn": "📱 ورود با شماره",
        "registered": "✅ ثبت‌نام انجام شد!\n🎁 10 UC دریافت کردید.",
        "menu_title": "منوی اصلی:",
        "menu_products": "🛍 محصولات",
        "menu_wishlist": "❤️ علاقه‌مندی‌ها",
        "menu_cart": "🛒 سبد",
        "menu_admin_profile": "💬 پروفایل ادمین",
        "menu_info": "ℹ اطلاعات",
        "menu_free_uc": "🎁 UC رایگان",
        "menu_admin_panel": "👑 پنل ادمین",
        "menu_lang": "🌐 زبان",
        "use_menu": "🤖 لطفاً از منو استفاده کنید.",
        "back": "⬅️ برگشت",
        "select": "انتخاب کنید",
        "product_not_found": "⚠️ محصول پیدا نشد.",
        "added_wish": "❤️ به علاقه‌مندی‌ها اضافه شد!",
        "wish_empty": "❤️ علاقه‌مندی‌ها خالی است.",
        "added_cart": "✅ {name} به سبد اضافه شد!",
        "cart_empty": "🛒 سبد خالی است.",
        "cart_cleared": "🗑️ سبد پاک شد.",
        "checkout": "📦 ثبت سفارش",
        "clear": "🗑️ پاک کردن",
        "wait_slow": "⏳ لطفاً خیلی سریع پیام ندهید. ۱–۲ ثانیه صبر کنید.",
        "blocked": "🚫 شما موقتاً مسدود هستید.\n⏰ لطفاً {m} دقیقه دیگر صبر کنید.",
        "math_prompt": "🔐 بررسی: {expr} = ?\n(فقط عدد)\n۳ فرصت دارید.",
        "math_ok": "✅ عالی! بررسی انجام شد.",
        "math_wrong": "❌ اشتباه. {left} فرصت باقی مانده.",
        "math_blocked_10": "🚫 ۳ بار اشتباه کردید!\nدسترسی برای ۱۰ دقیقه محدود شد.",
        "enter_game_id": "🎮 شناسه بازی را وارد کنید (۸–۱۵ رقم):",
        "bad_game_id": "⚠️ شناسه نادرست است (۸–۱۵ رقم). دوباره وارد کنید:",
        "choose_payment": "روش پرداخت را انتخاب کنید:",
        "receipt_send": "✅ پس از پرداخت، رسید را به‌صورت عکس یا فایل ارسال کنید.",
        "receipt_received": "✅ رسید دریافت شد. لطفاً منتظر بررسی ادمین باشید.",
        "admin_only": "🚫 فقط ادمین!",
        "order_not_found": "⚠️ سفارش پیدا نشد.",
        "order_not_yours": "⚠️ این سفارش برای شما نیست.",
        "sub_first": "📢 برای دریافت UC رایگان، ابتدا در کانال عضو شوید:",
        "check": "🔄 بررسی",
        "channel": "📢 کانال",
        "free_menu": "🎁 منوی UC رایگان:",
        "daily_uc": "🎲 UC روزانه",
        "my_uc": "📊 UC من",
        "invite_friends": "🔗 دعوت دوستان",
        "not_enough_uc": "❌ UC کافی نیست.",
        "enter_pubg_id": "🎮 PUBG ID را وارد کنید (۸–۱۵ رقم):",
        "request_sent": "✅ درخواست ارسال شد! №{id}",
        "admin_profile": "ادمین:",
        "tg": "✈️ تلگرام",
        "ig": "📸 اینستاگرام",
    },
}

def _safe_lang(lang: str) -> str:
    return lang if lang in LANGS else "tj"

def get_lang(uid: str) -> str:
    return _safe_lang(users_data.get(uid, {}).get("lang", "tj"))

def tr(uid: str, key: str, **kwargs) -> str:
    lang = get_lang(uid)
    txt = LANGS.get(lang, LANGS["tj"]).get(key) or LANGS["tj"].get(key, "")
    try:
        return txt.format(**kwargs)
    except Exception:
        return txt

# ===================== ADMIN INFO =====================
ADMIN_INFO_TJ = (
    """ UCstore — ин боти расмии фурӯши UC барои PUBG Mobile ва дигар хидматҳои рақамии бозӣ мебошад. Мо барои бозингарони тоҷик платформаи боэътимод, босифат ва осонро фароҳам овардаем, то харид кардан осон, бехатар ва зуд сурат гирад. ⚡️

🔹 Афзалиятҳои UCstore:

🎁 UC-и ройгон 

🫴Мо ба шумо ҳаруз аз 1 то 5 uc-и ройгон медиҳем ва инчунин бо даъвати ҳар як дуст шумо 2 uc ба даст меоред.

• 🛍 Каталоги пурра бо нархҳои дастрас

• 💳 Усулҳои гуногуни пардохт (аз ҷумла роҳи нави корти милли ва  VISA)

• ⚙️ Системаи автоматии фармоиш ва тасдиқ

• 💬 Пуштибонии зуд аз ҷониби админ

• ❤️ Имкони илова ба “дилхоҳҳо” ва сабади шахсӣ

• 🔔 Огоҳии фаврӣ дар бораи ҳолати фармоиш

📦 Чӣ тавр кор мекунад:

1️⃣ Ба бот ворид шавед

2️⃣ Маҳсулоти дилхоҳатонро интихоб кунед

3️⃣ Фармоиш диҳед ва пардохтро анҷом диҳед

4️⃣ Мунтазир шавед — UC ба ҳисоби шумо фиристода мешавад 🎁

🤝 Бартарии мо — шаффофият, суръат ва эътимод.

Ҳар як фармоиш боэҳтиёт санҷида мешавад, то мизоҷон таҷрибаи беҳтарин гиранд.

Бо UCstore шумо ҳамеша бехатар, зуд ва бо эътимод харид мекунед 💪

Инчунин дар бораи тамоми мушкилот шумо ҳамеша метавонед ба админ тамос гиред @MARZBON_TJ """
)

def admin_info(uid: str) -> str:
    return ADMIN_INFO_TJ

# ===================== DATA (PERSISTENT) =====================
# Ин тағйирёбандаҳо акнун аз файл пур мешаванд
users_data = {}
orders = []
user_carts = {}
user_wishlist = {}
broadcast_draft = {}

# ===================== DATABASE FUNCTIONS =====================
def load_database():
    """Маълумотро аз файл мехонад, агар файл бошад."""
    global users_data, orders
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_data = data.get("users", {})
                orders = data.get("orders", [])
                print(f"✅ Маълумот боргирӣ шуд: {len(users_data)} корбар.")
        except Exception as e:
            print(f"⚠️ Хатогӣ ҳангоми хондани база: {e}")
    else:
        print("ℹ️ Файли база нест. Нав сохта мешавад.")

def save_database():
    """Маълумотро ба файл сабт мекунад."""
    data = {
        "users": users_data,
        "orders": orders
    }
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"⚠️ Хатогӣ ҳангоми сабт: {e}")

# ===================== HELPERS =====================
def is_admin(uid: int) -> bool:
    return uid in ADMIN_IDS

def now_str() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def anti_spam(context: ContextTypes.DEFAULT_TYPE, delay: float = 1.5) -> bool:
    t = time.time()
    last = context.user_data.get("_last_action", 0.0)
    if t - last < delay:
        return False
    context.user_data["_last_action"] = t
    return True

def gen_code(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

def get_item(item_id: int):
    return ITEMS.get(item_id) or VOUCHERS.get(item_id)

def item_label(item_id: int) -> str:
    return "UC" if item_id in ITEMS else "🎫 дигарҳо" if item_id in VOUCHERS else "?"

def create_order(user_id: str, total: int, items: dict, game_id: str) -> dict:
    oid = random.randint(10000, 99999)
    u = users_data.get(user_id, {})
    o = {
        "id": oid,
        "user_id": user_id,
        "user_name": u.get("name", ""),
        "username": u.get("username", ""),
        "phone": u.get("phone", ""),
        "items": items,
        "game_id": game_id,
        "total": total,
        "status": "choose_payment",
        "payment_method": None,
        "proof_file": None,
        "time": now_str(),
        "type": "paid",
    }
    orders.append(o)
    save_database() # <--- САБТ КАРДАН
    return o

def find_order(order_id: int):
    for o in orders:
        if o.get("id") == order_id:
            return o
    return None

def menu_labels(uid: str) -> dict:
    return {
        "products": tr(uid, "menu_products"),
        "wishlist": tr(uid, "menu_wishlist"),
        "cart": tr(uid, "menu_cart"),
        "admin_profile": tr(uid, "menu_admin_profile"),
        "info": tr(uid, "menu_info"),
        "free_uc": tr(uid, "menu_free_uc"),
        "admin_panel": tr(uid, "menu_admin_panel"),
        "lang": tr(uid, "menu_lang"),
    }

async def show_main_menu(chat, user_id: str):
    m = menu_labels(user_id)
    kb = [
        [m["products"], m["wishlist"]],
        [m["cart"], m["admin_profile"]],
        [m["info"], m["free_uc"]],
        [m["lang"]],
    ]
    if is_admin(int(user_id)):
        kb.append([m["admin_panel"]])
    await chat.send_message(tr(user_id, "menu_title"), reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

# ===================== LANGUAGE FLOW =====================
async def send_language_picker(chat, uid: str, hint: str = None, edit_message=None):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(LANGS["tj"]["lang_name"], callback_data="lang_tj")],
        [InlineKeyboardButton(LANGS["ru"]["lang_name"], callback_data="lang_ru")],
        [InlineKeyboardButton(LANGS["en"]["lang_name"], callback_data="lang_en")],
        [InlineKeyboardButton(LANGS["fa"]["lang_name"], callback_data="lang_fa")],
    ])
    text = hint or tr(uid, "choose_lang_hint")
    if edit_message is not None:
        try:
            await edit_message.edit_text(text, reply_markup=kb)
            return
        except Exception:
            pass
    await chat.send_message(text, reply_markup=kb)

async def set_language_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    lang = _safe_lang(q.data.split("_", 1)[1])

    if uid not in users_data:
        users_data[uid] = {
            "id": q.from_user.id,
            "name": q.from_user.first_name or "",
            "username": q.from_user.username or "",
            "phone": "",
            "date": now_str(),
            "free_uc": 0,
            "last_daily_uc": None,
            "code": gen_code(),
            "lang": lang,
        }
        save_database() # <--- САБТ КАРДАН (корбари нав)
    else:
        users_data[uid]["lang"] = lang
        save_database() # <--- САБТ КАРДАН (тағйири забон)

    if context.user_data.get("awaiting_lang"):
        context.user_data["awaiting_lang"] = False

    await q.message.edit_text(tr(uid, "registered"))
    if context.user_data.get("pending_after_lang") == "start_math":
        context.user_data["pending_after_lang"] = None
        await start_math(update, context)
        return

    await show_main_menu(q.message.chat, uid)

# ===================== MATH CHALLENGE =====================
async def start_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    blocked_until = context.user_data.get("math_blocked_until")
    if blocked_until:
        if dt.datetime.now() < blocked_until:
            diff = blocked_until - dt.datetime.now()
            minutes_left = int(diff.total_seconds() // 60) + 1
            await update.effective_chat.send_message(tr(uid, "blocked", m=minutes_left))
            return
        else:
            context.user_data["math_blocked_until"] = None

    op = random.choice(["+", "-"])
    if op == "+":
        a, b = random.randint(1, 50), random.randint(1, 50)
        ans = a + b
        expr = f"{a} + {b}"
    else:
        a = random.randint(1, 50)
        b = random.randint(1, a)
        ans = a - b
        expr = f"{a} - {b}"

    context.user_data["awaiting_math"] = True
    context.user_data["math_ans"] = ans
    context.user_data["math_try"] = 0
    await update.effective_chat.send_message(tr(uid, "math_prompt", expr=expr))

async def check_math(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    uid = str(update.effective_user.id)
    if not context.user_data.get("awaiting_math"):
        blocked_until = context.user_data.get("math_blocked_until")
        if blocked_until and dt.datetime.now() < blocked_until:
            diff = blocked_until - dt.datetime.now()
            minutes_left = int(diff.total_seconds() // 60) + 1
            await update.message.reply_text(tr(uid, "blocked", m=minutes_left))
            return True
        return False

    txt = (update.message.text or "").strip()
    try:
        val = int(txt)
    except Exception:
        val = None

    if val is not None and val == context.user_data.get("math_ans"):
        context.user_data["awaiting_math"] = False
        context.user_data["math_blocked_until"] = None
        await update.message.reply_text(tr(uid, "math_ok"))
        await show_main_menu(update.effective_chat, uid)
        return True

    context.user_data["math_try"] += 1
    left = 3 - context.user_data["math_try"]
    if left > 0:
        await update.message.reply_text(tr(uid, "math_wrong", left=left))
    else:
        context.user_data["awaiting_math"] = False
        context.user_data["math_blocked_until"] = dt.datetime.now() + dt.timedelta(minutes=10)
        await update.message.reply_text(tr(uid, "math_blocked_10"))
    return True

# ===================== START / REGISTER =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    if uid in users_data:
        blocked_until = context.user_data.get("math_blocked_until")
        if blocked_until and dt.datetime.now() < blocked_until:
            diff = blocked_until - dt.datetime.now()
            minutes_left = int(diff.total_seconds() // 60) + 1
            await update.message.reply_text(tr(uid, "blocked", m=minutes_left))
            return
        context.user_data["awaiting_math"] = False
        await show_main_menu(update.effective_chat, uid)
        return

    args = context.args
    if args and args[0].startswith("invite_"):
        inviter = args[0].split("_", 1)[1]
        if inviter and inviter != uid:
            context.user_data["invited_by"] = inviter

    btn = KeyboardButton(tr(uid, "phone_btn"), request_contact=True)
    await update.message.reply_text(
        tr(uid, "send_phone"),
        reply_markup=ReplyKeyboardMarkup([[btn]], resize_keyboard=True, one_time_keyboard=True),
    )

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.contact:
        return
    u = update.effective_user
    uid = str(u.id)
    phone = update.message.contact.phone_number

    if uid not in users_data:
        code = gen_code()
        users_data[uid] = {
            "id": u.id,
            "name": u.first_name or "",
            "username": u.username or "",
            "phone": phone,
            "date": now_str(),
            "free_uc": 10,
            "last_daily_uc": None,
            "code": code,
            "lang": "tj",
        }
        inviter = context.user_data.get("invited_by")
        if inviter and inviter in users_data and inviter != uid:
            users_data[inviter]["free_uc"] = users_data[inviter].get("free_uc", 0) + 2
            try:
                await context.bot.send_message(int(inviter), "🎉 Барои даъват 2 UC гирифтед!")
            except Exception:
                pass
        
        save_database() # <--- САБТ КАРДАН

        for admin in ADMIN_IDS:
            try:
                await context.bot.send_message(admin, f"👤 Корбари нав!\n{u.first_name} | {phone}\n@{u.username}")
            except Exception:
                pass

    await update.message.reply_text("✅ OK", reply_markup=ReplyKeyboardRemove())
    context.user_data["awaiting_lang"] = True
    context.user_data["pending_after_lang"] = "start_math"
    await send_language_picker(update.effective_chat, uid, hint="🌐 Choose language / Забонро интихоб кунед:")

# ===================== CATALOG & ACTIONS =====================
async def catalog_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    target = update.message or (update.callback_query and update.callback_query.message)
    if not target: return
    kb = [
        [InlineKeyboardButton("🪙 UC", callback_data="catalog_uc")],
        [InlineKeyboardButton("🎫 Other / Дигарҳо", callback_data="catalog_voucher")],
        [InlineKeyboardButton(tr(uid, "back"), callback_data="back_main")],
    ]
    await target.reply_text(f"🛍 {tr(uid,'menu_products')}: {tr(uid,'select')}", reply_markup=InlineKeyboardMarkup(kb))

async def catalog_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rows = []
    row = []
    for i, item in ITEMS.items():
        row.append(InlineKeyboardButton(f"{item['name']} — {item['price']} TJS", callback_data=f"select_{i}"))
        if len(row) == 2:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="catalog_back")])
    await q.message.edit_text("🪙 UC:", reply_markup=InlineKeyboardMarkup(rows))

async def catalog_voucher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rows = []
    for i, item in VOUCHERS.items():
        rows.append([InlineKeyboardButton(f"{item['name']} — {item['price']} TJS", callback_data=f"select_{i}")])
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="catalog_back")])
    await q.message.edit_text("🎫 Other:", reply_markup=InlineKeyboardMarkup(rows))

async def select_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try: item_id = int(q.data.split("_", 1)[1])
    except: return
    item = get_item(item_id)
    if not item:
        await q.message.reply_text(tr(uid, "product_not_found"))
        return
    kb = [
        [
            InlineKeyboardButton("🛒 Add", callback_data=f"addcart_{item_id}"),
            InlineKeyboardButton("❤️ Save", callback_data=f"addwish_{item_id}"),
        ],
        [InlineKeyboardButton(tr(uid, "back"), callback_data="catalog_back")]
    ]
    await q.message.reply_text(f"{item_label(item_id)} • {item['name']} — {item['price']} TJS", reply_markup=InlineKeyboardMarkup(kb))

# ===================== WISHLIST =====================
async def add_wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try: item_id = int(q.data.split("_", 1)[1])
    except: return
    if not get_item(item_id): return
    user_wishlist.setdefault(uid, set()).add(item_id)
    await q.message.reply_text(tr(uid, "added_wish"))

async def show_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    w = user_wishlist.get(uid, set())
    if not w:
        await update.message.reply_text(tr(uid, "wish_empty"))
        return
    for item_id in list(w):
        item = get_item(item_id)
        if not item: continue
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("🛒 Add", callback_data=f"addcart_{item_id}"),
            InlineKeyboardButton("🗑️ Remove", callback_data=f"removewish_{item_id}")
        ]])
        await update.message.reply_text(f"❤️ {item['name']} — {item['price']} TJS", reply_markup=kb)

async def remove_wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🗑️")
    uid = str(q.from_user.id)
    try: item_id = int(q.data.split("_", 1)[1])
    except: return
    if uid in user_wishlist:
        user_wishlist[uid].discard(item_id)
    try: await q.message.delete()
    except: pass

# ===================== CART =====================
async def add_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try: item_id = int(q.data.split("_", 1)[1])
    except: return
    item = get_item(item_id)
    if not item:
        await q.message.reply_text(tr(uid, "product_not_found"))
        return
    user_carts.setdefault(uid, {})
    user_carts[uid][item_id] = user_carts[uid].get(item_id, 0) + 1
    await q.message.reply_text(tr(uid, "added_cart", name=item["name"]))

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    user_carts[uid] = {}
    await q.message.reply_text(tr(uid, "cart_cleared"))

async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    cart = user_carts.get(uid, {})
    if not cart:
        await update.message.reply_text(tr(uid, "cart_empty"))
        return
    total = 0
    txt = f"{tr(uid,'menu_cart')}\n"
    for item_id, qty in cart.items():
        note = get_item(item_id)
        if not note: continue
        subtotal = note["price"] * qty
        total += subtotal
        txt += f"- {note['name']} x{qty} = {subtotal} TJS\n"
    txt += f"\n💰 Total: {total} TJS"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(uid, "checkout"), callback_data="checkout"),
         InlineKeyboardButton(tr(uid, "clear"), callback_data="clear_cart")],
        [InlineKeyboardButton(tr(uid, "back"), callback_data="back_main")]
    ])
    await update.message.reply_text(txt, reply_markup=kb)

# ===================== CHECKOUT / PAYMENT =====================
async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    cart = user_carts.get(uid, {})
    if not cart:
        await q.message.reply_text(tr(uid, "cart_empty"))
        return
    context.user_data["awaiting_game_id"] = True
    context.user_data["pending_items"] = dict(cart)
    await q.message.reply_text(tr(uid, "enter_game_id"))

async def handle_game_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    game_id = (update.message.text or "").strip()
    if not game_id.isdigit() or not (8 <= len(game_id) <= 15):
        await update.message.reply_text(tr(uid, "bad_game_id"))
        return
    items = context.user_data.get("pending_items") or {}
    if not items:
        context.user_data["awaiting_game_id"] = False
        await update.message.reply_text(tr(uid, "cart_empty"))
        return
    total = 0
    for item_id, qty in items.items():
        it = get_item(int(item_id))
        if it: total += it["price"] * int(qty)
    order = create_order(uid, total, items, game_id)
    user_carts[uid] = {}
    context.user_data["awaiting_game_id"] = False
    context.user_data.pop("pending_items", None)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 VISA", callback_data=f"pay_visa_{order['id']}")],
        [InlineKeyboardButton("🏦 SberBank", callback_data=f"pay_sber_{order['id']}")],
    ])
    await update.message.reply_text(
        f"📦 Order №{order['id']}\n🎮 ID: {game_id}\n💰 Total: {total} TJS\n\n{tr(uid,'choose_payment')}",
        reply_markup=kb
    )

async def choose_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    parts = q.data.split("_")
    method = parts[1]
    order_id = int(parts[2])
    order = find_order(order_id)
    if not order:
        await q.message.reply_text(tr(uid, "order_not_found"))
        return
    if str(q.from_user.id) != str(order["user_id"]):
        await q.message.reply_text(tr(uid, "order_not_yours"))
        return
    order["status"] = "awaiting_proof"
    order["payment_method"] = "VISA" if method == "visa" else "SberBank"
    save_database() # <--- САБТ
    card = VISA_NUMBER if method == "visa" else SBER_NUMBER
    context.user_data["awaiting_proof_order"] = order_id
    await q.message.reply_text(f"💳 {order['payment_method']}\n📌 Card: {card}\n\n{tr(uid,'receipt_send')}")

async def receive_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    order_id = context.user_data.get("awaiting_proof_order")
    if not order_id: return
    order = find_order(int(order_id))
    if not order or order.get("status") != "awaiting_proof": return
    file_id = None
    is_photo = False
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        is_photo = True
    elif update.message.document:
        file_id = update.message.document.file_id
        is_photo = False
    else: return
    order["proof_file"] = file_id
    order["status"] = "proof_sent"
    save_database() # <--- САБТ
    context.user_data.pop("awaiting_proof_order", None)
    items_txt = ""
    for item_id, qty in (order.get("items") or {}).items():
        item_id = int(item_id)
        it = get_item(item_id)
        if it: items_txt += f"{item_label(item_id)}: {it['name']} x{qty}\n"
    caption = (
        f"📦 Order №{order['id']}\n"
        f"👤 @{order.get('username') or order.get('user_name')}\n"
        f"🎮 ID: {order.get('game_id')}\n\n"
        f"{items_txt}\n"
        f"💰 Total: {order.get('total')} TJS\n"
        f"💳 Payment: {order.get('payment_method')}\n"
        f"📱 Phone: {order.get('phone') or '—'}\n"
        f"🕒 {order.get('time')}"
    )
    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Confirm", callback_data=f"admin_pay_confirm_{order['id']}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"admin_pay_reject_{order['id']}"),
    ]])
    for admin in ADMIN_IDS:
        try:
            if is_photo: await context.bot.send_photo(admin, photo=file_id, caption=caption, reply_markup=buttons)
            else: await context.bot.send_document(admin, document=file_id, caption=caption, reply_markup=buttons)
        except: pass
    await update.message.reply_text(tr(uid, "receipt_received"))

async def admin_pay_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.message.reply_text(tr(str(q.from_user.id), "admin_only"))
        return
    parts = q.data.split("_")
    action = parts[2]
    order_id = int(parts[3])
    order = find_order(order_id)
    if not order:
        await q.message.reply_text("Order not found.")
        return
    if action == "confirm":
        order["status"] = "confirmed"
        txt_user = f"✅ Order №{order_id} confirmed. Thank you!"
        txt_admin = f"✅ Confirmed: №{order_id}"
    else:
        order["status"] = "rejected"
        txt_user = f"❌ Order №{order_id} rejected. Please contact admin."
        txt_admin = f"❌ Rejected: №{order_id}"
    
    save_database() # <--- САБТ

    try: await context.bot.send_message(int(order["user_id"]), txt_user)
    except: pass
    await q.message.reply_text(txt_admin)

# ===================== FREE UC =====================
async def free_uc_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    uid = str(update.effective_user.id)
    if uid not in users_data:
        await chat.send_message("⚠️ /start first.")
        return
    subscribed = False
    try:
        member = await context.bot.get_chat_member(FREE_UC_CHANNEL, int(uid))
        subscribed = member.status in ["member", "administrator", "creator"]
    except: subscribed = False
    if not subscribed:
        await chat.send_message(
            tr(uid, "sub_first"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(tr(uid, "channel"), url=f"https://t.me/{FREE_UC_CHANNEL.lstrip('@')}")],
                [InlineKeyboardButton(tr(uid, "check"), callback_data="check_sub")],
            ])
        )
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(uid, "daily_uc"), callback_data="daily_uc")],
        [InlineKeyboardButton(tr(uid, "my_uc"), callback_data="my_uc")],
        [InlineKeyboardButton("🎁 60 UC", callback_data="claim_60"),
         InlineKeyboardButton("🎁 325 UC", callback_data="claim_325")],
        [InlineKeyboardButton(tr(uid, "invite_friends"), callback_data="invite_link")]
    ])
    await chat.send_message(tr(uid, "free_menu"), reply_markup=kb)

async def daily_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    u = users_data.get(uid)
    if not u:
        await q.message.reply_text("⚠️ /start first.")
        return
    now = dt.datetime.now()
    last = u.get("last_daily_uc")
    if last:
        try:
            last_dt = dt.datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
            if (now - last_dt).total_seconds() < 24 * 3600:
                left_seconds = int(24 * 3600 - (now - last_dt).total_seconds())
                hours = left_seconds // 3600
                minutes = (left_seconds % 3600) // 60
                await q.message.edit_text(f"⏳ Already claimed.\nWait {hours}h {minutes}m.")
                return
        except: pass
    frames = [
        "🎁  Gift: [ 1 |  | 3 | 4 | 5 ]",
        "🎁  Gift: [ 5 | 1 | 2 | 3 | 4 ]",
        "🎁  Gift: [ 4 | 5 | 1 | 2 | 3 ]",
        "🎁  Gift: [ 3 | 4 | 5 | 1 | 2 ]",
    ]
    msg = await q.message.edit_text("🎁 Checking today's gift...")
    for _ in range(2):
        for frame in frames:
            try:
                await msg.edit_text(frame)
                time.sleep(0.3)
            except: pass
    roll = random.choices([1, 2, 3, 4, 5], weights=[60, 20, 10, 7, 3])[0]
    u["free_uc"] = u.get("free_uc", 0) + roll
    u["last_daily_uc"] = now_str()
    
    save_database() # <--- САБТ КАРДАН

    await msg.edit_text(f"🎁 Today: {roll} UC\n💰 Total: {u['free_uc']} UC\n\nCome back tomorrow!")

async def my_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    u = users_data.get(uid, {})
    await q.message.reply_text(f"📊 {u.get('free_uc', 0)} UC")

async def claim_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    need = 60 if q.data == "claim_60" else 325
    uid = str(q.from_user.id)
    u = users_data.get(uid, {})
    if u.get("free_uc", 0) < need:
        await q.message.reply_text(tr(uid, "not_enough_uc"))
        return
    context.user_data["awaiting_free_claim"] = need
    await q.message.reply_text(tr(uid, "enter_pubg_id"))

async def handle_free_claim_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    game_id = (update.message.text or "").strip()
    if not game_id.isdigit() or not (8 <= len(game_id) <= 15):
        await update.message.reply_text(tr(uid, "bad_game_id"))
        return
    need = context.user_data.pop("awaiting_free_claim", None)
    if not need: return
    u = users_data.get(uid)
    if not u or u.get("free_uc", 0) < need:
        await update.message.reply_text(tr(uid, "not_enough_uc"))
        return
    u["free_uc"] -= need
    order_id = random.randint(10000, 99999)
    o = {
        "id": order_id,
        "type": "free_uc",
        "pack": need,
        "user_id": uid,
        "username": u.get("username"),
        "phone": u.get("phone"),
        "game_id": game_id,
        "status": "pending",
        "time": now_str(),
    }
    orders.append(o)
    
    save_database() # <--- САБТ

    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Confirm", callback_data=f"admin_free_confirm_{order_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"admin_free_reject_{order_id}"),
    ]])
    for admin in ADMIN_IDS:
        try:
            await context.bot.send_message(
                admin,
                f"🎁 FREE UC #{order_id}\n👤 @{u.get('username') or '—'}\n🎮 ID: {game_id}\nPack: {need} UC",
                reply_markup=btn
            )
        except: pass
    await update.message.reply_text(tr(uid, "request_sent", id=order_id))

async def admin_free_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.message.reply_text(tr(str(q.from_user.id), "admin_only"))
        return
    parts = q.data.split("_")
    action = parts[2]
    order_id = int(parts[3])
    o = find_order(order_id)
    if not o or o.get("type") != "free_uc":
        await q.message.reply_text("Order not found.")
        return
    if action == "confirm":
        o["status"] = "confirmed"
        msg_user = f"✅ FREE UC (#{order_id}) confirmed!"
        msg_admin = "✅ Confirmed."
    else:
        o["status"] = "rejected"
        msg_user = f"❌ FREE UC (#{order_id}) rejected. Contact admin."
        msg_admin = "❌ Rejected."
    
    save_database() # <--- САБТ

    try: await context.bot.send_message(int(o["user_id"]), msg_user)
    except: pass
    await q.message.reply_text(msg_admin)

async def invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try:
        me = await context.bot.get_me()
        link = f"https://t.me/{me.username}?start=invite_{uid}"
        await q.message.reply_text(f"🔗 Invite link:\n{link}\n\nEach invite → 2 UC")
    except: await q.message.reply_text("⚠️ Error.")

# ===================== BROADCAST =====================
async def bc_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.message.reply_text(tr(str(q.from_user.id), "admin_only"))
        return
    aid = str(q.from_user.id)
    broadcast_draft[aid] = {"text": "", "photo": None, "buttons": [], "step": None}
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Text", callback_data="bc_text")],
        [InlineKeyboardButton("🔘 Button", callback_data="bc_button")],
        [InlineKeyboardButton("🖼 Photo", callback_data="bc_photo")],
        [InlineKeyboardButton("📤 Send", callback_data="bc_send")],
        [InlineKeyboardButton("❌ Cancel", callback_data="bc_cancel")],
    ])
    await q.message.reply_text("📢 Broadcast menu:", reply_markup=kb)

async def bc_set_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.setdefault(aid, {"text":"", "photo":None, "buttons":[], "step":None})
    broadcast_draft[aid]["step"] = "text"
    await q.message.reply_text("✏️ Write message text:")

async def bc_set_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.setdefault(aid, {"text":"", "photo":None, "buttons":[], "step":None})
    broadcast_draft[aid]["step"] = "button"
    await q.message.reply_text("🔘 Format:\nText | https://link")

async def bc_set_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.setdefault(aid, {"text":"", "photo":None, "buttons":[], "step":None})
    broadcast_draft[aid]["step"] = "photo"
    await q.message.reply_text("🖼 Send a photo:")

async def bc_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    aid = str(q.from_user.id)
    d = broadcast_draft.get(aid)
    if not d:
        await q.message.reply_text("❌ No draft.")
        return
    kb = None
    if d.get("buttons"): kb = InlineKeyboardMarkup([d["buttons"]])
    sent = 0
    for uid in list(users_data.keys()):
        try:
            if d.get("photo"): await context.bot.send_photo(int(uid), photo=d["photo"], caption=d.get("text",""), reply_markup=kb)
            else: await context.bot.send_message(int(uid), text=d.get("text",""), reply_markup=kb)
            sent += 1
        except: pass
    broadcast_draft.pop(aid, None)
    await q.message.reply_text(f"✅ Sent to {sent} users.")

async def bc_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.pop(aid, None)
    await q.message.reply_text("❌ Cancelled.")

async def bc_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo: return
    uid = str(update.effective_user.id)
    d = broadcast_draft.get(uid)
    if not d or d.get("step") != "photo": return
    d["photo"] = update.message.photo[-1].file_id
    d["step"] = None
    await update.message.reply_text("✅ Photo saved.")

# ===================== ADMIN PANEL (NEW GIFT FEATURE) =====================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid): return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Users", callback_data="admin_users")],
        [InlineKeyboardButton("📦 Orders", callback_data="admin_orders")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="bc_menu")],
        [InlineKeyboardButton("🎁 Gift UC (Туҳфа)", callback_data="admin_gift_start")],
        [InlineKeyboardButton("🗑 Clear users", callback_data="admin_clear_confirm")],
    ])
    await update.message.reply_text("👑 Admin panel:", reply_markup=kb)

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    if not users_data:
        await q.message.reply_text("No users yet.")
        return
    txt = "👤 Users (up to 20):\n\n"
    c = 0
    for uid, u in users_data.items():
        txt += f"- {u.get('name','—')} | {u.get('phone','—')} | id:{uid} | lang:{u.get('lang','tj')}\n"
        c += 1
        if c >= 20:
            if len(users_data) > 20: txt += "\n... more users exist"
            break
    await q.message.reply_text(txt)

async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    if not orders:
        await q.message.reply_text("No orders yet.")
        return
    txt = "📦 Last 15 orders:\n\n"
    for o in orders[-15:]:
        if o.get("type") == "free_uc": txt += f"#{o['id']} | FREE {o.get('pack')}UC | {o.get('status')}\n"
        else: txt += f"#{o['id']} | {o.get('total')}TJS | {o.get('status')}\n"
    await q.message.reply_text(txt)

async def admin_clear_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, clear", callback_data="admin_clear_do")],
        [InlineKeyboardButton("❌ No", callback_data="admin_clear_no")],
    ])
    await q.message.reply_text("⚠️ This will clear all users/orders. Continue?", reply_markup=kb)

async def admin_clear_do(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    n = len(users_data)
    users_data.clear()
    orders.clear()
    user_carts.clear()
    user_wishlist.clear()
    
    save_database() # <--- САБТ (База тоза шуд)

    await q.message.reply_text(f"🗑 Cleared: {n} users.")

async def admin_clear_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✅ Cancelled.")

# ---- NEW GIFT FUNCTIONS ----
async def admin_gift_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    context.user_data["awaiting_gift_id"] = True
    await q.message.reply_text("👤 ID-и корбарро нависед (User ID):")

async def admin_gift_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return
    
    amount = int(q.data.split("_")[2])
    context.user_data["gift_amount"] = amount
    context.user_data["awaiting_gift_reason"] = True
    
    await q.message.edit_text(
        f"🎁 Интихоб шуд: {amount} UC.\n"
        "📝 Акнун сабаби туҳфаро нависед (ин матн ба корбар меравад):"
    )

# ===================== MAIN HANDLER ROUTER =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    uid = str(update.effective_user.id)

    # Anti spam
    if not anti_spam(context):
        await update.message.reply_text(tr(uid, "wait_slow"))
        return

    # Block check
    blocked_until = context.user_data.get("math_blocked_until")
    if blocked_until:
        if dt.datetime.now() < blocked_until:
            diff = blocked_until - dt.datetime.now()
            minutes_left = int(diff.total_seconds() // 60) + 1
            await update.message.reply_text(tr(uid, "blocked", m=minutes_left))
            return
        else:
            context.user_data["math_blocked_until"] = None

    if context.user_data.get("awaiting_lang"):
        await send_language_picker(update.effective_chat, uid, hint=tr(uid, "choose_lang_hint"))
        return

    if context.user_data.get("awaiting_math"):
        consumed = await check_math(update, context)
        if consumed: return

    if context.user_data.get("awaiting_game_id"):
        await handle_game_id(update, context)
        return

    if context.user_data.get("awaiting_free_claim"):
        await handle_free_claim_id(update, context)
        return

    # BROADCAST STEPS
    d = broadcast_draft.get(uid)
    if d and d.get("step") == "text":
        d["text"] = update.message.text
        d["step"] = None
        await update.message.reply_text("✅ Saved.")
        return
    if d and d.get("step") == "button":
        try:
            bt, url = update.message.text.split("|", 1)
            d["buttons"].append(InlineKeyboardButton(bt.strip(), url=url.strip()))
            await update.message.reply_text("✅ Button added.")
        except: await update.message.reply_text("❌ Wrong format.\nText | https://link")
        d["step"] = None
        return

    # GIFT STEPS
    if context.user_data.get("awaiting_gift_id"):
        target_id = update.message.text.strip()
        if target_id not in users_data:
            await update.message.reply_text("⚠️ Корбар ёфт нашуд (ID нодуруст). Лутфан ID-и дурустро нависед:")
            return
        
        context.user_data["awaiting_gift_id"] = False
        context.user_data["gift_target_id"] = target_id
        
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("5 UC", callback_data="gift_amt_5"), InlineKeyboardButton("10 UC", callback_data="gift_amt_10")],
            [InlineKeyboardButton("15 UC", callback_data="gift_amt_15"), InlineKeyboardButton("20 UC", callback_data="gift_amt_20")],
            [InlineKeyboardButton("❌ Бекор кардан", callback_data="admin_gift_cancel")]
        ])
        await update.message.reply_text(f"👤 Корбар: {users_data[target_id].get('name')}\n🎁 Миқдори UC-ро интихоб кунед:", reply_markup=kb)
        return

    if context.user_data.get("awaiting_gift_reason"):
        reason = update.message.text.strip()
        target_id = context.user_data.get("gift_target_id")
        amount = context.user_data.get("gift_amount")
        
        if target_id in users_data and amount:
            users_data[target_id]["free_uc"] = users_data[target_id].get("free_uc", 0) + amount
            save_database() # <--- САБТ КАРДАН (Туҳфа)
            
            try:
                msg_to_user = (
                    f"🎁 Табрик! Шумо аз тарафи админ {amount} UC туҳфа гирифтед.\n"
                    f"💬 Сабаб: {reason}\n"
                    f"💰 Ҳисоби ҳозираи шумо: {users_data[target_id]['free_uc']} UC"
                )
                await context.bot.send_message(int(target_id), msg_to_user)
            except Exception as e:
                await update.message.reply_text(f"⚠️ Хатогӣ ҳангоми фиристодан ба корбар: {e}")
            
            await update.message.reply_text(
                f"✅ {amount} UC ба {users_data[target_id].get('name')} фиристода шуд!\n"
                f"Сабаб: {reason}"
            )
        else:
            await update.message.reply_text("⚠️ Хатогӣ. Маълумот гум шуд.")

        context.user_data["awaiting_gift_reason"] = False
        context.user_data["gift_target_id"] = None
        context.user_data["gift_amount"] = None
        return

    # MAIN MENU ACTIONS
    text = (update.message.text or "").strip()
    m = menu_labels(uid)

    if text == m["products"]: await catalog_menu(update, context)
    elif text == m["wishlist"]: await show_wishlist(update, context)
    elif text == m["cart"]: await show_cart(update, context)
    elif text == m["info"]: await update.message.reply_text(admin_info(uid))
    elif text == m["free_uc"]: await free_uc_menu(update, context)
    elif text == m["admin_profile"]:
        await update.message.reply_text(
            tr(uid, "admin_profile"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(tr(uid, "tg"), url=ADMIN_TELEGRAM)],
                [InlineKeyboardButton(tr(uid, "ig"), url=ADMIN_INSTAGRAM)],
            ])
        )
    elif text == m["lang"]: await send_language_picker(update.effective_chat, uid, hint=tr(uid, "choose_lang"))
    elif text == m["admin_panel"] and is_admin(int(uid)): await admin_panel(update, context)
    else: await update.message.reply_text(tr(uid, "use_menu"))

# ===================== CALLBACK ROUTER =====================
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if not q or not q.data: return
    uid = str(q.from_user.id)

    if not anti_spam(context, delay=1.2):
        await q.answer("⏳", show_alert=True)
        return
    blocked_until = context.user_data.get("math_blocked_until")
    if blocked_until and dt.datetime.now() < blocked_until:
        await q.answer("🚫", show_alert=True)
        return

    data = q.data

    if data.startswith("lang_"): await set_language_cb(update, context); return
    if data == "catalog_uc": await catalog_uc(update, context); return
    if data == "catalog_voucher": await catalog_voucher(update, context); return
    if data == "catalog_back": await catalog_menu(update, context); return
    if data.startswith("select_"): await select_item(update, context); return
    if data.startswith("addwish_"): await add_wish(update, context); return
    if data.startswith("removewish_"): await remove_wish(update, context); return
    if data.startswith("addcart_"): await add_cart(update, context); return
    if data == "clear_cart": await clear_cart(update, context); return
    if data == "checkout": await checkout(update, context); return
    if data.startswith(("pay_visa_", "pay_sber_")): await choose_payment(update, context); return
    if data.startswith("admin_pay_confirm_") or data.startswith("admin_pay_reject_"): await admin_pay_action(update, context); return
    if data == "check_sub": await q.answer(); await free_uc_menu(update, context); return
    if data == "daily_uc": await daily_uc(update, context); return
    if data == "my_uc": await my_uc(update, context); return
    if data in ("claim_60", "claim_325"): await claim_btn(update, context); return
    if data == "invite_link": await invite_link(update, context); return
    if data.startswith("admin_free_confirm_") or data.startswith("admin_free_reject_"): await admin_free_action(update, context); return
    
    # Broadcast
    if data == "bc_menu": await bc_menu(update, context); return
    if data == "bc_text": await bc_set_text(update, context); return
    if data == "bc_button": await bc_set_button(update, context); return
    if data == "bc_photo": await bc_set_photo(update, context); return
    if data == "bc_send": await bc_send(update, context); return
    if data == "bc_cancel": await bc_cancel(update, context); return
    
    # Admin Panel
    if data == "admin_users": await admin_users(update, context); return
    if data == "admin_orders": await admin_orders(update, context); return
    if data == "admin_clear_confirm": await admin_clear_confirm(update, context); return
    if data == "admin_clear_do": await admin_clear_do(update, context); return
    if data == "admin_clear_no": await admin_clear_no(update, context); return
    
    # Gift Handlers
    if data == "admin_gift_start": await admin_gift_start(update, context); return
    if data.startswith("gift_amt_"): await admin_gift_amount(update, context); return
    if data == "admin_gift_cancel": 
        await q.message.edit_text("❌ Бекор шуд.")
        context.user_data["awaiting_gift_id"] = False
        return

    if data == "back_main":
        await q.answer()
        await show_main_menu(q.message.chat, uid); return

    await q.answer()

# ===================== MAIN =====================
def main():
    if not TOKEN or TOKEN == "PASTE_YOUR_TOKEN_HERE":
        print("⚠️ Please set your bot token in UCSTORE_BOT_TOKEN env var or in TOKEN variable.")
    
    # БОРГИРИИ БАЗАИ МАЪЛУМОТ ПЕШ АЗ ОҒОЗ
    load_database()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", lambda u, c: u.message.reply_text(admin_info(str(u.effective_user.id)))))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("/start /about /help")))

    app.add_handler(MessageHandler(filters.CONTACT, get_contact))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.PHOTO, bc_photo_handler), group=0)
    app.add_handler(MessageHandler((filters.PHOTO | filters.Document.ALL) & (~filters.COMMAND), receive_proof), group=1)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text), group=2)

    print("✅ UCstore бо database фаъол шуд )")
    app.run_polling()

if __name__ == "__main__":
    main()
