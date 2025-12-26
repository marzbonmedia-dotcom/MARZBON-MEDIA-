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

# ===================== CONFIG =====================
TOKEN = "8524676045:AAE7Eb_BDZKaB98-SHis2t4Pdrjgi-UodzY"
ADMIN_IDS = [8436218638]

ADMIN_TELEGRAM = "https://t.me/MARZBON_TJ"
ADMIN_INSTAGRAM = "https://www.instagram.com/marzbontj?igsh=MW9yaG9lcm93YjRueA=="

FREE_UC_CHANNEL = "@marzbon_media" 
VISA_NUMBER = "4439200020432471"
SBER_NUMBER = "2202208496090011"

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

ADMIN_INFO = (
    """UCstore — ин боти расмии фурӯши UC барои PUBG Mobile ва дигар хидматҳои рақамии бозӣ мебошад. Мо барои бозингарони тоҷик платформаи боэътимод, босифат ва осонро фароҳам овардаем, то харид кардан осон, бехатар ва зуд сурат гирад. ⚡️

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

Инчунин дар бораи тамоми мушкилот шумо ҳамеша метавонед ба админ тамос гиред @MARZBON_TJ"""
)

# ===================== DATA (RAM ONLY) =====================
users_data = {}         
orders = []             
user_carts = {}         
user_wishlist = {}      
broadcast_draft = {}    

# ===================== HELPERS =====================
def is_admin(uid: int) -> bool:
    return uid in ADMIN_IDS

def now_str() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def anti_spam(context: ContextTypes.DEFAULT_TYPE, delay: float = 1.5) -> bool:
    """Агар корбар тез-тез клик кунад, False бармегардонад."""
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
    return o

def find_order(order_id: int):
    for o in orders:
        if o.get("id") == order_id:
            return o
    return None

async def show_main_menu(chat, user_id: str):
    kb = [
        ["🛍 Маҳсулот", "❤️ Дилхоҳҳо"],
        ["🛒 Сабад", "💬 Профили админ"],
        ["ℹ Маълумот", "🎁 UC ройгон"],
    ]
    if is_admin(int(user_id)):
        kb.append(["👑 Панели админ"])
    await chat.send_message("Менюи асосӣ:", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

# ===================== MATH CHALLENGE =====================
async def start_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Санҷиш: оё корбар блок аст?
    blocked_until = context.user_data.get("math_blocked_until")
    if blocked_until:
        if dt.datetime.now() < blocked_until:
            diff = blocked_until - dt.datetime.now()
            minutes_left = int(diff.total_seconds() // 60) + 1
            await update.effective_chat.send_message(
                f"🚫 Шумо блок шудед! Лутфан пас аз {minutes_left} дақиқа дубора кӯшиш кунед."
            )
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

    await update.effective_chat.send_message(
        f"🔐 Санҷиш: {expr} = ?\n(фақат рақам)\nШумо 3 кӯшиш доред."
    )

async def check_math(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not context.user_data.get("awaiting_math"):
        # Санҷиши блок ҳангоми навиштан
        blocked_until = context.user_data.get("math_blocked_until")
        if blocked_until and dt.datetime.now() < blocked_until:
             diff = blocked_until - dt.datetime.now()
             minutes_left = int(diff.total_seconds() // 60) + 1
             await update.message.reply_text(f"⏳ Шумо блок ҳастед. {minutes_left} дақиқаи дигар сабр кунед.")
             return True
        return False

    txt = (update.message.text or "").strip()
    try:
        val = int(txt)
    except:
        val = None 

    if val is not None and val == context.user_data.get("math_ans"):
        context.user_data["awaiting_math"] = False
        context.user_data["math_blocked_until"] = None
        await update.message.reply_text("✅ Офарин! Санҷиш гузашт.")
        await show_main_menu(update.effective_chat, str(update.effective_user.id))
        return True

    context.user_data["math_try"] += 1
    left = 3 - context.user_data["math_try"]

    if left > 0:
        await update.message.reply_text(f"❌ Нодуруст. {left} кӯшиш монд.")
    else:
        context.user_data["awaiting_math"] = False
        context.user_data["math_blocked_until"] = dt.datetime.now() + dt.timedelta(minutes=10)
        await update.message.reply_text(
            "🚫 Шумо 3 маротиба хато кардед!\n"
            "Дастрасӣ барои 10 дақиқа маҳдуд шуд."
        )
    return True

# ===================== START / REGISTER =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    # 1. Агар корбар аллакай бошад -> РОСТ БА МЕНЮ (дигар санҷиш нест)
    if uid in users_data:
        # Танҳо агар блок набошад
        blocked_until = context.user_data.get("math_blocked_until")
        if blocked_until and dt.datetime.now() < blocked_until:
             diff = blocked_until - dt.datetime.now()
             minutes_left = int(diff.total_seconds() // 60) + 1
             await update.message.reply_text(f"🚫 Шумо блок ҳастед. {minutes_left} дақиқа сабр кунед.")
             return
        
        # Агар корбар дар ҷараёни санҷиш монда бошад, онро лағв мекунем ва меню медиҳем
        context.user_data["awaiting_math"] = False
        await show_main_menu(update.effective_chat, uid)
        return

    # Payload for invite
    args = context.args
    if args and args[0].startswith("invite_"):
        inviter = args[0].split("_", 1)[1]
        if inviter and inviter != uid:
            context.user_data["invited_by"] = inviter

    btn = KeyboardButton("📱 Ворид шудан бо рақам", request_contact=True)
    await update.message.reply_text(
        "🔐 Барои истифодаи бот рақами телефони худро фиристед:",
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
        }

        inviter = context.user_data.get("invited_by")
        if inviter and inviter in users_data and inviter != uid:
            users_data[inviter]["free_uc"] = users_data[inviter].get("free_uc", 0) + 2
            try:
                await context.bot.send_message(int(inviter), "🎉 Барои даъват 2 UC гирифтед!")
            except:
                pass

        for admin in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin,
                    f"👤 Корбари нав!\n{u.first_name} | {phone}\n@{u.username}"
                )
            except:
                pass

    await update.message.reply_text(
        "✅ Сабт шудед!\n🎁 10 UC бонус гирифтед.",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Санҷиш ТАНҲО дар вақти сабти ном
    await start_math(update, context)

# ===================== CATALOG & ACTIONS =====================
async def catalog_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message or (update.callback_query and update.callback_query.message)
    if not target:
        return
    kb = [
        [InlineKeyboardButton("🪙 UC харидан", callback_data="catalog_uc")],
        [InlineKeyboardButton("🎫 Функсияҳои дигар", callback_data="catalog_voucher")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back_main")],
    ]
    await target.reply_text("🛍 Маҳсулот: интихоб кунед", reply_markup=InlineKeyboardMarkup(kb))

async def catalog_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rows = []
    row = []
    for i, item in ITEMS.items():
        row.append(InlineKeyboardButton(f"{item['name']} — {item['price']} TJS", callback_data=f"select_{i}"))
        if len(row) == 2:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")])
    await q.message.edit_text("🪙 Рӯйхати UC:", reply_markup=InlineKeyboardMarkup(rows))

async def catalog_voucher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rows = []
    for i, item in VOUCHERS.items():
        rows.append([InlineKeyboardButton(f"{item['name']} — {item['price']} TJS", callback_data=f"select_{i}")])
    rows.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")])
    await q.message.edit_text("🎫 Рӯйхати дигарҳо:", reply_markup=InlineKeyboardMarkup(rows))

async def select_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    try:
        item_id = int(q.data.split("_", 1)[1])
    except:
        return
    item = get_item(item_id)
    if not item:
        await q.message.reply_text("⚠️ Маҳсулот ёфт нашуд.")
        return
    kb = [
        [
            InlineKeyboardButton("🛒 Ба сабад", callback_data=f"addcart_{item_id}"),
            InlineKeyboardButton("❤️ Ба дилхоҳҳо", callback_data=f"addwish_{item_id}"),
        ],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")]
    ]
    await q.message.reply_text(f"{item_label(item_id)} • {item['name']} — {item['price']} TJS", reply_markup=InlineKeyboardMarkup(kb))

# ===================== WISHLIST =====================
async def add_wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try:
        item_id = int(q.data.split("_", 1)[1])
    except:
        return
    if not get_item(item_id):
        return
    user_wishlist.setdefault(uid, set()).add(item_id)
    await q.message.reply_text("❤️ Ба дилхоҳҳо илова шуд!")

async def show_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    w = user_wishlist.get(uid, set())
    if not w:
        await update.message.reply_text("❤️ Дилхоҳҳо холист.")
        return
    for item_id in list(w):
        item = get_item(item_id)
        if not item:
            continue
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("🛒 Ба сабад", callback_data=f"addcart_{item_id}"),
            InlineKeyboardButton("🗑️ Пок", callback_data=f"removewish_{item_id}")
        ]])
        await update.message.reply_text(f"❤️ {item['name']} — {item['price']} TJS", reply_markup=kb)

async def remove_wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🗑️ Пок шуд!")
    uid = str(q.from_user.id)
    try:
        item_id = int(q.data.split("_", 1)[1])
    except:
        return
    if uid in user_wishlist:
        user_wishlist[uid].discard(item_id)
    try:
        await q.message.delete()
    except:
        pass

# ===================== CART =====================
async def add_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try:
        item_id = int(q.data.split("_", 1)[1])
    except:
        return
    item = get_item(item_id)
    if not item:
        await q.message.reply_text("⚠️ Маҳсулот ёфт нашуд.")
        return
    user_carts.setdefault(uid, {})
    user_carts[uid][item_id] = user_carts[uid].get(item_id, 0) + 1
    await q.message.reply_text(f"✅ {item['name']} ба сабад илова шуд!")

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    user_carts[uid] = {}
    await q.message.reply_text("🗑️ Сабад пок шуд.")

async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    cart = user_carts.get(uid, {})
    if not cart:
        await update.message.reply_text("🛒 Сабад холист.")
        return

    total = 0
    txt = "🛒 Сабади шумо:\n"
    for item_id, qty in cart.items():
        note = get_item(item_id)
        if not note:
            continue
        subtotal = note["price"] * qty
        total += subtotal
        txt += f"- {note['name']} x{qty} = {subtotal} TJS\n"
    txt += f"\n💰 Ҳамагӣ: {total} TJS"

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Фармоиш", callback_data="checkout"),
         InlineKeyboardButton("🗑️ Пок", callback_data="clear_cart")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back_main")]
    ])
    await update.message.reply_text(txt, reply_markup=kb)

# ===================== CHECKOUT / PAYMENT =====================
async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    cart = user_carts.get(uid, {})
    if not cart:
        await q.message.reply_text("🛒 Сабад холист.")
        return

    context.user_data["awaiting_game_id"] = True
    context.user_data["pending_items"] = dict(cart)
    await q.message.reply_text("🎮 ID-и бозиро ворид кунед (8–15 рақам):")

async def handle_game_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_id = (update.message.text or "").strip()
    if not game_id.isdigit() or not (8 <= len(game_id) <= 15):
        await update.message.reply_text("⚠️ ID хатост (8–15 рақам). Дубора ворид кунед:")
        return

    uid = str(update.effective_user.id)
    items = context.user_data.get("pending_items") or {}
    if not items:
        context.user_data["awaiting_game_id"] = False
        await update.message.reply_text("⚠️ Сабад холист.")
        return

    total = 0
    for item_id, qty in items.items():
        it = get_item(int(item_id))
        if it:
            total += it["price"] * int(qty)

    order = create_order(uid, total, items, game_id)

    user_carts[uid] = {}
    context.user_data["awaiting_game_id"] = False
    context.user_data.pop("pending_items", None)

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 VISA", callback_data=f"pay_visa_{order['id']}")],
        [InlineKeyboardButton("🏦 SberBank", callback_data=f"pay_sber_{order['id']}")],
    ])
    await update.message.reply_text(
        f"📦 Фармоиш №{order['id']}\n"
        f"🎮 ID: {game_id}\n"
        f"💰 Ҳамагӣ: {total} TJS\n\n"
        "Тарзи пардохтро интихоб кунед:",
        reply_markup=kb
    )

async def choose_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.split("_")
    method = parts[1]
    order_id = int(parts[2])

    order = find_order(order_id)
    if not order:
        await q.message.reply_text("⚠️ Фармоиш ёфт нашуд.")
        return

    if str(q.from_user.id) != str(order["user_id"]):
        await q.message.reply_text("⚠️ Ин фармоиш барои шумо нест.")
        return

    order["status"] = "awaiting_proof"
    order["payment_method"] = "VISA" if method == "visa" else "SberBank"
    card = VISA_NUMBER if method == "visa" else SBER_NUMBER

    context.user_data["awaiting_proof_order"] = order_id

    await q.message.reply_text(
        f"💳 Тарзи пардохт: {order['payment_method']}\n"
        f"📌 Рақами корт: {card}\n\n"
        "✅ Пас аз пардохт квитанцияро ҳамчун акс ё файл фиристед."
    )

async def receive_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    order_id = context.user_data.get("awaiting_proof_order")
    if not order_id:
        return
    order = find_order(int(order_id))
    if not order or order.get("status") != "awaiting_proof":
        return

    file_id = None
    is_photo = False
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        is_photo = True
    elif update.message.document:
        file_id = update.message.document.file_id
        is_photo = False
    else:
        return

    order["proof_file"] = file_id
    order["status"] = "proof_sent"
    context.user_data.pop("awaiting_proof_order", None)

    items_txt = ""
    for item_id, qty in (order.get("items") or {}).items():
        item_id = int(item_id)
        it = get_item(item_id)
        if it:
            items_txt += f"{item_label(item_id)}: {it['name']} x{qty}\n"

    caption = (
        f"📦 Фармоиш №{order['id']}\n"
        f"👤 @{order.get('username') or order.get('user_name')}\n"
        f"🎮 ID: {order.get('game_id')}\n\n"
        f"{items_txt}\n"
        f"💰 Ҳамагӣ: {order.get('total')} TJS\n"
        f"💳 Пардохт: {order.get('payment_method')}\n"
        f"📱 Телефон: {order.get('phone') or '—'}\n"
        f"🕒 {order.get('time')}"
    )

    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Тасдиқ", callback_data=f"admin_pay_confirm_{order['id']}"),
        InlineKeyboardButton("❌ Рад", callback_data=f"admin_pay_reject_{order['id']}"),
    ]])

    for admin in ADMIN_IDS:
        try:
            if is_photo:
                await context.bot.send_photo(admin, photo=file_id, caption=caption, reply_markup=buttons)
            else:
                await context.bot.send_document(admin, document=file_id, caption=caption, reply_markup=buttons)
        except:
            pass

    await update.message.reply_text("✅ Квитанция қабул шуд. Мунтазир шавед, админ месанҷад.")

async def admin_pay_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.message.reply_text("🚫 Танҳо админ!")
        return

    parts = q.data.split("_")
    action = parts[2]
    order_id = int(parts[3])

    order = find_order(order_id)
    if not order:
        await q.message.reply_text("Фармоиш ёфт нашуд.")
        return

    if action == "confirm":
        order["status"] = "confirmed"
        txt_user = f"✅ Фармоиши №{order_id} тасдиқ шуд. Ташаккур!"
        txt_admin = f"✅ Тасдиқ шуд: №{order_id}"
    else:
        order["status"] = "rejected"
        txt_user = f"❌ Фармоиши №{order_id} рад шуд. Лутфан бо админ тамос гиред."
        txt_admin = f"❌ Рад шуд: №{order_id}"

    try:
        await context.bot.send_message(int(order["user_id"]), txt_user)
    except:
        pass
    await q.message.reply_text(txt_admin)

# ===================== FREE UC =====================
async def free_uc_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    uid = str(update.effective_user.id)

    if uid not in users_data:
        await chat.send_message("⚠️ Аввал /start кунед.")
        return

    subscribed = False
    try:
        member = await context.bot.get_chat_member(FREE_UC_CHANNEL, int(uid))
        subscribed = member.status in ["member", "administrator", "creator"]
    except:
        subscribed = False

    if not subscribed:
        await chat.send_message(
            "📢 Барои гирифтани UC ройгон, аввал ба канал обуна шавед:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Канал", url=f"https://t.me/{FREE_UC_CHANNEL.lstrip('@')}")],
                [InlineKeyboardButton("🔄 Санҷиш", callback_data="check_sub")],
            ])
        )
        return

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 UC рӯзона (1–5)", callback_data="daily_uc")],
        [InlineKeyboardButton("📊 UC-и ман", callback_data="my_uc")],
        [InlineKeyboardButton("🎁 60 UC", callback_data="claim_60"),
         InlineKeyboardButton("🎁 325 UC", callback_data="claim_325")],
        [InlineKeyboardButton("🔗 Даъвати дӯстон", callback_data="invite_link")]
    ])
    await chat.send_message("🎁 Менюи UC ройгон:", reply_markup=kb)

async def daily_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    u = users_data.get(uid)
    if not u:
        await q.message.reply_text("⚠️ /start кунед.")
        return

    now = dt.datetime.now()
    last = u.get("last_daily_uc")
    if last:
        try:
            last_dt = dt.datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
            if (now - last_dt).total_seconds() < 24 * 3600:
                left_hours = int((24*3600 - (now-last_dt).total_seconds()) // 3600)
                await q.message.reply_text(f"⏳ Ҳоло намешавад. Боз {left_hours} соат мондааст.")
                return
        except:
            pass

    roll = random.choices([1,2,3,4,5], weights=[70,20,7,2,1])[0]
    u["free_uc"] = u.get("free_uc", 0) + roll
    u["last_daily_uc"] = now_str()
    await q.message.reply_text(f"🎉 Шумо {roll} UC гирифтед! Ҳамагӣ: {u['free_uc']} UC")

async def my_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    u = users_data.get(uid, {})
    await q.message.reply_text(f"📊 Шумо доред: {u.get('free_uc', 0)} UC")

async def claim_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    need = 60 if q.data == "claim_60" else 325
    uid = str(q.from_user.id)
    u = users_data.get(uid, {})
    if u.get("free_uc", 0) < need:
        await q.message.reply_text("❌ UC кофӣ нест.")
        return
    context.user_data["awaiting_free_claim"] = need
    await q.message.reply_text("🎮 ID-и PUBG-ро ворид кунед (8–15 рақам):")

async def handle_free_claim_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_id = (update.message.text or "").strip()
    if not game_id.isdigit() or not (8 <= len(game_id) <= 15):
        await update.message.reply_text("⚠️ ID хатост (8–15 рақам). Дубора ворид кунед:")
        return

    uid = str(update.effective_user.id)
    need = context.user_data.pop("awaiting_free_claim", None)
    if not need:
        return

    u = users_data.get(uid)
    if not u or u.get("free_uc", 0) < need:
        await update.message.reply_text("❌ UC кофӣ нест.")
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

    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Тасдиқ", callback_data=f"admin_free_confirm_{order_id}"),
        InlineKeyboardButton("❌ Рад", callback_data=f"admin_free_reject_{order_id}"),
    ]])

    for admin in ADMIN_IDS:
        try:
            await context.bot.send_message(
                admin,
                f"🎁 UC Ройгон №{order_id}\n"
                f"👤 @{u.get('username') or '—'}\n"
                f"🎮 ID: {game_id}\n"
                f"Пакет: {need} UC",
                reply_markup=btn
            )
        except:
            pass

    await update.message.reply_text(f"✅ Дархост фиристода шуд! №{order_id}")

async def admin_free_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.message.reply_text("🚫 Танҳо админ!")
        return

    parts = q.data.split("_")
    action = parts[2]
    order_id = int(parts[3])

    o = find_order(order_id)
    if not o or o.get("type") != "free_uc":
        await q.message.reply_text("Фармоиш ёфт нашуд.")
        return

    if action == "confirm":
        o["status"] = "confirmed"
        msg_user = f"✅ UC ройгон (№{order_id}) тасдиқ шуд!"
        msg_admin = "✅ Тасдиқ шуд."
    else:
        o["status"] = "rejected"
        msg_user = f"❌ UC ройгон (№{order_id}) рад шуд. Бо админ тамос гиред."
        msg_admin = "❌ Рад шуд."

    try:
        await context.bot.send_message(int(o["user_id"]), msg_user)
    except:
        pass
    await q.message.reply_text(msg_admin)

async def invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    try:
        me = await context.bot.get_me()
        link = f"https://t.me/{me.username}?start=invite_{uid}"
        await q.message.reply_text(f"🔗 Линки даъват:\n{link}\n\nҲар даъват → 2 UC")
    except:
        await q.message.reply_text("⚠️ Хато шуд.")

# ===================== BROADCAST =====================
async def bc_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.message.reply_text("🚫 Танҳо админ!")
        return

    aid = str(q.from_user.id)
    broadcast_draft[aid] = {"text": "", "photo": None, "buttons": [], "step": None}

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Матн", callback_data="bc_text")],
        [InlineKeyboardButton("🔘 Тугма", callback_data="bc_button")],
        [InlineKeyboardButton("🖼 Акс", callback_data="bc_photo")],
        [InlineKeyboardButton("📤 Ирсол", callback_data="bc_send")],
        [InlineKeyboardButton("❌ Бекор", callback_data="bc_cancel")],
    ])
    await q.message.reply_text("📢 Broadcast меню:", reply_markup=kb)

async def bc_set_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.setdefault(aid, {"text":"", "photo":None, "buttons":[], "step":None})
    broadcast_draft[aid]["step"] = "text"
    await q.message.reply_text("✏️ Матни паёмро навис:")

async def bc_set_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.setdefault(aid, {"text":"", "photo":None, "buttons":[], "step":None})
    broadcast_draft[aid]["step"] = "button"
    await q.message.reply_text("🔘 Формат:\nМатн | https://link")

async def bc_set_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.setdefault(aid, {"text":"", "photo":None, "buttons":[], "step":None})
    broadcast_draft[aid]["step"] = "photo"
    await q.message.reply_text("🖼 Аксеро фирист:")

async def bc_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return

    aid = str(q.from_user.id)
    d = broadcast_draft.get(aid)
    if not d:
        await q.message.reply_text("❌ Draft нест.")
        return

    kb = None
    if d.get("buttons"):
        kb = InlineKeyboardMarkup([d["buttons"]])

    sent = 0
    for uid in list(users_data.keys()):
        try:
            if d.get("photo"):
                await context.bot.send_photo(int(uid), photo=d["photo"], caption=d.get("text",""), reply_markup=kb)
            else:
                await context.bot.send_message(int(uid), text=d.get("text",""), reply_markup=kb)
            sent += 1
        except:
            pass

    broadcast_draft.pop(aid, None)
    await q.message.reply_text(f"✅ Ирсол шуд. Ба {sent} корбар.")

async def bc_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    aid = str(q.from_user.id)
    broadcast_draft.pop(aid, None)
    await q.message.reply_text("❌ Бекор шуд.")

async def bc_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return
    uid = str(update.effective_user.id)
    d = broadcast_draft.get(uid)
    if not d or d.get("step") != "photo":
        return
    d["photo"] = update.message.photo[-1].file_id
    d["step"] = None
    await update.message.reply_text("✅ Акс сабт шуд.")

# ===================== ADMIN PANEL =====================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Корбарон", callback_data="admin_users")],
        [InlineKeyboardButton("📦 Заказҳо", callback_data="admin_orders")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="bc_menu")],
        [InlineKeyboardButton("🗑 Пок кардани корбарон", callback_data="admin_clear_confirm")],
    ])
    await update.message.reply_text("👑 Панели админ:", reply_markup=kb)

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return
    if not users_data:
        await q.message.reply_text("Ҳоло корбар нест.")
        return
    txt = "👤 Корбарон (20-то):\n\n"
    c = 0
    for uid, u in users_data.items():
        txt += f"- {u.get('name','—')} | {u.get('phone','—')} | id:{uid}\n"
        c += 1
        if c >= 20:
            if len(users_data) > 20:
                txt += "\n... дигарон ҳам ҳаст"
            break
    await q.message.reply_text(txt)

async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return
    if not orders:
        await q.message.reply_text("Ҳоло заказ нест.")
        return
    txt = "📦 Охирин 15 заказ:\n\n"
    for o in orders[-15:]:
        if o.get("type") == "free_uc":
            txt += f"#{o['id']} | FREE {o.get('pack')}UC | {o.get('status')}\n"
        else:
            txt += f"#{o['id']} | {o.get('total')}TJS | {o.get('status')}\n"
    await q.message.reply_text(txt)

async def admin_clear_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Ҳа, пок кун", callback_data="admin_clear_do")],
        [InlineKeyboardButton("❌ Не", callback_data="admin_clear_no")],
    ])
    await q.message.reply_text("⚠️ Ҳамаи корбарон тоза мешаванд. Давом медиҳед?", reply_markup=kb)

async def admin_clear_do(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return
    n = len(users_data)
    users_data.clear()
    orders.clear()
    user_carts.clear()
    user_wishlist.clear()
    await q.message.reply_text(f"🗑 Пок шуд: {n} корбар.")

async def admin_clear_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("✅ Бекор шуд.")

# ===================== MAIN HANDLER ROUTER =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    
    # --- ANTI SPAM CHECK FOR TEXT ---
    if not anti_spam(context):
        await update.message.reply_text("⏳ Лутфан тез-тез нанависед. 1-2 сония сабр кунед.")
        return

    # --- BLOCK CHECK FOR ALL MESSAGES ---
    blocked_until = context.user_data.get("math_blocked_until")
    if blocked_until:
        if dt.datetime.now() < blocked_until:
            diff = blocked_until - dt.datetime.now()
            minutes_left = int(diff.total_seconds() // 60) + 1
            await update.message.reply_text(
                f"🚫 Шумо муваққатан блок ҳастед.\n⏰ {minutes_left} дақиқаи дигар интизор шавед."
            )
            return
        else:
            context.user_data["math_blocked_until"] = None

    # 1) Math challenge active
    if context.user_data.get("awaiting_math"):
        consumed = await check_math(update, context)
        if consumed:
            return

    # 2) Paid Checkout ID
    if context.user_data.get("awaiting_game_id"):
        await handle_game_id(update, context)
        return

    # 3) Free UC ID
    if context.user_data.get("awaiting_free_claim"):
        await handle_free_claim_id(update, context)
        return

    # 4) Broadcast draft steps
    uid = str(update.effective_user.id)
    d = broadcast_draft.get(uid)
    if d and d.get("step") == "text":
        d["text"] = update.message.text
        d["step"] = None
        await update.message.reply_text("✅ Матн сабт шуд.")
        return
    if d and d.get("step") == "button":
        try:
            bt, url = update.message.text.split("|", 1)
            d["buttons"].append(InlineKeyboardButton(bt.strip(), url=url.strip()))
            await update.message.reply_text("✅ Тугма илова шуд.")
        except:
            await update.message.reply_text("❌ Формат нодуруст.\nНамуна:\nМатн | https://link")
        d["step"] = None
        return

    # 5) Main Menu
    text = update.message.text
    user_id = str(update.effective_user.id)

    if text == "🛍 Маҳсулот":
        await catalog_menu(update, context)
    elif text == "❤️ Дилхоҳҳо":
        await show_wishlist(update, context)
    elif text == "🛒 Сабад":
        await show_cart(update, context)
    elif text == "ℹ Маълумот":
        await update.message.reply_text(ADMIN_INFO)
    elif text == "🎁 UC ройгон":
        await free_uc_menu(update, context)
    elif text == "💬 Профили админ":
        await update.message.reply_text(
            "Админ:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✈️ Telegram", url=ADMIN_TELEGRAM)],
                [InlineKeyboardButton("📸 Instagram", url=ADMIN_INSTAGRAM)],
            ])
        )
    elif text == "👑 Панели админ" and is_admin(int(user_id)):
        await admin_panel(update, context)
    else:
        await update.message.reply_text("🤖 Аз меню истифода баред.")

# ===================== CALLBACK ROUTER =====================
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if not q or not q.data:
        return
    
    # --- ANTI SPAM CHECK FOR BUTTONS ---
    if not anti_spam(context, delay=1.2):
        await q.answer("⏳ Лутфан 1-2 сония сабр кунед!", show_alert=True)
        return

    # Check block for buttons too
    blocked_until = context.user_data.get("math_blocked_until")
    if blocked_until and dt.datetime.now() < blocked_until:
         await q.answer("🚫 Шумо блок ҳастед!", show_alert=True)
         return

    data = q.data

    # catalog
    if data == "catalog_uc":
        await catalog_uc(update, context); return
    if data == "catalog_voucher":
        await catalog_voucher(update, context); return
    if data == "catalog_back":
        await catalog_menu(update, context); return
    if data.startswith("select_"):
        await select_item(update, context); return

    # wishlist/cart
    if data.startswith("addwish_"):
        await add_wish(update, context); return
    if data.startswith("removewish_"):
        await remove_wish(update, context); return
    if data.startswith("addcart_"):
        await add_cart(update, context); return
    if data == "clear_cart":
        await clear_cart(update, context); return

    # checkout/payment
    if data == "checkout":
        await checkout(update, context); return
    if data.startswith(("pay_visa_", "pay_sber_")):
        await choose_payment(update, context); return

    # admin payment actions
    if data.startswith("admin_pay_confirm_") or data.startswith("admin_pay_reject_"):
        await admin_pay_action(update, context); return

    # free uc
    if data == "check_sub":
        await q.answer()
        await free_uc_menu(update, context); return
    if data == "daily_uc":
        await daily_uc(update, context); return
    if data == "my_uc":
        await my_uc(update, context); return
    if data in ("claim_60", "claim_325"):
        await claim_btn(update, context); return
    if data == "invite_link":
        await invite_link(update, context); return
    if data.startswith("admin_free_confirm_") or data.startswith("admin_free_reject_"):
        await admin_free_action(update, context); return

    # broadcast
    if data == "bc_menu":
        await bc_menu(update, context); return
    if data == "bc_text":
        await bc_set_text(update, context); return
    if data == "bc_button":
        await bc_set_button(update, context); return
    if data == "bc_photo":
        await bc_set_photo(update, context); return
    if data == "bc_send":
        await bc_send(update, context); return
    if data == "bc_cancel":
        await bc_cancel(update, context); return

    # admin panel
    if data == "admin_users":
        await admin_users(update, context); return
    if data == "admin_orders":
        await admin_orders(update, context); return
    if data == "admin_clear_confirm":
        await admin_clear_confirm(update, context); return
    if data == "admin_clear_do":
        await admin_clear_do(update, context); return
    if data == "admin_clear_no":
        await admin_clear_no(update, context); return

    # back
    if data == "back_main":
        await q.answer()
        await show_main_menu(q.message.chat, str(q.from_user.id)); return

    await q.answer()

# ===================== MAIN =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", lambda u, c: u.message.reply_text(ADMIN_INFO)))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("/start /about /help")))

    app.add_handler(MessageHandler(filters.CONTACT, get_contact))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.PHOTO, bc_photo_handler), group=0)
    app.add_handler(MessageHandler((filters.PHOTO | filters.Document.ALL) & (~filters.COMMAND), receive_proof), group=1)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text), group=2)

    print("✅ UCstore FULL (botifyhost safe) started")
    app.run_polling()

if __name__ == "__main__":
    main()
