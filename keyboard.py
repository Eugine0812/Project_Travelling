from aiogram import types
from aiogram.types import InlineKeyboardButton

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.InlineKeyboardButton(text="Рассылка"))
kb.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
kb.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
kb.add(types.InlineKeyboardButton(text="Статистика"))

kb_information = types.ReplyKeyboardMarkup().add("Туры по Беларуси", "Туры за границу").add("Календарь туров", "Понравился тур?")

kb_info_abroad = types.InlineKeyboardMarkup(row_width=1)
kb_info_abroad_btn1 = InlineKeyboardButton(text="🚜Джип тур в Карелию", url='https://psixtravel.by/tour/jeep-tur-karelia/')
kb_info_abroad_btn2 = InlineKeyboardButton(text="🚜Джип тур в Молдову", url='https://psixtravel.by/tour/jeep-tour-moldova/')
kb_info_abroad_btn3 = InlineKeyboardButton(text="🚜Джип туры в Грузию", url='https://psixtravel.by/tour/4h4-gruzija/')
kb_info_abroad.add(kb_info_abroad_btn1, kb_info_abroad_btn2, kb_info_abroad_btn3)

kb_info_belarus = types.InlineKeyboardMarkup(row_width=1)
kb_info_belarus_btn1 = InlineKeyboardButton(text="Байдарки + поход на болото + усадьба", url='https://psixtravel.by/tour/splav-boloto/')
kb_info_belarus_btn2 = InlineKeyboardButton(text="Сплав по рекам Узлянка-Нарочанка", url='https://psixtravel.by/tour/splav-uzljanka-narochanka/')
kb_info_belarus_btn3 = InlineKeyboardButton(text="Сплав! Бацька Нёман!", url='https://psixtravel.by/tour/splav-papa-neman/')
kb_info_belarus_btn4 = InlineKeyboardButton(text='Джип тур "War"', url='https://psixtravel.by/tour/jeep-tour-war/')
kb_info_belarus.add(kb_info_belarus_btn1, kb_info_belarus_btn2, kb_info_belarus_btn3, kb_info_belarus_btn4)

kb_info_admin = types.InlineKeyboardMarkup(row_width=1)
kb_info_admin_btn1 = InlineKeyboardButton(text="Переходите и жмите 'Заказать тур'", url="https://psixtravel.by/")
kb_info_admin.add(kb_info_admin_btn1)
