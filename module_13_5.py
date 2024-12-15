# Домашнее задание по теме "Клавиатура кнопок".

# Задача "Меньше текста, больше кликов":

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "Token"
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

# Создаем клавиатуру
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)

# Создаем обработчики кнопок
@dp.message_handler(commands= 'start')
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.",reply_markup=kb)

@dp.message_handler(text= 'Информация')
async def send_information(message: types.Message):
    await message.answer("Информация о боте")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    """
        Обработчик состояния для получения возраста.
        Сохраняет возраст и переходит к состоянию для получения роста
        """
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer('Введите свой рост:')

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    """
        Обработчик состояния для получения роста.
        Сохраняет рост и переходит к состоянию для получения веса
        """
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес:')

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    """
        Обработчик состояния для получения веса.
        Рассчитывает норму калорий и завершает цепочку состояний
        """
    await state.update_data(weight=message.text)
    data = await state.get_data()

    # Получаем данные из состояния
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Используем упрощенную формулу Миффлина - Сан Жеора для расчета нормы калорий
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Для мужчин
    #calories = 10 * weight + 6.25 * growth - 5 * age - 161 # Для женщин

    await message.answer(f'Ваша норма калорий: {calories:.2f}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Привет! Введите команду /start, чтобы начать общение')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)