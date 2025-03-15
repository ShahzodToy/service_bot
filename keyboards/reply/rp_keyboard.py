from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from utils.transaltion import translate as __

lang_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="🇬🇧 English", ),
        ],
        [
            KeyboardButton(text="🇺🇿 Uzbek", ),
        ],
        [
            KeyboardButton(text="🇷🇺 Russian",)
        ]
            ],resize_keyboard=True
    )
def setting_menu(lang):
    return  ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=__('Change Language',lang))
            ]
        ],resize_keyboard=True
)

def main_menu(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=__('Services',lang)),
            KeyboardButton(text=__('My Orders',lang))
        ],
        [
            KeyboardButton(text=__('⚙️ Settings',lang))
        ]
    ], resize_keyboard=True
)

def back_keyboard(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=__('⬅️ Back',lang))
        ]
    ],resize_keyboard=True
)

def order_way(lang): 
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=__('📌 Order the service',lang)),
            KeyboardButton(text=__('📞 Phone number',lang))
        ],
        [
            KeyboardButton(text=__('⬅️ Back',lang))
        ]
    ], resize_keyboard=True
)

def phone_numbe_keyboard(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=__('📞 Phone number',lang), request_contact=True),
            ],
            [
                KeyboardButton(text=__('⬅️ Back',lang))
            ]
    ],resize_keyboard=True
)

def verify_order_keyboard(lang):
    return  ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=__('✅ Verify order',lang)),
                KeyboardButton(text=__('❌ Cancel order',lang))
            ],
            [
                KeyboardButton(text=__('⬅️ Back',lang))
            ]
    ],resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Barcha buyurtmalar'),
            KeyboardButton(text='Xizmatlar qo\'shish')
        ],
    ],resize_keyboard=True
)