def translate(text, lang):
    translations = {
        'Choose service category': {
            'uz': "Siz xizmat kategoriyasiga o'tdingiz",
            'en': "Choose service category",
            'ru': "Вы перешли в категорию услуг"
        },
        'Choose service type:': {
            'uz': "Xizmat turini tanlang:",
            'en': "Choose service type:",
            'ru': "Выберите тип услуги:"
        },
        'Choose the way of communication': {
            'uz': "Aloqa usulini tanlang",
            'en': "Choose the way of communication",
            'ru': "Выберите способ связи"
        },
        'Enter name once more:': {
            'uz': "Ismingizni yana kiriting:",
            'en': "Enter name once more:",
            'ru': "Введите имя еще раз:"
        },
        'Enter phone number once more': {
            'uz': "Telefon raqamingizni qayta kiriting",
            'en': "Enter phone number once more",
            'ru': "Введите номер телефона еще раз"
        },
        'Enter location once more': {
            'uz': "Joylashuvingizni yana kiriting",
            'en': "Enter location once more",
            'ru': "Введите местоположение еще раз"
        },
        'Enter verification:': {
            'uz': "Tasdiqlash kodini kiriting:",
            'en': "Enter verification:",
            'ru': "Введите код подтверждения:"
        },
        'Welcome to our main page': {
            'uz': "Bizning asosiy sahifamizga xush kelibsiz",
            'en': "Welcome to our main page",
            'ru': "Добро пожаловать на нашу главную страницу"
        },
        'Please choose only one of the languages': {
            'uz': "Iltimos, faqat bitta tilni tanlang",
            'en': "Please choose only one of the languages",
            'ru': "Пожалуйста, выберите только один язык"
        },
        'You have no orders yet.': {
            'uz': "Sizda hali buyurtmalar yo‘q.",
            'en': "You have no orders yet.",
            'ru': "У вас пока нет заказов."
        },
        'Order created successfully': {
            'uz': "Buyurtma muvaffaqiyatli yaratildi",
            'en': "Order created successfully",
            'ru': "Заказ успешно создан"
        },
        'Order cancelled successfully': {
            'uz': "Buyurtma muvaffaqiyatli bekor qilindi",
            'en': "Order cancelled successfully",
            'ru': "Заказ успешно отменен"
        },
        'Settings menu': {
            'uz': "Sozlamalar menyusi",
            'en': "Settings menu",
            'ru': "Меню настроек"
        },
        'Language updated successfully': {
            'uz': "Til muvaffaqiyatli yangilandi",
            'en': "Language updated successfully",
            'ru': "Язык успешно обновлен"
        },
        '📞 Phone number':{
            'ru':'📞 Номер телефона',
            'uz':"📞 Telefon raqami",
            'en':'📞 Phone number'
        },
        'Contact our poeple: +998949252945':{
            'ru':'Свяжитесь с нашими людьми: +998777070707',
            'uz':"Bizning odamlar bilan bog'laning: +998777070707",
            'en':'Contact our poeple: +998777070707',
        },
        '⬅️ Back':{
            'uz':'⬅️ Orqaga',
            'ru':'⬅️ Назад',
            'en':'⬅️ Back'
        },
        "You don't have previous step, just enter service category, or cancel it":{
            'uz':"Sizda oldingi qadam yo‘q, faqat xizmat toifasini kiriting yoki bekor qiling.",
            'ru':"У вас нет предыдущего шага, просто введите категорию услуги или отмените.",
            'en':"You don't have previous step, just enter service category, or cancel it"
        },
        "Choose langugae!!":{
            'en':'Choose langugae!!',
            'ru':'Выберите язык!!',
            'uz':'Tilni tanlang!!'
        },
        '❌ Cancel order':{
            'en':'❌ Cancel order',
            'ru':'❌ Отменить заказ',
            'uz':'❌ Buyurtmani bekor qilish'
        },
        'My Orders':{
            'uz':'Mening buyurtmalarim',
            'en':'My Orders',
            'ru':'Мои заказы',
        },
        'Services':{
            'en':'Services',
            'uz':'Xizmatlar',
            'ru':'Услуги'
        },
        '⚙️ Settings':{
            'uz':'⚙️ Sozlamalar',
            'en':'⚙️ Settings',
            'ru':'⚙️ Настройки',
        },
        "⬅️ Back":{
            'uz':'⬅️ Orqaga',
            'en':'⬅️ Back',
            'ru':'⬅️ Назад',
        },
        '✅ Verify order':{
            'en':'✅ Verify order',
            'uz':'✅ Buyurtmani tasdiqlash',
            'ru':'✅ Подтвердить заказ',
        },
        '📌 Order the service':{
            'en':'📌 Order the service',
            'ru':'📌 Заказать услугу',
            'uz':'📌 Xizmatga buyurtma berish'
        },
        'Choose service category':{
            'en':'Choose service category',
            'uz':'Xizmat turini tanlang',
            'ru':'Выберите категорию услуги'
        },
        'Choose services':{
            'en':'Choose services',
            'uz':'Xizmatlarni tanlang',
            'ru':'Выберите услуги'
        },
        'Change Language':{
            'en':'Change Language',
            'ru':'Изменить язык',
            'uz':"Tilni o'zgartirish"
        },
        'Enter your full name':{
            "uz": "To'liq ismingizni kiriting",
            "en": "Enter your full name",
            "ru": "Введите ваше полное имя"
        },
        'Enter your valid phone number':{
            "uz": "Yaroqli telefon raqamingizni kiriting",
            "en": "Enter your valid phone number",
            "ru": "Введите ваш действительный номер телефона"
        },
        'Please provide your full location!!!':{
            "uz": "Iltimos, to'liq manzilingizni kiriting!!!",
            "en": "Please provide your full location!!!",
            "ru": "Пожалуйста, укажите ваш полный адрес!!!"
        },
        "O'lchovni kiriting":{
            'uz':"Sizda qancha maydon bor",
            'ru':"Введите размер",
            'en':'Enter the measurement'
        },
        'Narxi:':{
            'uz':'Narxi:',
            "ru":"Цена:",
            "en":"Price:"
        }

    }
    
    return translations.get(text, {}).get(lang, text)

translations = {
    "service_name": {
        "uz": "Xizmat nomi",
        "en": "Service name",
        "ru": "Название услуги"
    },
    "full_name": {
        "uz": "Ism Familiya",
        "en": "Full Name",
        "ru": "ФИО"
    },
    "phone_number": {
        "uz": "Telefon raqam",
        "en": "Phone number",
        "ru": "Номер телефона"
    },
    "location": {
        "uz": "Manzil",
        "en": "Location",
        "ru": "Адрес"
    }
}