import os
import random
import telebot
from telebot import types


BOT_TOKEN = os.getenv("BOT_TOKEN") or "8382682504:AAErIB11GWaGJDfn4YRlu6hpQC1dAVsDRng"

bot = telebot.TeleBot(BOT_TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    ("classic", 60),
    ("all_spies", 10),
    ("all_civilians", 10),
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


# Внешний интерфейс бота

@bot.message_handler(commands=["start"])
def cmd_start(message):
    reset_state(message.chat.id)
    bot.send_message(
        message.chat.id,
        "<b>🫆Бот для игры в шпиона</b>\n\n<i>Нажмите кнопку ниже, чтобы начать.</i>",
        reply_markup=start_keyboard(),
        parse_mode="HTML",
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data
    state = get_state(chat_id)

    if data == "start_game":
        bot.edit_message_text(
            "🎭 <b>Выберите тему игры:</b>",
            chat_id,
            call.message.message_id,
            reply_markup=theme_keyboard(),
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


bot.polling(none_stop=True)

# Janasyl syebalsya otsuda
