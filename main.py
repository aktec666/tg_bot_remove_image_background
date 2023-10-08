import asyncio
import logging
import sys
import shutil
import requests
import time
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from rembg import remove
from aiogram.types import FSInputFile

import config

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет!, {hbold(message.from_user.full_name)}!\n Отправь мне картинку и я уберу фон!")

bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)

async def main() -> None:
    await dp.start_polling(bot)


# @dp.message_handler(content_types=['photo'])
# async def handle_docs_photo(message):
#     await message.photo[-1].download('images/test.jpg')

def download_image(fileID, file):
    r = requests.get(
        "https://api.telegram.org/file/bot" + config.TOKEN + "/" + file.file_path,
        timeout=None,
        stream=True,
    )
    with open("images/test.png", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

def remove_background():
    input_path = 'images/test.png'
    output_path = 'images/result.png'

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

@dp.message()
async def echo_handler(message: types.input_media_photo) -> None:
    fileID = message.photo[-1].file_id
    file = await bot.get_file(fileID)
    download_image(fileID, file)
    remove_background()
    result = FSInputFile("images/result.png")
    await bot.send_photo(message.from_user.id, result)

   
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())