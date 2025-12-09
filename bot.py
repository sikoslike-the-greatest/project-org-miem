import logging
import os
from typing import Dict, List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


ARTIST_DIR_MAP = {
    "pimenov": {"dir": "Пименов", "title": "Пименов", "title_gen": "Пименова"},
    "plavinskiy": {"dir": "Плавинский", "title": "Плавинский", "title_gen": "Плавинского"},
    "chtak": {"dir": "Чтак", "title": "Чтак", "title_gen": "Чтака"},
}

REALISM_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), "images", "Реализм", "Фото-раздела.jpg"
)

AVANT_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), "images", "Авангард", "фото-раздела.jpg"
)

SOVIET_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), "images", "соцреализм", "обложка-раздела.jpeg"
)

CONTEMP_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), "images", "современное", "обложка-раздела.jpg"
)

GUIDE_CLASSIC_DETAILS = {
    "tretyakov_lavrushinsky": {
        "title": "Государственная Третьяковская галерея, Лаврушинский переулок",
        "desc": (
            "Главное собрание русской классической живописи и реализма XIX – начала XX века, включая передвижников."
        ),
        "site": "https://www.tretyakovgallery.ru/",
        "address": "Лаврушинский пер., 10",
    },
    "tretyakov_kadashevskaya": {
        "title": "Новый корпус Третьяковской галереи (Кадашевская наб.)",
        "desc": (
            "Крупная экспозиция, целиком посвящённая русскому реализму и Товариществу передвижных художественных выставок."
        ),
        "site": "https://www.tretyakovgallery.ru/",
        "address": "Кадашевская наб., 10",
    },
    "pushkin_main": {
        "title": "Государственный музей изобразительных искусств им. А.С. Пушкина (основное здание)",
        "desc": (
            "Европейская классическая живопись и скульптура, старые мастера — важный блок для понимания академической традиции и реалистической школы."
        ),
        "site": "https://www.pushkinmuseum.art/",
        "address": "ул. Волхонка, 12",
    },
}

GUIDE_CLASSIC_IMAGES = {
    "tretyakov_lavrushinsky": os.path.join(
        os.path.dirname(__file__), "images", "Реализм", "третьяковка-лаврушенский-переулок.jpg"
    ),
    "tretyakov_kadashevskaya": os.path.join(
        os.path.dirname(__file__), "images", "Реализм", "третьяковка-кадашевская.jpg"
    ),
    "pushkin_main": os.path.join(
        os.path.dirname(__file__), "images", "Реализм", "музей-пушкина.jpg"
    ),
}

GUIDE_AVANT_DETAILS = {
    "shabolovka_museum": {
        "title": "Музей авангарда на Шаболовке (Галерея «На Шаболовке»)",
        "desc": (
            "Экспозиция в конструктивистском жилмассиве Хавско‑Шаболовского района, посвящена архитектуре 1920–1930-х, "
            "Шуховской башне и истории советского авангарда в квартале."
        ),
        "site": "https://shabolovka.vzmoscow.ru/",
        "address": "ул. Шаболовка, 24, корп. 2",
    },
    "shabolovka_walk": {
        "title": "Пешеходный маршрут «Авангард на Шаболовке»",
        "desc": (
            "Прогулка вокруг Шуховской башни: дом-коммуна, школа‑«гигант», конструктивистские дома. "
            "Показывает, как идеи авангарда воплотились в городской среде."
        ),
        "site": "https://shabolovka.vzmoscow.ru/archive/tproduct/1243040061-175439713442-ulichnaya-ekskursiya-avangard-na-shabolo",
        "address": "Старт: ул. Шаболовка, 37 (Шуховская башня)",
    },
    "jewish_museum": {
        "title": "Еврейский музей и Центр толерантности (Центр авангарда)",
        "desc": (
            "Выставки русского авангарда («До востребования», «Союз молодёжи» и др.), ключевые художники начала XX века и контекст движения."
        ),
        "site": "https://www.jewish-museum.ru/",
        "address": "ул. Образцова, 11, стр. 1",
    },
    "tretyakov_new": {
        "title": "Третьяковская галерея (Новая Третьяковка, проекты об авангарде)",
        "desc": (
            "Крупные выставки по русскому авангарду (например, «Авангард. Список № 1»): Кандинский, Малевич, Татлин, Попова и др."
        ),
        "site": "https://www.tretyakovgallery.ru/",
        "address": "Крымский Вал, 10",
    },
}

GUIDE_AVANT_IMAGES = {
    "shabolovka_museum": os.path.join(
        os.path.dirname(__file__), "images", "Авангард", "шаболовка.jpg"
    ),
    "shabolovka_walk": os.path.join(
        os.path.dirname(__file__), "images", "Авангард", "авангард-на-шабаловке.jpg"
    ),
    "jewish_museum": os.path.join(
        os.path.dirname(__file__), "images", "Авангард", "еврейский-центр.jpeg"
    ),
    "tretyakov_new": os.path.join(
        os.path.dirname(__file__), "images", "Авангард", "новая-третьяковка-крымский-вал.jpg"
    ),
}

GUIDE_SOVIET_DETAILS = {
    "tretyakov_soviet": {
        "title": "Новая Третьяковка (Крымский Вал)",
        "desc": (
            "Постоянная экспозиция искусства XX века, крупные полотна соцреализма и проекты вроде "
            "«Соцреализм. Метаморфозы. Советское искусство 1927–1987». Видно, как формировался официальный канон СССР."
        ),
        "site": "https://www.tretyakovgallery.ru/",
        "address": "Крымский Вал, 10",
    },
    "vmdpni": {
        "title": "Всероссийский музей декоративного искусства",
        "desc": (
            "Проекты «Соцреализм. Стиль большой эпохи»: живопись, скульптура, декоративное искусство и предметы быта "
            "советского периода. Помогает понять повседневную эстетику эпохи."
        ),
        "site": "https://damuseum.ru/",
        "address": "ул. Делегатская, 3",
    },
    "mosaics": {
        "title": "Советские мозаики и панно Москвы",
        "desc": (
            "Мозаичная карта: станции метро (например, «Маяковская»), фасады и интерьеры зданий, заводские и креативные кластеры "
            "с сохранёнными мозаиками. Живой визуальный код эпохи в городской среде."
        ),
        "site": "https://tour.mosmetro.ru/tours/0C452E44-DB24-4B8E-A551-52C6538952EB",
        "address": "Разные адреса; старт маршрута: м. Маяковская",
    },
}

GUIDE_SOVIET_IMAGES = {
    "tretyakov_soviet": os.path.join(
        os.path.dirname(__file__), "images", "соцреализм", "новая-третьяковка-крымский-вал.jpg"
    ),
    "vmdpni": os.path.join(
        os.path.dirname(__file__), "images", "соцреализм", "музей-декоративного-искусства.jpg"
    ),
    "mosaics": os.path.join(
        os.path.dirname(__file__), "images", "соцреализм", "мозаика-в-метро.jpeg"
    ),
}

GUIDE_CONTEMP_DETAILS = {
    "mmoma": {
        "title": "Московский музей современного искусства (MMOMA)",
        "desc": (
            "Первый в России музей, полностью посвящённый современному искусству: несколько площадок в центре, "
            "постоянная коллекция и крупные выставки российских и зарубежных художников XX–XXI веков."
        ),
        "site": "https://mmoma.ru/",
        "address": "ул. Петровка, 25 и др. площадки",
    },
    "garage": {
        "title": "Музей современного искусства «Гараж» (Парк Горького)",
        "desc": (
            "Один из главных центров актуального искусства: международные выставки, перформансы, лекции, фестивали "
            "и сильная образовательная программа."
        ),
        "site": "https://garagemca.org/",
        "address": "Парк Горького, ул. Крымский Вал, 9, стр. 32",
    },
    "mamm": {
        "title": "Мультимедиа Арт Музей, Москва (МАММ)",
        "desc": (
            "Музей фотографии, видео- и медиаискусства на Остоженке: семь этажей экспозиций, "
            "фокус на современном визуальном языке, документальной и художественной фотографии."
        ),
        "site": "https://mamm-mdf.ru/",
        "address": "ул. Остоженка, 16",
    },
    "winzavod": {
        "title": "Центр современного искусства «Винзавод»",
        "desc": (
            "Крупный арт-кластер на территории бывшего завода: галереи современного искусства, мастерские, "
            "институт «БАЗА», фестивали и ярмарки."
        ),
        "site": "https://winzavod.ru/",
        "address": "4-й Сыромятнический пер., 1/8с6",
    },
}

GUIDE_CONTEMP_IMAGES = {
    "mmoma": os.path.join(
        os.path.dirname(__file__), "images", "современное", "ммома.jpeg"
    ),
    "garage": os.path.join(
        os.path.dirname(__file__), "images", "современное", "музей-гараж.jpg"
    ),
    "mamm": os.path.join(
        os.path.dirname(__file__), "images", "современное", "ммам.jpg"
    ),
    "winzavod": os.path.join(
        os.path.dirname(__file__), "images", "современное", "винзавод.jpg"
    ),
}


START_MESSAGE = (
    "✨*Привет!* Этот бот поможет тебе открыть Москву как крупнейший художественный центр "
    "России и подобрать маршрут по самым ярким творческим локациям города. Проект создан "
    "студентами 1 курса НИУ ВШЭ (МИЭМ) в рамках учебного курса ОРГ.\n\n"
    "🧭 *Навигация*:\n\n"
    "> Нажми «*Узнать о Москве*», чтобы начать знакомство.\n"
    "> Нажми «*Московские художники*», чтобы узнать больше о художниках Москвы.\n"
    "> Нажми «*Путеводитель*», чтобы составить маршрут по интересным местам города."


)


def build_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("Узнать о Москве", callback_data="info:moscow")],
        [InlineKeyboardButton("Московские художники", callback_data="artists")],
        [InlineKeyboardButton("Путеводитель", callback_data="guide")],
        [InlineKeyboardButton("Авторы", callback_data="authors")],
    ]
    return InlineKeyboardMarkup(buttons)


def _artist_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Пименов", callback_data="artist:pimenov"),
                InlineKeyboardButton("Плавинский", callback_data="artist:plavinskiy"),
            ],
            [InlineKeyboardButton("Чтак", callback_data="artist:chtak")],
            [InlineKeyboardButton("⬅️ В меню", callback_data="back")],
        ]
    )


def _guide_classic_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Классика и реализм", callback_data="guide:classic")],
            [InlineKeyboardButton("Русский авангард и модернизм", callback_data="guide:avant")],
            [InlineKeyboardButton("Советское искусство и соцреализм", callback_data="guide:soviet")],
            [InlineKeyboardButton("Современное искусство", callback_data="guide:contemporary")],
            [InlineKeyboardButton("⬅️ В меню", callback_data="back")],
        ]
    )


def _guide_classic_places_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1️⃣ Третьяковка (Лаврушинский)", callback_data="guide:classic:tretyakov_lavrushinsky"
                )
            ],
            [
                InlineKeyboardButton(
                    "2️⃣ Третьяковка (Кадашевская)", callback_data="guide:classic:tretyakov_kadashevskaya"
                )
            ],
            [
                InlineKeyboardButton(
                    "3️⃣ ГМИИ Пушкин (осн.)", callback_data="guide:classic:pushkin_main"
                )
            ],
            [InlineKeyboardButton("⬅️ К путеводителю", callback_data="guide")],
        ]
    )


def _guide_avant_places_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1️⃣ Музей авангарда (Шаболовка)", callback_data="guide:avant:shabolovka_museum"
                )
            ],
            [
                InlineKeyboardButton(
                    "2️⃣ Маршрут «Авангард на Шаболовке»", callback_data="guide:avant:shabolovka_walk"
                )
            ],
            [
                InlineKeyboardButton(
                    "3️⃣ Еврейский музей / Центр авангарда", callback_data="guide:avant:jewish_museum"
                )
            ],
            [
                InlineKeyboardButton(
                    "4️⃣ Новая Третьяковка (авангард)", callback_data="guide:avant:tretyakov_new"
                )
            ],
            [InlineKeyboardButton("⬅️ К путеводителю", callback_data="guide")],
        ]
    )


def _guide_soviet_places_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1️⃣ Новая Третьяковка (соцреализм)", callback_data="guide:soviet:tretyakov_soviet"
                )
            ],
            [
                InlineKeyboardButton(
                    "2️⃣ Всероссийский музей декоративного искусства", callback_data="guide:soviet:vmdpni"
                )
            ],
            [
                InlineKeyboardButton(
                    "3️⃣ Советские мозаики и панно", callback_data="guide:soviet:mosaics"
                )
            ],
            [InlineKeyboardButton("⬅️ К путеводителю", callback_data="guide")],
        ]
    )


def _guide_contemp_places_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("1️⃣ MMOMA", callback_data="guide:contemporary:mmoma")],
            [InlineKeyboardButton("2️⃣ Гараж", callback_data="guide:contemporary:garage")],
            [InlineKeyboardButton("3️⃣ МАММ", callback_data="guide:contemporary:mamm")],
            [InlineKeyboardButton("4️⃣ Винзавод", callback_data="guide:contemporary:winzavod")],
            [InlineKeyboardButton("⬅️ К путеводителю", callback_data="guide")],
        ]
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            START_MESSAGE,
            reply_markup=build_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            START_MESSAGE,
            reply_markup=build_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/help — эта справка\n"
        "Используйте кнопки в главном меню, чтобы читать разделы и составить маршрут."
    )
    await update.message.reply_text(text)


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()

    data = query.data or ""
    if data == "back":
        if query.message:
            await query.message.reply_text(
                START_MESSAGE,
                reply_markup=build_main_keyboard(),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
        return

    if data == "info:moscow":
        text = (
            "*Узнать о Москве*\n\n"
            "Москва — крупнейший художественный центр России: именно здесь находятся главные собрания русского искусства, "
            "которые формируют представление о культуре всей страны. В Третьяковской галерее можно увидеть путь московской "
            "и общерусской живописи от древнерусской иконописи до картин передвижников и мастеров XX века (онлайн-коллекция: "
            "https://gallerix.ru/album/GTG, сайт галереи: https://tretyakovskaja.ru). Государственный музей изобразительных искусств "
            "имени А.С. Пушкина дополняет образ Москвы как «моста» между Россией и Европой: его коллекция показывает, как столичные "
            "художники и зрители вступали в диалог с мировым искусством (электронный каталог: https://collection.pushkinmuseum.art).\n\n"
            "Чтобы лучше понять художественную Москву, можно начать с книг, которые напрямую связаны с её музеями и экспозициями. "
            "Про русскую живопись и московские залы передвижников помогут издания «Русские художники-передвижники» Ирины Кравченко "
            "(например, описание: https://www.moscowbooks.ru/book/1205821/, https://www.labirint.ru/books/550453/) и альбом "
            "«Передвижники. Художники-передвижники и самые важные картины» (https://www.litres.ru/book/uliya-varencova/peredvizhniki-"
            "hudozhniki-peredvizhniki-i-samye-vazhnye-kar-51611144/) — многие репродукции из этих книг можно увидеть «вживую» именно "
            "в московских музеях. А чтобы увидеть, как Москва стала центром русского авангарда и эксперимента, подойдут подборка "
            "«Книги о русском авангарде» от издательства АСТ (https://ast.ru/top/knigi-o-russkom-avangarde/) и книга Андрея Сарабьянова "
            "«Русский авангард. И не только» (https://www.labirint.ru/books/961444/) — они хорошо объясняют контекст работ, которые сегодня "
            "экспонируются в московских коллекциях и выставках."
        )
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Вернуться в меню", callback_data="back")]]
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return

    if data == "artists":
        text = (
            "*Московские художники*\n\n"
            "Москва — это не только столица, но и родной город для многих художников, которые здесь родились, "
            "выросли и связали с ней своё творчество. Их картины часто показывают московские улицы, дворы и жителей, "
            "а биографии тесно связаны с московскими школами, мастерскими и выставками.\n\n"
            "Примеры московских художников:\n\n"
            "• Юрий Иванович Пименов (1903–1977) — родился в Москве, учился и работал в столице, "
            "один из самых узнаваемых художников XX века. Прославился лирическими городскими сценами "
            "и образом «новой, современной Москвы» — автомобили, улицы, театральная жизнь. (https://izvestnye-lyudi.ru/person/yurij-ivanovich-pimenov/)\n\n"
            "• Дмитрий Петрович Плавинский (1937–2012) — родился в Москве и стал одним из ярких представителей "
            "неофициального искусства второй половины XX века. В его живописи часто соединяются мотивы истории, "
            "архитектуры и городского пространства. (https://izvestnye-lyudi.ru/person/dmitrij-petrovich-plavinskij/)\n\n"
            "• Валерий Сергеевич Чтак (1981–2024) — родился в Москве, художник-концептуалист и стрит-арт автор, участник московских "
            "художественных проектов. Его произведения связаны с языком городской среды, текстами и визуальными высказываниями "
            "о жизни в мегаполисе. (https://vladey.net/ru/artist/valeriy-chtak)\n\n"
            "Где дальше искать московских художников:\n"
            "Подборка «Художники, родившиеся в Москве» с краткими биографиями и датами: "
            "https://izvestnye-lyudi.ru/moskovskaya-oblast/moskovskaya-aglomeraciya/moskva/?list=hudozhniki\n\n"
            "Ознакомиться с работами данных авторов:"
        )
        await query.edit_message_text(
            text,
            reply_markup=_artist_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return

    if data == "guide":
        text = (
            "*Путеводитель*\n\n"
            "В этом разделе собраны маршруты по Москве, привязанные к разным художественным стилям. "
            "Вы выбираете интересующее направление и получаете список мест в городе, где этот стиль можно «увидеть вживую».\n\n"
            "*Классика и реализм*\n"
            "Маршруты по музеям и локациям, где представлены шедевры классической живописи, передвижники и реалистические пейзажи.\n\n"
            "*Русский авангард и модернизм*\n"
            "Пункты, связанные с художниками и архитектурой начала XX века, рождением авангарда и новыми художественными формами.\n\n"
            "*Советское искусство и соцреализм*\n"
            "Объекты и музеи, показывающие искусство советского периода: крупные полотна, монументальные композиции и образы города эпохи СССР.\n\n"
            "*Современное искусство*\n"
            "Места, где можно увидеть актуальные выставки, креативные кластеры, галереи и уличное искусство сегодняшней Москвы."
        )
        if query.message:
            await query.message.reply_text(
                text,
                reply_markup=_guide_classic_keyboard(),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
        return

    if data == "guide:classic":
        caption = (
            "*Классика и реализм*\n\n"
            "1️⃣ Государственная Третьяковская галерея, Лаврушинский переулок\n"
            "Главное собрание русской классической живописи и реализма XIX – начала XX века, включая передвижников.\n\n"
            "2️⃣ Новый корпус Третьяковской галереи на Кадашевской набережной (выставка «Передвижники»)\n"
            "Крупная экспозиция, целиком посвящённая русскому реализму и Товариществу передвижных художественных выставок.\n\n"
            "3️⃣ Государственный музей изобразительных искусств им. А.С. Пушкина (основное здание)\n"
            "Европейская классическая живопись и скульптура, старые мастера — важный блок для понимания академической традиции и реалистической школы."
        )
        if query.message:
            if os.path.exists(REALISM_IMAGE_PATH):
                with open(REALISM_IMAGE_PATH, "rb") as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=_guide_classic_places_keyboard(),
                    )
            else:
                await query.message.reply_text(
                    caption,
                    reply_markup=_guide_classic_places_keyboard(),
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
        return

    if data.startswith("guide:classic:"):
        slug = data.split(":", 2)[2]
        detail = GUIDE_CLASSIC_DETAILS.get(slug)
        if not detail:
            await query.message.reply_text("Детали маршрута недоступны.")
            return
        detail_text = (
            f"*{detail['title']}*\n\n"
            f"{detail['desc']}\n"
            f"Адрес: {detail['address']}\n"
            f"Сайт: {detail['site']}"
        )
        image_path = GUIDE_CLASSIC_IMAGES.get(slug)
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=detail_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=_guide_classic_places_keyboard(),
                )
        else:
            await query.message.reply_text(
                detail_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=_guide_classic_places_keyboard(),
            )
        return

    if data == "guide:avant":
        caption = (
            "*Русский авангард и модернизм*\n\n"
            "1️⃣ Музей авангарда на Шаболовке (Галерея «На Шаболовке»)\n"
            "Экспозиция о конструктивизме и Шуховской башне в жилмассиве 1920–1930-х.\n\n"
            "2️⃣ Пешеходный маршрут «Авангард на Шаболовке»\n"
            "Дом-коммуна, школа‑«гигант», конструктивистские дома вокруг Шуховской башни.\n\n"
            "3️⃣ Еврейский музей и Центр толерантности (Центр авангарда)\n"
            "Выставки русского авангарда с работами мастеров начала XX века.\n\n"
            "4️⃣ Третьяковская галерея (Новая Третьяковка)\n"
            "Крупные проекты об авангарде: Кандинский, Малевич, Татлин, Попова и др."
        )
        if query.message:
            if os.path.exists(AVANT_IMAGE_PATH):
                with open(AVANT_IMAGE_PATH, "rb") as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=_guide_avant_places_keyboard(),
                    )
            else:
                await query.message.reply_text(
                    caption,
                    reply_markup=_guide_avant_places_keyboard(),
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
        return

    if data.startswith("guide:avant:"):
        slug = data.split(":", 2)[2]
        detail = GUIDE_AVANT_DETAILS.get(slug)
        if not detail:
            await query.message.reply_text("Детали маршрута недоступны.")
            return
        detail_text = (
            f"*{detail['title']}*\n\n"
            f"{detail['desc']}\n"
            f"Адрес: {detail['address']}\n"
            f"Сайт: {detail['site']}"
        )
        image_path = GUIDE_AVANT_IMAGES.get(slug)
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=detail_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=_guide_avant_places_keyboard(),
                )
        else:
            await query.message.reply_text(
                detail_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=_guide_avant_places_keyboard(),
            )
        return

    if data == "guide:soviet":
        caption = (
            "*Советское искусство и соцреализм*\n\n"
            "1️⃣ Новая Третьяковка (Крымский Вал)\n"
            "Постоянная экспозиция искусства XX века и проекты по соцреализму.\n\n"
            "2️⃣ Всероссийский музей декоративного искусства\n"
            "Показы живописи, скульптуры, предметов быта советского периода.\n\n"
            "3️⃣ Советские мозаики и панно Москвы\n"
            "Мозаичная карта: метро, фасады, интерьеры с визуальным кодом эпохи."
        )
        if query.message:
            if os.path.exists(SOVIET_IMAGE_PATH):
                with open(SOVIET_IMAGE_PATH, "rb") as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=_guide_soviet_places_keyboard(),
                    )
            else:
                await query.message.reply_text(
                    caption,
                    reply_markup=_guide_soviet_places_keyboard(),
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
        return

    if data.startswith("guide:soviet:"):
        slug = data.split(":", 2)[2]
        detail = GUIDE_SOVIET_DETAILS.get(slug)
        if not detail:
            await query.message.reply_text("Детали маршрута недоступны.")
            return
        detail_text = (
            f"*{detail['title']}*\n\n"
            f"{detail['desc']}\n"
            f"Адрес: {detail['address']}\n"
            f"Сайт: {detail['site']}"
        )
        image_path = GUIDE_SOVIET_IMAGES.get(slug)
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=detail_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=_guide_soviet_places_keyboard(),
                )
        else:
            await query.message.reply_text(
                detail_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=_guide_soviet_places_keyboard(),
            )
        return

    if data == "guide:contemporary":
        caption = (
            "*Современное искусство*\n\n"
            "1️⃣ Московский музей современного искусства (MMOMA)\n"
            "Первый музей современного искусства в России: несколько площадок, коллекция и крупные выставки.\n\n"
            "2️⃣ Музей «Гараж» (Парк Горького)\n"
            "Ключевой центр актуального искусства: международные проекты, перформансы, лекции, фестивали.\n\n"
            "3️⃣ Мультимедиа Арт Музей, Москва (МАММ)\n"
            "Семь этажей фото-, видео- и медиаискусства, фокус на современном визуальном языке.\n\n"
            "4️⃣ Центр современного искусства «Винзавод»\n"
            "Галереи, мастерские, институт «БАЗА», фестивали и ярмарки в бывшем заводском кластере."
        )
        if query.message:
            if os.path.exists(CONTEMP_IMAGE_PATH):
                with open(CONTEMP_IMAGE_PATH, "rb") as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=_guide_contemp_places_keyboard(),
                    )
            else:
                await query.message.reply_text(
                    caption,
                    reply_markup=_guide_contemp_places_keyboard(),
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
        return

    if data.startswith("guide:contemporary:"):
        slug = data.split(":", 2)[2]
        detail = GUIDE_CONTEMP_DETAILS.get(slug)
        if not detail:
            await query.message.reply_text("Детали маршрута недоступны.")
            return
        detail_text = (
            f"*{detail['title']}*\n\n"
            f"{detail['desc']}\n"
            f"Адрес: {detail['address']}\n"
            f"Сайт: {detail['site']}"
        )
        image_path = GUIDE_CONTEMP_IMAGES.get(slug)
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=detail_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=_guide_contemp_places_keyboard(),
                )
        else:
            await query.message.reply_text(
                detail_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=_guide_contemp_places_keyboard(),
            )
        return

    if data.startswith("artist:"):
        artist = data.split(":", 1)[1]
        meta = ARTIST_DIR_MAP.get(artist)
        if not meta:
            await query.message.reply_text("Автор не найден.")
            return
        base_dir = os.path.join(os.path.dirname(__file__), "images", meta["dir"])
        if not os.path.isdir(base_dir):
            await query.message.reply_text("Изображения не найдены для этого автора.")
            return
        files = [os.path.join(base_dir, f"{i}.jpg") for i in range(1, 5)]
        # Некоторые файлы могут быть .jpeg — подменяем при отсутствии .jpg
        resolved_files = []
        for path in files:
            if os.path.exists(path):
                resolved_files.append(path)
            else:
                alt = path[:-4] + ".jpeg"
                if os.path.exists(alt):
                    resolved_files.append(alt)
        if not resolved_files:
            await query.message.reply_text("Изображения не найдены для этого автора.")
            return
        media = [
            InputMediaPhoto(
                media=open(fp, "rb"),
                caption=f"Работы {meta['title_gen']}",
            )
            if idx == 0
            else InputMediaPhoto(media=open(fp, "rb"))
            for idx, fp in enumerate(resolved_files)
        ]
        await query.message.reply_media_group(media=media)
        await query.message.reply_text(
            "Выберите другого автора или вернитесь в меню.",
            reply_markup=_artist_keyboard(),
        )
        return


    if data == "authors":
        text = "*Авторы*\n\nМанин Андрей БИБ254\n\nИбрагимова Афина БИТ252"
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ В меню", callback_data="back")]]
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return

    await query.edit_message_text(
        "Неизвестное действие. Вернитесь в меню.",
        reply_markup=build_main_keyboard(),
        disable_web_page_preview=True,
    )


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Переменная окружения BOT_TOKEN не установлена.")

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(CallbackQueryHandler(on_callback))

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()



