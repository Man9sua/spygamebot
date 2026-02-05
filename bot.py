import html
import os
import random
import threading
import telebot
from telebot import types


BOT_TOKEN = os.getenv("BOT_TOKEN") or "8382682504:AAErIB11GWaGJDfn4YRlu6hpQC1dAVsDRng"
BOT_USERNAME = os.getenv('BOT_USERNAME') or "@altairotdaimestovpervoigruppebot"

bot = telebot.TeleBot(BOT_TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not BOT_USERNAME:
    try:
        BOT_USERNAME = bot.get_me().username
    except Exception:
        BOT_USERNAME = None
if BOT_USERNAME:
    BOT_USERNAME = BOT_USERNAME.strip().lstrip("@")

GROUP_GAMES = {}
USER_TO_GROUP = {}

GROUP_RANDOM_SCENARIO_WEIGHTS = [
    ("classic", 90),
    ("opposite", 10),
]

CHANGELOG = [
    {
        "version": "1.1.0",
        "added": [
            "Групповой режим с подбором, настройкой и голосованиями",
            "Гайд /help и кнопка «Гайд»",
            "Команда /log с историей версий",
        ],
        "fixed": [
            "Блокировка спама в ролях и в группе",
            "Корректные пути к изображениям",
        ],
    },
    {
        "version": "1.0.0",
        "added": [
            "Режим «1 телефон» с раздачей ролей",
            "Темы: Өзімізғо / JJS / Clash Royale",
            "Сценарии и логика шпионов/мирных",
        ],
        "fixed": [],
    },
]

HELP_PAGES = [
    (
        "📘 <b>Гайд: старт</b>\n\n"
        "<b>Команды (личные сообщения):</b>\n"
        "<code>/start</code> — старт бота\n"
        "<code>/help</code> — этот гайд\n"
        "<code>/log</code> — список версий\n\n"
        "<b>Команды в группе:</b>\n"
        "<code>/s</code> — начать подбор участников\n"
        "<code>/stop</code> — остановить подбор/игру (только создатель)\n"
        "<code>/game</code> — досрочно запустить игру (если ≥ 3 игроков)\n"
        "<code>/answer &lt;название карты&gt;</code> — попытка шпиона угадать карту\n\n"
        "⚠️ <i>Важно: для группового режима бот должен быть администратором.</i>"
    ),
    (
        "🎭 <b>Гайд: сценарии в группе</b>\n\n"
        "<b>Классический</b> — мирные + шпионы.\n"
        "Количество шпионов выбирает создатель.\n\n"
        "<b>Рандомный</b> — сценарий выбирается автоматически.\n"
        "В групповом режиме шансы:\n"
        "• Классический — 90%\n"
        "• Наоборот — 10%\n\n"
        "<b>Наоборот</b> — один мирный, остальные шпионы."
    ),
    (
        "🧩 <b>Гайд: как проходит игра в группе</b>\n\n"
        "1) Создатель запускает <code>/s</code>.\n"
        "2) Игроки жмут «Присоединиться».\n"
        "3) После набора — выбор темы/сценария.\n"
        "4) Роли выдаются в ЛС.\n"
        "5) Раунды, обсуждения и голосования.\n\n"
        "💡 <i>Если игрок не может писать — проверьте права бота.</i>"
    ),
    (
        "🎲 <b>Гайд: сценарии в «1 телефон»</b>\n\n"
        "<b>Классический</b> — мирные + шпионы.\n"
        "Количество шпионов выбирается вручную.\n\n"
        "<b>Рандомный</b> — бот сам выбирает сценарий:\n"
        "• Классический — 70%\n"
        "• Все шпионы — 5%\n"
        "• Все мирные — 5%\n"
        "• Хаос — 10%\n"
        "• Наоборот — 10%\n\n"
        "<b>Хаос</b> — у каждого своя карта в одной теме.\n"
        "<b>Наоборот</b> — один мирный, остальные шпионы."
    ),
]

# Темы (можно ещё добавлять карты отсюда)
THEMES = {
    "ozimizgo": {
        "label": "Өзімізғо",
        "cards": [
            "Дулат ағай",
            "Асель апай",
            "Абинаус Архат",
            "Арынғазы Айғаным",
            "Базархан Ғания",
            "Болат Арманжан",
            "Нығыметбек Мансұр",
            "Садыр Қайсар",
            "Төлепберген Расул",
            "Хамидулла Әлтаир",
            "Алибек Абдуррахман",
            "Беринов Санжар",
            "Ержан Жанасыл",
            "Жылқышиев Ақжол",
            "Кульжанов Асанали",
            "Медел Абылай",
            "Нұрланұлы Әли",
            "Рысбек Сымбат",
            "Хасейнқызы Гүлнәз",
            "Шакар Фатихсултан Ариф",
            "Досжан Мақсат",
            "Досымбек Асанали",
        ],
        "images_dir": None,
    },
    "jjs": {
        "label": "JJS",
        "cards": [
            ("Honored One", "jjs/ho.jpg"),
            ("Vessel", "jjs/v.jpg"),
            ("Restless Gambler", "jjs/rg.jpg"),
            ("Ten Shadows", "jjs/ts.jpg"),
            ("Perfection", "jjs/p.jpg"),
            ("Blood Manipulator", "jjs/bm.jpg"),
            ("Switcher", "jjs/sw.jpg"),
            ("Defence Attorney", "jjs/da.jpg"),
            ("Cursed Partners", "jjs/cp.jpg"),
            ("Puppet Master", "jjs/pm.jpg"),
            ("Head of the Hei", "jjs/hoth.jpg"),
            ("Salaryman", "jjs/s.jpg"),
            ("Locust Guy", "jjs/lg.jpg"),
            ("Star Rage", "jjs/sr.jpg"),
            ("Aspiring Mangaka", "jjs/am.jpg"),
            ("Strongest of History", "jjs/soh.jpg"),
        ],
        "images_dir": "spygame",
    },
    "cr": {
        "label": "Clash Royal",
        "cards": [
            ("Three musketeers", "cr/3mush.webp"),
            ("Archer queen", "cr/archerqueen.webp"),
            ("Balloon", "cr/balloon.webp"),
            ("Bandit", "cr/bandit.webp"),
            ("Barbarian barrel", "cr/barbarianbarrel.webp"),
            ("Barbarians", "cr/barbarians.webp"),
            ("Berserker", "cr/berserker.webp"),
            ("Bowler", "cr/bowler.webp"),
            ("Clone", "cr/clone.webp"),
            ("Dark prince", "cr/darkprince.webp"),
            ("Dart goblin", "cr/dartgob.webp"),
            ("Elixir", "cr/elixir.webp"),
            ("Electro spirit", "cr/espirit.webp"),
            ("Electro wizard", "cr/ewizard.webp"),
            ("Firecracker", "cr/firecracker.webp"),
            ("Fisherman", "cr/fisherman.webp"),
            ("Flying machine", "cr/flyingmachine.webp"),
            ("Freeze", "cr/freeze.webp"),
            ("Giant skeleton", "cr/giantskeleton.webp"),
            ("Goblin cage", "cr/gobcage.webp"),
            ("Goblin drill", "cr/gobdrill.webp"),
            ("Goblin hunt", "cr/gobhunt.webp"),
            ("Goblin machine", "cr/gobmachine.webp"),
            ("Goblins", "cr/gobs.webp"),
            ("Goblinstein", "cr/gobstein.webp"),
            ("Golden knight", "cr/goldenknight.webp"),
            ("Golem", "cr/golem.webp"),
            ("Graveyard", "cr/graveyard.webp"),
            ("Hog Rider", "cr/hog.webp"),
            ("Ice golem", "cr/icegolem.webp"),
            ("Ice wizard", "cr/icewizard.webp"),
            ("Inferno tower", "cr/infernotower.webp"),
            ("Lightning", "cr/lightning.webp"),
            ("Little prince", "cr/littleprince.webp"),
            ("Lumberjack", "cr/lumberjack.webp"),
            ("Megaknight", "cr/megaknight.webp"),
            ("Mini P.E.K.K.A.", "cr/minipekka.webp"),
            ("Mirror", "cr/mirror.webp"),
            ("Monk", "cr/monk.webp"),
            ("Mother witch", "cr/motherwitch.webp"),
            ("Night witch", "cr/nightwitch.webp"),
            ("P.E.K.K.A.", "cr/pekka.webp"),
            ("Phoenix", "cr/phoenix.webp"),
            ("Poison", "cr/poison.webp"),
            ("Prince", "cr/prince.webp"),
            ("Princess", "cr/princess.webp"),
            ("Ram Rider", "cr/ramrider.webp"),
            ("Royal delivery", "cr/royaldelivery.webp"),
            ("Royal giant", "cr/royalgiant.webp"),
            ("Royal hogs", "cr/royalhogs.webp"),
            ("Royal recruits", "cr/royalrecruits.webp"),
            ("Rune giant", "cr/runegiant.webp"),
            ("Skeleton barrel", "cr/skeletonbarrel.webp"),
            ("Skeleton king", "cr/skeletonking.webp"),
            ("Sparky", "cr/sparky.webp"),
            ("Spear goblins", "cr/speargob.webp"),
            ("Tesla", "cr/tesla.webp"),
            ("Tombstone", "cr/tombstone.webp"),
            ("Valkyrie", "cr/valk.webp"),
            ("Vines", "cr/vines.webp"),
            ("Wallbreakers", "cr/wallbreaker.webp"),
            ("Wizard", "cr/wizard.webp"),
            ("X-bow", "cr/xbow.webp"),
            ("Zappiers", "cr/zappiers.webp"),
            ("Log", "cr/log.webp"),
            ("Miner", "cr/miner.webp"),
            ("Inferno dragon", "cr/infernodragon.webp"),
            ("Royal ghost", "cr/royalghost.webp"),
            ("Magic archer", "cr/magicarcher.webp"),
            ("Spirit Empress", "cr/spiritempress.webp"),
            ("Mighty miner", "cr/mightyminer.webp"),
            ("Boss bandit", "cr/bossbandit.webp"),
            ("Skeletons", "cr/skeletons.webp"),
            ("Minions", "cr/minions.webp"),
            ("Mega minion", "cr/megaminion.webp"),
            ("Baby dragon", "cr/babydragon.webp"),
            ("Tornado", "cr/tornado.webp"),
            ("Minion horde", "cr/minionhorde.webp"),
            ("Archers", "cr/archers.webp"),
            ("Rocket", "cr/rocket.webp"),
            
        ],
        "images_dir": "spygame",
    },
}


SCENARIOS = {
    "classic": "Классический",
    "random": "Рандомный",
    "all_spies": "Все шпионы",
    "all_civilians": "Все мирные жители",
    "chaos": "Хаос",
    "opposite": "Наоборот",
}

RANDOM_SCENARIO_WEIGHTS = [
    ("classic", 70),
    ("all_spies", 5),
    ("all_civilians", 5),
    ("chaos", 10),
    ("opposite", 10),
]


STATE = {}

#  функцииblya

def get_state(chat_id):
    return STATE.setdefault(chat_id, {
        "theme": None,
        "players": None,
        "scenario_choice": None,
        "scenario_final": None,
        "spies": None,
        "assignments": [],
        "index": 0,
        "prompt_message_id": None,
        "phase": "idle",
    })


def reset_state(chat_id):
    STATE[chat_id] = {
        "theme": None,
        "players": None,
        "scenario_choice": None,
        "scenario_final": None,
        "spies": None,
        "assignments": [],
        "index": 0,
        "prompt_message_id": None,
        "phase": "idle",
    }


def start_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать игру", callback_data="start_game"))
    kb.add(types.InlineKeyboardButton("Гайд", callback_data="show_help"))
    return kb


def mode_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("1 телефон", callback_data="mode:single"))
    kb.add(types.InlineKeyboardButton("В группе", callback_data="mode:group"))
    return kb


def theme_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🦁Өзімізғо", callback_data="theme:ozimizgo"))
    kb.add(types.InlineKeyboardButton("🀄️JJS", callback_data="theme:jjs"))
    kb.add(types.InlineKeyboardButton("👑Clash Royale", callback_data="theme:cr"))
    kb.add(types.InlineKeyboardButton("↩️Назад", callback_data="back:start"))
    return kb


def players_keyboard():
    kb = types.InlineKeyboardMarkup()
    row = []
    for n in range(3, 11):
        row.append(types.InlineKeyboardButton(str(n), callback_data=f"players:{n}"))
        if len(row) == 4:
            kb.row(*row)
            row = []
    if row:
        kb.row(*row)
    kb.add(types.InlineKeyboardButton("↩️Назад", callback_data="back:theme"))
    return kb


def scenario_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📌Классический", callback_data="scenario:classic"))
    kb.add(types.InlineKeyboardButton("🎲Рандомный", callback_data="scenario:random"))
    kb.add(types.InlineKeyboardButton("↩️Назад", callback_data="back:players"))
    return kb


def spies_keyboard(players):
    kb = types.InlineKeyboardMarkup()
    if players is None:
        kb.add(types.InlineKeyboardButton("Назад", callback_data="back:players"))
        return kb
    options = []
    if 3 <= players <= 4:
        options = [1]
    elif 5 <= players <= 7:
        options = [1, 2]
    else:
        options = [1, 2, 3]
    for n in options:
        kb.add(types.InlineKeyboardButton(str(n), callback_data=f"spies:{n}"))
    kb.add(types.InlineKeyboardButton("↩️Назад", callback_data="back:scenario"))
    return kb


def show_player_prompt(chat_id):
    state = get_state(chat_id)
    idx = state["index"] + 1
    state["phase"] = "waiting_show"
    text = (
        f"👤 <b>Игрок {idx}</b>\n\n"
        f"Передайте телефон Игроку {idx}.\n"
        "<i>Когда будете готовы, нажмите кнопку ниже, чтобы увидеть свою роль.</i>"
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Показать", callback_data="show_role"))
    msg = bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")
    state["prompt_message_id"] = msg.message_id


def pick_random_scenario():
    pool = []
    for name, weight in RANDOM_SCENARIO_WEIGHTS:
        pool.extend([name] * weight)
    return random.choice(pool)


def pick_spies_for_classic(players, explicit=None):
    if explicit is not None:
        return explicit
    if 3 <= players <= 4:
        return 1
    if 5 <= players <= 7:
        return random.choice([1, 2])
    return random.choice([1, 2, 3])


def get_theme_cards(theme_key):
    theme = THEMES[theme_key]
    if theme_key == "ozimizgo":
        return [(name, None) for name in theme["cards"]]
    return theme["cards"]


def build_assignments(theme_key, players, scenario_final, spies_count):
    cards = get_theme_cards(theme_key)
    assignments = []

    if scenario_final == "all_spies":
        for _ in range(players):
            assignments.append({"role": "spy", "card": None})
        return assignments

    if scenario_final == "all_civilians":
        card = random.choice(cards)
        for _ in range(players):
            assignments.append({"role": "civilian", "card": card})
        return assignments

    if scenario_final == "chaos":
        if players <= len(cards):
            selection = random.sample(cards, players)
        else:
            selection = [random.choice(cards) for _ in range(players)]
        for card in selection:
            assignments.append({"role": "civilian", "card": card})
        return assignments

    if scenario_final == "opposite":
        card = random.choice(cards)
        peaceful_index = random.randrange(players)
        for i in range(players):
            if i == peaceful_index:
                assignments.append({"role": "civilian", "card": card})
            else:
                assignments.append({"role": "spy", "card": None})
        return assignments

    # классический сценарий
    card = random.choice(cards)
    indices = list(range(players))
    random.shuffle(indices)
    spy_indices = set(indices[:spies_count])
    for i in range(players):
        if i in spy_indices:
            assignments.append({"role": "spy", "card": None})
        else:
            assignments.append({"role": "civilian", "card": card})
    return assignments


def start_role_distribution(chat_id):
    state = get_state(chat_id)
    state["index"] = 0
    state["phase"] = "waiting_show"
    show_player_prompt(chat_id)


def send_role(chat_id):
    state = get_state(chat_id)
    if state["index"] >= len(state["assignments"]):
        send_summary(chat_id)
        return
    state["phase"] = "showing_role"

    assignment = state["assignments"][state["index"]]

    if assignment["role"] == "spy":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Скрыть", callback_data="hide_role"))
        spy_path = os.path.join(BASE_DIR, "spy", "spy.jpg")
        try:
            with open(spy_path, "rb") as img:
                bot.send_photo(chat_id, img, caption="🔎 <b>Вы шпион</b>", reply_markup=kb, parse_mode="HTML")
        except Exception:
            bot.send_message(chat_id, "🔎 <b>Вы шпион</b>", reply_markup=kb, parse_mode="HTML")
        return

    card_name, card_path = assignment["card"]
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Скрыть", callback_data="hide_role"))

    caption = f"🗣️ <b>Вы мирный житель</b>\n\n🃏Карта игры: <b>{card_name}</b>"
    if card_path:
        with open(os.path.join(BASE_DIR, card_path), "rb") as img:
            bot.send_photo(chat_id, img, caption=caption, reply_markup=kb, parse_mode="HTML")
    else:
        bot.send_message(chat_id, caption, reply_markup=kb, parse_mode="HTML")


def send_summary(chat_id):
    state = get_state(chat_id)
    state["phase"] = "summary"
    theme_label = THEMES[state["theme"]]["label"]
    if state.get("scenario_choice") == "random":
        scenario_label = "Рандомный"
    else:
        scenario_label = SCENARIOS.get(state["scenario_final"], state["scenario_final"])

    text = (
        "👁️ <b>Все игроки просмотрели свои роли.</b>\n\n"
        f"🎭 <b>Тема игры:</b> {theme_label}\n"
        f"📋 <b>Сценарий:</b> {scenario_label}"
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄Играть заново", callback_data="play_again"))
    msg = bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")
    state["prompt_message_id"] = msg.message_id



# GROUP MODE HELPERS

def is_group_chat(chat):
    return getattr(chat, "type", None) in ("group", "supergroup")


def user_label(user):
    name = " ".join([p for p in [user.first_name, user.last_name] if p])
    if name:
        return name
    if user.username:
        return f"@{user.username}"
    return str(user.id)


def mention_user(user_id, name):
    safe_name = html.escape(name or str(user_id))
    return f"<a href=\"tg://user?id={user_id}\">{safe_name}</a>"


def numbered_user_list(user_ids, users_map):
    lines = []
    for idx, uid in enumerate(user_ids, start=1):
        name = users_map.get(uid, {}).get("name") or str(uid)
        lines.append(f"{idx}. {mention_user(uid, name)}")
    return "\n".join(lines) if lines else "—"


def get_group_state(group_id):
    return GROUP_GAMES.get(group_id)


def cancel_timer(timer_obj):
    if timer_obj:
        try:
            timer_obj.cancel()
        except Exception:
            pass


def cleanup_group_state(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    cancel_timer(state.get("join_timer"))
    cancel_timer(state.get("turn_timer"))
    if state.get("action_vote"):
        cancel_timer(state["action_vote"].get("timer"))
    if state.get("elimination"):
        cancel_timer(state["elimination"].get("timer"))
        cancel_timer(state["elimination"].get("confirm_timer"))
    for uid in state.get("participants", []):
        if USER_TO_GROUP.get(uid) == group_id:
            del USER_TO_GROUP[uid]
    del GROUP_GAMES[group_id]


def create_group_state(group_id, creator):
    state = {
        "group_id": group_id,
        "creator_id": creator.id,
        "creator_name": user_label(creator),
        "status": "recruiting",
        "participants": [],
        "users": {},
        "join_message_id": None,
        "join_timer": None,
        "theme": None,
        "scenario_choice": None,
        "scenario_final": None,
        "spies_count": None,
        "assignments": {},
        "alive": set(),
        "card": None,
        "round": 0,
        "turn_order": [],
        "turn_index": 0,
        "turn_timer": None,
        "current_speaker_id": None,
        "turn_spoken": False,
        "action_vote": None,
        "elimination": None,
    }
    GROUP_GAMES[group_id] = state
    add_participant(state, creator)
    return state


def add_participant(state, user):
    uid = user.id
    if uid in state["participants"]:
        return False
    state["participants"].append(uid)
    state["users"][uid] = {"name": user_label(user)}
    return True


def join_keyboard(group_id):
    kb = types.InlineKeyboardMarkup()
    if BOT_USERNAME:
        url = f"https://t.me/{BOT_USERNAME}?start=join_{group_id}"
        kb.add(types.InlineKeyboardButton("✅ Присоединиться", url=url))
    else:
        kb.add(types.InlineKeyboardButton("✅ Присоединиться", callback_data=f"g_join:{group_id}"))
    return kb


def build_join_text(state):
    names_text = numbered_user_list(state["participants"], state["users"])
    text = (
        "🧩 <b>Подбор участников</b>\n"
        f"👥 Участников: <b>{len(state['participants'])}</b>\n"
        f"{names_text}\n\n"
        "⚠️ <i>Важно: выдайте боту права администратора, чтобы игра в группе работала корректно.</i>"
    )
    return text


def update_join_message(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or not state.get("join_message_id"):
        return
    try:
        bot.edit_message_text(
            build_join_text(state),
            group_id,
            state["join_message_id"],
            reply_markup=join_keyboard(group_id),
            parse_mode="HTML",
        )
    except Exception:
        pass


def handle_private_join(message, group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state.get("status") != "recruiting":
        bot.send_message(message.chat.id, "⏳ Набор игроков не активен.")
        return
    if add_participant(state, message.from_user):
        bot.send_message(message.chat.id, "✅ Вы присоединились к текущей игре.")
        update_join_message(group_id)
    else:
        bot.send_message(message.chat.id, "ℹ️ Вы уже в списке участников.")


def handle_private_vote(message, group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state.get("status") != "elimination_vote":
        bot.send_message(message.chat.id, "⏳ Сейчас голосование не активно.")
        return
    if message.from_user.id not in state.get("alive", set()):
        bot.send_message(message.chat.id, "⛔ Вы не участвуете в текущей игре.")
        return
    alive = list(state["alive"])
    bot.send_message(
        message.chat.id,
        "🗳️ Отдайте свой голос на линчевание:",
        reply_markup=vote_keyboard(group_id, alive, exclude_id=message.from_user.id),
    )


def finalize_recruiting(group_id, reason="timeout"):
    state = GROUP_GAMES.get(group_id)
    if not state or state.get("status") != "recruiting":
        return
    cancel_timer(state.get("join_timer"))
    state["join_timer"] = None
    if len(state["participants"]) >= 3:
        start_group_config(group_id)
        return
    if reason == "creator":
        bot.send_message(group_id, "🚫 Игра была отменена создателем")
    else:
        bot.send_message(group_id, "⏰ Игра была отменена из-за истечения таймера")
    cleanup_group_state(group_id)


def help_text(index):
    index = max(0, min(index, len(HELP_PAGES) - 1))
    return HELP_PAGES[index], index


def help_keyboard(index):
    kb = types.InlineKeyboardMarkup()
    prev_idx = max(index - 1, 0)
    next_idx = min(index + 1, len(HELP_PAGES) - 1)
    kb.row(
        types.InlineKeyboardButton("<", callback_data=f"help:{prev_idx}"),
        types.InlineKeyboardButton(">", callback_data=f"help:{next_idx}"),
    )
    return kb


def pick_group_random_scenario():
    pool = []
    for name, weight in GROUP_RANDOM_SCENARIO_WEIGHTS:
        pool.extend([name] * weight)
    return random.choice(pool)


def group_theme_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🦁Өзімізғо", callback_data="g_theme:ozimizgo"))
    kb.add(types.InlineKeyboardButton("🀄️JJS", callback_data="g_theme:jjs"))
    kb.add(types.InlineKeyboardButton("👑Clash Royale", callback_data="g_theme:cr"))
    return kb


def group_scenario_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📌Классический", callback_data="g_scenario:classic"))
    kb.add(types.InlineKeyboardButton("🎲Рандомный", callback_data="g_scenario:random"))
    kb.add(types.InlineKeyboardButton("↩️Назад", callback_data="g_back:theme"))
    return kb


def group_spies_keyboard(players):
    kb = types.InlineKeyboardMarkup()
    options = []
    if 3 <= players <= 4:
        options = [1]
    elif 5 <= players <= 7:
        options = [1, 2]
    else:
        options = [1, 2, 3]
    for n in options:
        kb.add(types.InlineKeyboardButton(str(n), callback_data=f"g_spies:{n}"))
    kb.add(types.InlineKeyboardButton("↩️Назад", callback_data="g_back:scenario"))
    return kb


def start_group_config(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    state["status"] = "config_theme"
    text = (
        "🚀 <b>Игра запустилась</b>\n"
        f"👥 Количество участников: <b>{len(state['participants'])}</b>\n\n"
        "🎭 <b>Выберите тему игры:</b>"
    )
    bot.send_message(group_id, text, reply_markup=group_theme_keyboard(), parse_mode="HTML")


def send_role_private(user_id, assignment):
    try:
        if assignment["role"] == "spy":
            spy_path = os.path.join(BASE_DIR, "spy", "spy.jpg")
            try:
                with open(spy_path, "rb") as img:
                    bot.send_photo(user_id, img, caption="<b>Вы шпион</b>", parse_mode="HTML")
            except Exception:
                bot.send_message(user_id, "<b>Вы шпион</b>", parse_mode="HTML")
            return True
        card_name, card_path = assignment["card"]
        text = f"<b>Вы мирный житель</b>\n\nКарта игры: <b>{card_name}</b>"
        if card_path:
            with open(os.path.join(BASE_DIR, card_path), "rb") as img:
                bot.send_photo(user_id, img, caption=text, parse_mode="HTML")
        else:
            bot.send_message(user_id, text, parse_mode="HTML")
        return True
    except Exception:
        return False


def start_group_game(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    state["status"] = "roles"
    players = len(state["participants"])
    assignments = build_assignments(
        state["theme"],
        players,
        state["scenario_final"],
        state["spies_count"],
    )
    shuffled = list(state["participants"])
    random.shuffle(shuffled)
    state["assignments"] = {}
    for uid, assignment in zip(shuffled, assignments):
        state["assignments"][uid] = assignment
    for assignment in assignments:
        if assignment["role"] == "civilian":
            state["card"] = assignment["card"]
            break
    state["alive"] = set(state["participants"])

    unreachable = []
    for uid, assignment in list(state["assignments"].items()):
        if not send_role_private(uid, assignment):
            unreachable.append(uid)

    for uid in unreachable:
        if uid in state["alive"]:
            state["alive"].remove(uid)
        if uid in state["participants"]:
            state["participants"].remove(uid)
        state["assignments"].pop(uid, None)
        state["users"].pop(uid, None)
        try:
            bot.send_message(group_id, f"Игрок {uid} не открыл бота и был удален из игры.")
        except Exception:
            pass

    for uid in state["participants"]:
        USER_TO_GROUP[uid] = group_id

    bot.send_message(group_id, "<b>Все игроки просмотрели свои роли.</b>", parse_mode="HTML")
    state["turn_timer"] = threading.Timer(10, start_round, args=(group_id,))
    state["turn_timer"].start()


def start_round(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] == "ended":
        return
    state["status"] = "round_speaking"
    state["round"] += 1
    alive = list(state["alive"])
    random.shuffle(alive)
    state["turn_order"] = alive
    state["turn_index"] = 0
    state["current_speaker_id"] = None
    state["turn_spoken"] = False

    names_text = numbered_user_list(alive, state["users"])
    scenario_label = SCENARIOS.get(state["scenario_final"], state["scenario_final"])
    text = (
        f"🔔 <b>Круг {state['round']}</b>\n"
        f"👥 Игроков: <b>{len(alive)}</b>\n"
        f"🎭 Тема: <b>{THEMES[state['theme']]['label']}</b>\n"
        f"📋 Сценарий: <b>{scenario_label}</b>\n\n"
        f"🫂 <b>Список живых игроков:</b>\n{names_text}"
    )
    bot.send_message(group_id, text, parse_mode="HTML")
    start_turn(group_id)


def start_turn(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] != "round_speaking":
        return
    if state["turn_index"] >= len(state["turn_order"]):
        start_action_vote(group_id)
        return

    speaker_id = state["turn_order"][state["turn_index"]]
    state["current_speaker_id"] = speaker_id
    state["turn_spoken"] = False
    name = state["users"][speaker_id]["name"]
    text = (
        f"🎙️ <b>Ход игрока:</b> {name}\n\n"
        "Опишите карту игры, не называя ее конкретно.\n"
        "⏱️ У вас есть 30 секунд на сообщение."
    )
    bot.send_message(group_id, text, parse_mode="HTML")

    cancel_timer(state.get("turn_timer"))
    state["turn_timer"] = threading.Timer(30, turn_timeout, args=(group_id, speaker_id))
    state["turn_timer"].start()


def turn_timeout(group_id, speaker_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] != "round_speaking":
        return
    if state.get("current_speaker_id") != speaker_id:
        return
    advance_turn(group_id)


def advance_turn(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    cancel_timer(state.get("turn_timer"))
    state["turn_index"] += 1
    start_turn(group_id)


def start_action_vote(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] == "ended":
        return
    state["status"] = "action_vote"
    state["action_vote"] = {"votes": {}, "message_id": None, "timer": None}

    kb = action_vote_keyboard(state)
    msg = bot.send_message(
        group_id,
        f"✅ <b>Круг {state['round']} окончен</b>\n\nВыберите действие:",
        reply_markup=kb,
        parse_mode="HTML",
    )
    state["action_vote"]["message_id"] = msg.message_id
    state["action_vote"]["timer"] = threading.Timer(30, finalize_action_vote, args=(group_id,))
    state["action_vote"]["timer"].start()


def action_vote_keyboard(state):
    votes = state["action_vote"]["votes"]
    counts = {"eliminate": 0, "next": 0}
    for v in votes.values():
        if v in counts:
            counts[v] += 1
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f"❌ Выбывание ({counts['eliminate']})", callback_data="g_action:eliminate"))
    kb.add(types.InlineKeyboardButton(f"➡️ Следующий круг ({counts['next']})", callback_data="g_action:next"))
    return kb


def finalize_action_vote(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] != "action_vote":
        return
    votes = state["action_vote"]["votes"]
    counts = {"eliminate": 0, "next": 0}
    for v in votes.values():
        if v in counts:
            counts[v] += 1
    if counts["eliminate"] > counts["next"]:
        start_elimination_discuss(group_id)
    else:
        start_round(group_id)


def start_elimination_discuss(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    state["status"] = "elimination_discuss"
    text = "🗣️ <b>Выбывание</b>\n\nОбсудите, кого линчевать в этом кругу"
    bot.send_message(group_id, text, parse_mode="HTML")
    state["elimination"] = {"votes": {}, "timer": None, "confirm_votes": {}, "candidate": None, "confirm_timer": None}
    state["elimination"]["timer"] = threading.Timer(60, start_elimination_vote, args=(group_id,))
    state["elimination"]["timer"].start()


def start_elimination_vote(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] != "elimination_discuss":
        return
    state["status"] = "elimination_vote"

    kb = types.InlineKeyboardMarkup()
    if BOT_USERNAME:
        url = f"https://t.me/{BOT_USERNAME}?start=vote_{group_id}"
        kb.add(types.InlineKeyboardButton("🗳️ Проголосовать", url=url))
    else:
        kb.add(types.InlineKeyboardButton("🗳️ Проголосовать", callback_data=f"g_vote_open:{group_id}"))

    bot.send_message(
        group_id,
        "🗳️ <b>Голосование</b>\n\nОтдайте свой голос на линчевание",
        reply_markup=kb,
        parse_mode="HTML",
    )

    alive = [uid for uid in state["alive"]]
    for uid in alive:
        try:
            bot.send_message(
                uid,
                "🗳️ Отдайте свой голос на линчевание:",
                reply_markup=vote_keyboard(group_id, alive, exclude_id=uid),
            )
        except Exception:
            pass

    state["elimination"]["timer"] = threading.Timer(30, finalize_elimination_vote, args=(group_id,))
    state["elimination"]["timer"].start()


def vote_keyboard(group_id, alive_list, exclude_id=None):
    kb = types.InlineKeyboardMarkup()
    for uid in alive_list:
        if exclude_id is not None and uid == exclude_id:
            continue
        name = GROUP_GAMES[group_id]["users"][uid]["name"]
        kb.add(types.InlineKeyboardButton(name, callback_data=f"g_vote:{group_id}:{uid}"))
    return kb


def finalize_elimination_vote(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] != "elimination_vote":
        return
    votes = state["elimination"]["votes"]
    for uid in list(state["alive"]):
        if uid not in votes:
            try:
                bot.send_message(uid, "ℹ️ Вы решили не участвовать в голосовании")
            except Exception:
                pass
    if not votes:
        bot.send_message(group_id, "🤷 Игроки передумали участвовать в голосовании")
        start_round(group_id)
        return

    tally = {}
    for target in votes.values():
        tally[target] = tally.get(target, 0) + 1
    max_votes = max(tally.values())
    leaders = [uid for uid, cnt in tally.items() if cnt == max_votes]
    if len(leaders) != 1:
        bot.send_message(group_id, "⚖️ Мнения игроков разошлись")
        start_round(group_id)
        return

    candidate = leaders[0]
    start_confirmation_vote(group_id, candidate)


def start_confirmation_vote(group_id, candidate_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    state["status"] = "elimination_confirm"
    state["elimination"]["candidate"] = candidate_id
    state["elimination"]["confirm_votes"] = {"yes": set(), "no": set()}

    name = state["users"][candidate_id]["name"]
    kb = confirm_keyboard(state)
    msg = bot.send_message(
        group_id,
        f"❓ Вы действительно хотите линчевать {name}?",
        reply_markup=kb,
    )
    state["elimination"]["confirm_message_id"] = msg.message_id
    state["elimination"]["confirm_timer"] = threading.Timer(20, finalize_confirmation_vote, args=(group_id,))
    state["elimination"]["confirm_timer"].start()


def confirm_keyboard(state):
    votes = state["elimination"]["confirm_votes"]
    yes_count = len(votes["yes"])
    no_count = len(votes["no"])
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton(f"Да ({yes_count})", callback_data=f"g_confirm:yes"),
        types.InlineKeyboardButton(f"Нет ({no_count})", callback_data=f"g_confirm:no"),
    )
    return kb


def finalize_confirmation_vote(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state or state["status"] != "elimination_confirm":
        return
    votes = state["elimination"]["confirm_votes"]
    yes_count = len(votes["yes"])
    no_count = len(votes["no"])
    if yes_count == no_count or (yes_count == 0 and no_count == 0):
        bot.send_message(group_id, "⚖️ Мнения игроков разошлись")
        start_round(group_id)
        return
    if yes_count > no_count:
        eliminate_player(group_id, state["elimination"]["candidate"])
    else:
        bot.send_message(group_id, "⚖️ Мнения игроков разошлись")
        start_round(group_id)


def eliminate_player(group_id, player_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    name = state["users"][player_id]["name"]
    role = state["assignments"][player_id]["role"]
    role_label = "Шпион" if role == "spy" else "Мирный житель"
    if player_id in state["alive"]:
        state["alive"].remove(player_id)
    bot.send_message(group_id, f"❌ {name} выбывает из игры")
    bot.send_message(group_id, f"🪪 {name} — {role_label}")

    if check_group_end(group_id):
        return
    start_round(group_id)


def check_group_end(group_id):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return True
    spies_alive = [uid for uid in state["alive"] if state["assignments"][uid]["role"] == "spy"]
    civilians_alive = [uid for uid in state["alive"] if state["assignments"][uid]["role"] == "civilian"]

    if len(state["alive"]) == 2 and len(spies_alive) == 1 and len(civilians_alive) == 1:
        end_group_game(group_id, "🤝 Ничья! Мирные жители не смогли определить шпиона, а шпион не смог угадать карту.")
        return True
    if len(spies_alive) == 0:
        end_group_game(group_id, "🏆 Победа мирных жителей!")
        return True
    return False


def end_group_game(group_id, result_text):
    state = GROUP_GAMES.get(group_id)
    if not state:
        return
    state["status"] = "ended"
    bot.send_message(group_id, result_text)

    card_name, card_path = state.get("card") or (None, None)
    scenario_label = SCENARIOS.get(state["scenario_final"], state["scenario_final"])

    players_lines = []
    for idx, uid in enumerate(state["participants"], start=1):
        role = state["assignments"].get(uid, {}).get("role")
        if not role:
            continue
        role_label = "Шпион" if role == "spy" else "Мирный житель"
        name_link = mention_user(uid, state["users"].get(uid, {}).get("name"))
        players_lines.append(f"{idx}. {name_link} — {role_label}")

    summary = (
        "🏁 Итоги игры\n"
        f"🗺️ Карта: {card_name}\n"
        f"🎭 Тема: {THEMES[state['theme']]['label']}\n"
        f"📋 Сценарий: {scenario_label}\n\n"
        "👥 Игроки:\n"
        + "\n".join(players_lines)
    )

    if card_path:
        try:
            with open(os.path.join(BASE_DIR, card_path), "rb") as img:
                bot.send_photo(group_id, img, caption=summary, parse_mode="HTML")
        except Exception:
            bot.send_message(group_id, summary, parse_mode="HTML")
    else:
        bot.send_message(group_id, summary, parse_mode="HTML")

    cleanup_group_state(group_id)
# Внешний интерфейс бота

@bot.message_handler(commands=["start"])
def cmd_start(message):
    args = message.text.split()
    if len(args) > 1:
        if args[1].startswith("join_"):
            try:
                group_id = int(args[1].split("_", 1)[1])
            except ValueError:
                group_id = None
            if group_id is not None:
                handle_private_join(message, group_id)
                return
        if args[1].startswith("vote_"):
            try:
                group_id = int(args[1].split("_", 1)[1])
            except ValueError:
                group_id = None
            if group_id is not None:
                handle_private_vote(message, group_id)
                return
    reset_state(message.chat.id)
    bot.send_message(
        message.chat.id,
        "<b>🫆Бот для игры в шпиона</b>\n\n<i>Нажмите кнопку ниже, чтобы начать.</i>",
        reply_markup=start_keyboard(),
        parse_mode="HTML",
    )


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text, idx = help_text(0)
    bot.send_message(message.chat.id, text, reply_markup=help_keyboard(idx), parse_mode="HTML")


def log_text(index):
    index = max(0, min(index, len(CHANGELOG) - 1))
    entry = CHANGELOG[index]
    lines = [f"<b>Версия {entry['version']}</b>"]
    for item in entry.get("added", []):
        lines.append(f"• {item}")
    for item in entry.get("fixed", []):
        lines.append(f"• {item}")
    return "\n".join(lines), index


def log_keyboard(index):
    kb = types.InlineKeyboardMarkup()
    prev_idx = max(index - 1, 0)
    next_idx = min(index + 1, len(CHANGELOG) - 1)
    kb.row(
        types.InlineKeyboardButton("<", callback_data=f"log:{prev_idx}"),
        types.InlineKeyboardButton(">", callback_data=f"log:{next_idx}"),
    )
    return kb


@bot.message_handler(commands=["log"])
def cmd_log(message):
    text, idx = log_text(0)
    bot.send_message(message.chat.id, text, reply_markup=log_keyboard(idx), parse_mode="HTML")


@bot.message_handler(commands=["s"])
def cmd_group_start(message):
    if not is_group_chat(message.chat):
        return
    group_id = message.chat.id
    state = GROUP_GAMES.get(group_id)
    if state and state.get("status") != "ended":
        bot.send_message(
            group_id,
            f"⛔ Невозможно начать подбор игроков. Подбор уже начат игроком {state['creator_name']}",
        )
        return
    state = create_group_state(group_id, message.from_user)
    msg = bot.send_message(
        group_id,
        build_join_text(state),
        reply_markup=join_keyboard(group_id),
        parse_mode="HTML",
    )
    state["join_message_id"] = msg.message_id
    state["join_timer"] = threading.Timer(60, finalize_recruiting, args=(group_id, "timeout"))
    state["join_timer"].start()


@bot.message_handler(commands=["stop"])
def cmd_group_stop(message):
    if not is_group_chat(message.chat):
        return
    group_id = message.chat.id
    state = GROUP_GAMES.get(group_id)
    if not state or state.get("status") == "ended":
        bot.send_message(group_id, "⛔ Невозможно досрочно распустить НЕСУЩЕСТВУЮЩИЙ подбор")
        return
    if message.from_user.id != state["creator_id"]:
        return
    if state.get("status") == "recruiting":
        finalize_recruiting(group_id, "creator")
        return
    if state.get("status", "").startswith("config"):
        bot.send_message(group_id, "🚫 Игра была отменена создателем")
        cleanup_group_state(group_id)
        return


@bot.message_handler(commands=["game"])
def cmd_group_game(message):
    if not is_group_chat(message.chat):
        return
    group_id = message.chat.id
    state = GROUP_GAMES.get(group_id)
    if not state or state.get("status") != "recruiting":
        bot.send_message(group_id, "⛔ Невозможно досрочно начать НЕСУЩЕСТВУЮЩИЙ подбор")
        return
    if len(state["participants"]) < 3:
        bot.send_message(group_id, "⚠️ Невозможно досрочно начать игру. Участников меньше минимального порога.")
        return
    cancel_timer(state.get("join_timer"))
    state["join_timer"] = None
    start_group_config(group_id)


@bot.message_handler(commands=["answer"])
def cmd_group_answer(message):
    guess = message.text.split(maxsplit=1)
    if len(guess) < 2:
        bot.send_message(message.chat.id, "ℹ️ Используйте: /answer Название карты")
        return
    guess_text = " ".join(guess[1:]).strip()
    if not guess_text:
        bot.send_message(message.chat.id, "ℹ️ Используйте: /answer Название карты")
        return

    if is_group_chat(message.chat):
        group_id = message.chat.id
    else:
        group_id = USER_TO_GROUP.get(message.from_user.id)
    if not group_id:
        bot.send_message(message.chat.id, "⛔ Игра не найдена.")
        return
    state = GROUP_GAMES.get(group_id)
    if not state or state.get("status") in ("recruiting", "config_theme", "config_scenario", "config_spies", "ended"):
        bot.send_message(message.chat.id, "⏳ Сейчас игра не активна.")
        return
    if message.from_user.id not in state.get("alive", set()):
        bot.send_message(message.chat.id, "⛔ Вы не участвуете в текущей игре.")
        return
    if state["assignments"][message.from_user.id]["role"] != "spy":
        bot.send_message(message.chat.id, "🕵️ Эта команда доступна только шпионам.")
        return

    card_name = state.get("card")[0] if state.get("card") else ""
    norm_guess = " ".join(guess_text.lower().split())
    norm_card = " ".join(card_name.lower().split())
    if norm_guess == norm_card:
        winner = state["users"][message.from_user.id]["name"]
        end_group_game(group_id, f"🎉 Победа Шпиона {winner}!")
        return

    name = state["users"][message.from_user.id]["name"]
    bot.send_message(group_id, f"💥 Шпион {name} был выбит из игры за неправильный ответ: {guess_text}")
    if message.from_user.id in state["alive"]:
        state["alive"].remove(message.from_user.id)
    check_group_end(group_id)


def handle_group_callback(call):
    data = call.data

    if data.startswith("g_join:"):
        try:
            group_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "recruiting":
            bot.answer_callback_query(call.id, "⏳ Набор игроков не активен.", show_alert=True)
            return
        if call.from_user.id in state["participants"]:
            bot.answer_callback_query(call.id, "ℹ️ Вы уже в списке участников.", show_alert=False)
            return
        try:
            bot.send_message(call.from_user.id, "✅ Вы присоединились к текущей игре.")
        except Exception:
            bot.answer_callback_query(call.id, "Сначала напишите боту /start в личных сообщениях.", show_alert=True)
            return
        add_participant(state, call.from_user)
        update_join_message(group_id)
        bot.answer_callback_query(call.id, "✅ Вы присоединились.", show_alert=False)
        return

    if data.startswith("g_theme:"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "config_theme":
            return
        if call.from_user.id != state["creator_id"]:
            bot.answer_callback_query(call.id, "🛡️ Только создатель может выбирать настройки.", show_alert=True)
            return
        theme_key = data.split(":", 1)[1]
        state["theme"] = theme_key
        state["status"] = "config_scenario"
        text = (
            f"<b>Количество участников:</b> {len(state['participants'])}\n"
            f"<b>Тема игры:</b> {THEMES[theme_key]['label']}\n\n"
            "<b>Выберите сценарий:</b>"
        )
        bot.edit_message_text(
            text,
            group_id,
            call.message.message_id,
            reply_markup=group_scenario_keyboard(),
            parse_mode="HTML",
        )
        return

    if data.startswith("g_back:theme"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state:
            return
        if call.from_user.id != state["creator_id"]:
            bot.answer_callback_query(call.id, "🛡️ Только создатель может выбирать настройки.", show_alert=True)
            return
        state["status"] = "config_theme"
        bot.edit_message_text(
            f"<b>Количество участников:</b> {len(state['participants'])}\n\nВыберите тему игры:",
            group_id,
            call.message.message_id,
            reply_markup=group_theme_keyboard(),
            parse_mode="HTML",
        )
        return

    if data.startswith("g_back:scenario"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state:
            return
        if call.from_user.id != state["creator_id"]:
            bot.answer_callback_query(call.id, "🛡️ Только создатель может выбирать настройки.", show_alert=True)
            return
        state["status"] = "config_scenario"
        text = (
            f"<b>Количество участников:</b> {len(state['participants'])}\n"
            f"<b>Тема игры:</b> {THEMES[state['theme']]['label']}\n\n"
            "<b>Выберите сценарий:</b>"
        )
        bot.edit_message_text(
            text,
            group_id,
            call.message.message_id,
            reply_markup=group_scenario_keyboard(),
            parse_mode="HTML",
        )
        return

    if data.startswith("g_scenario:"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "config_scenario":
            return
        if call.from_user.id != state["creator_id"]:
            bot.answer_callback_query(call.id, "🛡️ Только создатель может выбирать настройки.", show_alert=True)
            return
        scenario_choice = data.split(":", 1)[1]
        state["scenario_choice"] = scenario_choice
        if scenario_choice == "classic":
            state["status"] = "config_spies"
            text = (
                f"<b>Количество участников:</b> {len(state['participants'])}\n"
                f"<b>Тема игры:</b> {THEMES[state['theme']]['label']}\n"
                "<b>Сценарий:</b> Классический\n\n"
                "<b>Выберите количество шпионов:</b>"
            )
            bot.edit_message_text(
                text,
                group_id,
                call.message.message_id,
                reply_markup=group_spies_keyboard(len(state["participants"])),
                parse_mode="HTML",
            )
            return

        scenario_final = pick_group_random_scenario()
        state["scenario_final"] = scenario_final
        state["spies_count"] = pick_spies_for_classic(len(state["participants"]))
        if scenario_final == "opposite":
            state["spies_count"] = None
        bot.edit_message_text(
            "🔒 <b>Раздача ролей начинается.</b>",
            group_id,
            call.message.message_id,
            parse_mode="HTML",
        )
        start_group_game(group_id)
        return

    if data.startswith("g_spies:"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "config_spies":
            return
        if call.from_user.id != state["creator_id"]:
            bot.answer_callback_query(call.id, "🛡️ Только создатель может выбирать настройки.", show_alert=True)
            return
        try:
            spies = int(data.split(":", 1)[1])
        except ValueError:
            return
        state["spies_count"] = spies
        state["scenario_final"] = "classic"
        bot.edit_message_text(
            "🔒 <b>Раздача ролей начинается.</b>",
            group_id,
            call.message.message_id,
            parse_mode="HTML",
        )
        start_group_game(group_id)
        return

    if data.startswith("g_action:"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "action_vote":
            return
        if call.from_user.id not in state["alive"]:
            return
        action = data.split(":", 1)[1]
        if call.from_user.id in state["action_vote"]["votes"]:
            return
        state["action_vote"]["votes"][call.from_user.id] = action
        try:
            bot.edit_message_reply_markup(
                group_id,
                state["action_vote"]["message_id"],
                reply_markup=action_vote_keyboard(state),
            )
        except Exception:
            pass
        if len(state["action_vote"]["votes"]) >= len(state["alive"]):
            cancel_timer(state["action_vote"].get("timer"))
            finalize_action_vote(group_id)
        return

    if data.startswith("g_vote_open:"):
        bot.answer_callback_query(call.id, "🗳️ Голосование проходит в личных сообщениях.", show_alert=True)
        return

    if data.startswith("g_vote:"):
        parts = data.split(":")
        if len(parts) != 3:
            return
        group_id = int(parts[1])
        target_id = int(parts[2])
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "elimination_vote":
            return
        if call.from_user.id not in state["alive"]:
            return
        if call.from_user.id in state["elimination"]["votes"]:
            return
        state["elimination"]["votes"][call.from_user.id] = target_id
        voter_name = state["users"][call.from_user.id]["name"]
        target_name = state["users"][target_id]["name"]
        try:
            bot.send_message(call.from_user.id, f"✅ Вы успешно отдали свой голос за {target_name}")
        except Exception:
            pass
        bot.send_message(group_id, f"🗳️ {voter_name} проголосовал за {target_name}")
        if len(state["elimination"]["votes"]) >= len(state["alive"]):
            cancel_timer(state["elimination"].get("timer"))
            finalize_elimination_vote(group_id)
        return

    if data.startswith("g_confirm:"):
        group_id = call.message.chat.id
        state = GROUP_GAMES.get(group_id)
        if not state or state.get("status") != "elimination_confirm":
            return
        candidate = state["elimination"]["candidate"]
        if call.from_user.id not in state["alive"] or call.from_user.id == candidate:
            return
        choice = data.split(":", 1)[1]
        if call.from_user.id in state["elimination"]["confirm_votes"]["yes"] or call.from_user.id in state["elimination"]["confirm_votes"]["no"]:
            return
        if choice == "yes":
            state["elimination"]["confirm_votes"]["yes"].add(call.from_user.id)
        else:
            state["elimination"]["confirm_votes"]["no"].add(call.from_user.id)
        try:
            bot.edit_message_reply_markup(
                group_id,
                state["elimination"]["confirm_message_id"],
                reply_markup=confirm_keyboard(state),
            )
        except Exception:
            pass
        eligible = len(state["alive"]) - 1
        total_votes = len(state["elimination"]["confirm_votes"]["yes"]) + len(state["elimination"]["confirm_votes"]["no"])
        if total_votes >= max(eligible, 0):
            cancel_timer(state["elimination"].get("confirm_timer"))
            finalize_confirmation_vote(group_id)
        return


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data
    state = get_state(chat_id)

    if data.startswith("g_"):
        handle_group_callback(call)
        return

    if data == "show_help":
        text, idx = help_text(0)
        bot.send_message(chat_id, text, reply_markup=help_keyboard(idx), parse_mode="HTML")
        return

    if data.startswith("help:"):
        try:
            idx = int(data.split(":", 1)[1])
        except ValueError:
            return
        text, idx = help_text(idx)
        try:
            bot.edit_message_text(
                text,
                chat_id,
                call.message.message_id,
                reply_markup=help_keyboard(idx),
                parse_mode="HTML",
            )
        except Exception:
            pass
        return

    if data.startswith("log:"):
        try:
            idx = int(data.split(":", 1)[1])
        except ValueError:
            return
        text, idx = log_text(idx)
        try:
            bot.edit_message_text(
                text,
                chat_id,
                call.message.message_id,
                reply_markup=log_keyboard(idx),
                parse_mode="HTML",
            )
        except Exception:
            pass
        return

    if data == "start_game":
        bot.edit_message_text(
            "🎮 <b>Выберите режим игры:</b>",
            chat_id,
            call.message.message_id,
            reply_markup=mode_keyboard(),
            parse_mode="HTML",
        )
        return

    if data == "mode:single":
        bot.edit_message_text(
            "🎭 <b>Выберите тему игры:</b>",
            chat_id,
            call.message.message_id,
            reply_markup=theme_keyboard(),
            parse_mode="HTML",
        )
        return

    if data == "mode:group":
        bot.edit_message_text(
            "👥 <b>Режим игры в группе</b>\n\n"
            "1) Добавьте бота в группу.\n"
            "2) Выдайте боту права администратора.\n"
            "3) Напишите команду <b>/s</b> для старта подбора.\n\n"
            "✅ После набора участников начнётся настройка игры.",
            chat_id,
            call.message.message_id,
            parse_mode="HTML",
        )
        return

    if data.startswith("theme:"):
        theme_key = data.split(":", 1)[1]
        state["theme"] = theme_key
        bot.edit_message_text(
            "👥 <b>Выберите количество игроков:</b>",
            chat_id,
            call.message.message_id,
            reply_markup=players_keyboard(),
            parse_mode="HTML",
        )
        return

    if data.startswith("players:"):
        players = int(data.split(":", 1)[1])
        state["players"] = players
        bot.edit_message_text(
            "📋 <b>Выберите сценарий:</b>",
            chat_id,
            call.message.message_id,
            reply_markup=scenario_keyboard(),
            parse_mode="HTML",
        )
        return

    if data.startswith("scenario:"):
        scenario_choice = data.split(":", 1)[1]
        state["scenario_choice"] = scenario_choice

        if scenario_choice == "classic":
            if state.get("players") is None:
                bot.edit_message_text(
                    "👥 <b>Сначала выберите количество игроков.</b>",
                    chat_id,
                    call.message.message_id,
                    reply_markup=players_keyboard(),
                    parse_mode="HTML",
                )
                return
            bot.edit_message_text(
                "🔎 <b>Выберите количество шпионов:</b>",
                chat_id,
                call.message.message_id,
                reply_markup=spies_keyboard(state["players"]),
                parse_mode="HTML",
            )
            return

        scenario_final = pick_random_scenario()
        state["scenario_final"] = scenario_final
        state["spies"] = pick_spies_for_classic(state["players"])
        if scenario_final in ("all_spies", "all_civilians", "chaos", "opposite"):
            state["spies"] = None
        state["assignments"] = build_assignments(
            state["theme"],
            state["players"],
            scenario_final,
            state["spies"],
        )
        bot.edit_message_text(
            "<b>Раздача ролей начинается...</b>",
            chat_id,
            call.message.message_id,
            parse_mode="HTML",
        )
        start_role_distribution(chat_id)
        return

    if data.startswith("spies:"):
        spies = int(data.split(":", 1)[1])
        state["spies"] = spies
        state["scenario_final"] = "classic"
        state["assignments"] = build_assignments(
            state["theme"],
            state["players"],
            "classic",
            spies,
        )
        bot.edit_message_text(
            f"🔎 <b>Шпионов:</b> {spies}.\n<i>Раздача ролей начинается...</i>",
            chat_id,
            call.message.message_id,
            parse_mode="HTML",
        )
        start_role_distribution(chat_id)
        return

    if data == "show_role":
        if state.get("phase") != "waiting_show":
            return
        prompt_id = state.get("prompt_message_id")
        if prompt_id:
            try:
                bot.delete_message(chat_id, prompt_id)
            except Exception:
                pass
            state["prompt_message_id"] = None
        send_role(chat_id)
        return

    if data == "hide_role":
        if state.get("phase") != "showing_role":
            return
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except Exception:
            pass
        state["index"] += 1
        if state["index"] >= len(state["assignments"]):
            send_summary(chat_id)
        else:
            show_player_prompt(chat_id)
        return

    if data == "play_again":
        reset_state(chat_id)
        bot.edit_message_text(
            "<b>🫆Бот для игры в шпиона.</b>\n\n<i>Нажмите кнопку ниже, чтобы начать.</i>",
            chat_id,
            call.message.message_id,
            reply_markup=start_keyboard(),
            parse_mode="HTML",
        )
        return

    if data.startswith("back:"):
        target = data.split(":", 1)[1]
        if target == "start":
            reset_state(chat_id)
            bot.edit_message_text(
                "<b>🫆Бот для игры в шпиона.</b>\n\n<i>Нажмите кнопку ниже, чтобы начать.</i>",
                chat_id,
                call.message.message_id,
                reply_markup=start_keyboard(),
                parse_mode="HTML",
            )
            return
        if target == "theme":
            bot.edit_message_text(
                "🎭 <b>Выберите тему игры:</b>",
                chat_id,
                call.message.message_id,
                reply_markup=theme_keyboard(),
                parse_mode="HTML",
            )
            return
        if target == "players":
            bot.edit_message_text(
                "👥 <b>Выберите количество игроков:</b>",
                chat_id,
                call.message.message_id,
                reply_markup=players_keyboard(),
                parse_mode="HTML",
            )
            return
        if target == "scenario":
            bot.edit_message_text(
                "📋 <b>Выберите сценарий:</b>",
                chat_id,
                call.message.message_id,
                reply_markup=scenario_keyboard(),
                parse_mode="HTML",
            )
            return


@bot.message_handler(
    func=lambda message: is_group_chat(message.chat),
    content_types=["text", "sticker", "photo", "animation", "video", "document", "audio", "voice", "video_note"],
)
def handle_group_messages(message):
    state = GROUP_GAMES.get(message.chat.id)
    if not state:
        return
    if message.text and message.text.startswith("/"):
        return

    if state.get("status") == "round_speaking":
        speaker_id = state.get("current_speaker_id")
        if message.from_user.id != speaker_id:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            return
        if state.get("turn_spoken"):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            return
        state["turn_spoken"] = True
        advance_turn(message.chat.id)
        return

    if state.get("status") in ("action_vote", "elimination_vote", "elimination_confirm", "roles"):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass

bot.polling(none_stop=True)

# Janasyl syebalsya otsuda




