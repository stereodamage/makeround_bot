import asyncio
import logging
import os
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from utils import roundify

TOKEN = getenv("BOT_TOKEN", False)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(F.video)
async def video_handler(message: types.Message) -> None:
    await bot.download(message.video.file_id,
                       destination=f"tmp/{message.video.file_id}.mp4", timeout=60)
    # create rounded video from OG
    roundified = await roundify(f"tmp/{message.video.file_id}.mp4")
    # send as video note
    await bot.send_video_note(message.chat.id, types.FSInputFile(roundified))
    # clean up
    os.remove(f"tmp/{message.video.file_id}.mp4")
    os.remove(f"tmp/{message.video.file_id}_r.mp4")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    if TOKEN is False:
        raise ValueError("BOT_TOKEN environment variable is not set")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
