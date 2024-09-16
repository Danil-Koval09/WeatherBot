from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import requests

Open_Weather_Api = ''

bot = Bot(token='')
dp = Dispatcher(bot, storage=MemoryStorage())


class WeatherState(StatesGroup):
    city = State()


@dp.message_handler(commands=['start', 'hello', 'привет'])
async def start(message: types.Message):
    await message.answer('Привет! Тут ты можешь узнать погоду любого города, для этого напиши название города')




async def get_weather(city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Open_Weather_Api}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


async def send_weather(message: types.Message, data):
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']

    await message.answer(f"Погода в {data['name']}:\n"
                        f"Температура: {temp}°C\n"
                        f"Описание: {description}\n"
                        f"Влажность: {humidity}%\n"
                        f"Давление: {pressure} Паскаль\n"
                        f"Скорость ветра: {wind_speed}м/с")



@dp.message_handler(state=None)
async def name_city(message: types.Message, state: FSMContext):
    city = message.text
    data = await get_weather(city)
    if data:
        await send_weather(message, data)
    else:
        await message.answer('Город не найден ☹. Введите название города правильно')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)