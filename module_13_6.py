from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StateGroup):                                             # наследованный от StatesGroup
    age = State()                                                        # 3 объекта класса
    growth = State()
    weight = State()


@dp.callback_query_handler(text = 'calories')                            # handler исправлен'
async def set_age(call):
    await call.message.answer('Введите свой возраст:')                   # ответ на сообщение
    await UserState.age.set()                                            # ввода возраста в атрибут





kb = ReplyKeyboardMarkup(resize_keyboard=True)                      # клавиатура и её размеры
button = KeyboardButton(text = 'Рассчитать')                        # кнопка 1
kb.add(button)                                                      # добавление в клавиатуру кнопки
button_2 = KeyboardButton(text= 'Информация')                       # кнопка 2
kb.add(button_2)                                                    # добавление в клавиатуру кнопки







kb_menu = InlineKeyboardMarkup(resize_keyboard=True)
button_3 = KeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')    # кнопка 3
kb.add(button_3)                                                                            # добавление кнопки
button_4 = KeyboardButton(text= 'Формулы расчёта', callback_data = 'formulas')              # кнопка 4
kb.add(button_4)                                                                            # добавление кнопки






@dp.message_handler(text = 'Рассчитать')
async def inform(message):
    await message.answer('Выберите опцию:', reply_markup = kb_menu)



@dp.callback_query_handler(text = 'formulas')    #call back дата, на какую кнопку будет отрабатывать handler
async def get_formulas(call):
    await call.message.answer("6.25 * рост(см) + 10 * вес(кг) - 5 * возраст(лет) + 5 для мужчин\n6.25 * рост(см)"
                              "+ 10 * вес(кг) - 5 * возраст(лет) - 161 для женщин", reply_markup=kb_menu)
    await call.answer()





@dp.message_handler(commands = ['start'])                       # хендлер на вызов команды
async def start(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup = kb)
    # возвращение ответа, reply_markup показывает клавиатуру


@dp.message_handler(text = 'Рассчитать')                        # хендлер на вызов кнопки
async def inform(message):
    await message.answer('Рассчитать')







@dp.message_handler(state = UserState.age)                      # реагирует на переданное состояние UserState.age
async def set_growth(message, state):
    await state.update_data(age=message.text)                   # обновляет данные в состоянии age
    await message.answer(f"Введите свой рост:")                 # сообщение после ввода
    await UserState.growth.set()                                # ввод роста в атрибут UserState.growth


@dp.message_handler(state=UserState.growth)                     # реагирует на переданное состояние UserState.growth.
async def set_weight(message, state):
    await state.update_data(growth=message.text)                # обновляет данные в состоянии growth
    await message.answer(f"Введите свой вес:")                  # сообщение после ввода
    await UserState.weight.set()                                # ввод роста в атрибут UserState.weight


@dp.message_handler(state=UserState.weight)                     # реагирует на переданное состояние UserState.weight.
async def send_calories(message, state):
    await state.update_data(weight=message.text)                # обновляет данные в состоянии weight
    await message.answer(f"Введите свой вес:")                  # сообщение после ввода
    data = await state.get_data()                               # данные сохранены в переменную data
    norma_calories_man = 6.25 * float(data['growth']) + 10 * float(data['weight']) - 5 * float(data['age']) + 5     # для мужчин
    norma_calories_woman = 6.25 * float(data['growth']) + 10 * float(data['weight']) - 5 * float(data['age']) - 161 # для женщин
    await message.answer(f' Норма калорий составляет для мужчины: {norma_calories_man:.2f}, '
                         f'для женщины: {norma_calories_woman:.2f}.')                   # Результат вычисления
    await state.finish()                                        # закрытие машины


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

