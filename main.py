import argparse
import sys
import time
import logging
import asyncio
from aiopathlib import AsyncPath
from aioshutil import copy2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('file_copy.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



async def copy_file(path_to, child) -> None:
    path_ext = path_to / child.suffix[1:]

    try:
        await path_ext.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Помилка створення папки {path_ext}: {e}")

    try:
        await copy2(child, path_ext)
    except OSError as e:
        logger.error(f"Помилка копіювання файлу {child}: {e}")

async def read_folder(folder_from, folder_to) -> None:

    path_from = AsyncPath(folder_from)
    path_to = AsyncPath(folder_to)

    try:
        for child in path_from.iterdir():
            if await child.is_dir():
                await read_folder(child, path_to)
            elif await child.is_file():
                await copy_file(path_to, child)
    except OSError as e:
        logger.error(f"Помилка операцій з файлом чи папкою: {e}")

parser = argparse.ArgumentParser(description='Копіювання файлів з однієї папки в іншу')
parser.add_argument('folder_from', help='Шлях до папки з файлами')
parser.add_argument('folder_to', nargs='?', default='destination', help='Шлях до папки призначення')

try:
    args = parser.parse_args()
except SystemExit:
    logger.error('Помилка! Не вказаний шлях до папки з файлами. Спробуйте ще раз.')
    sys.exit(1)

start_time = time.time()
asyncio.run(read_folder(args.folder_from, args.folder_to))
logger.info('Час виконання: %s', time.time() - start_time)
