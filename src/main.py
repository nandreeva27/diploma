import pandas as pd
from telegram import Bot
import logging
import asyncio
import os

# Настройки Telegram API
with open("token.txt", encoding='utf-8') as token:
    TELEGRAM_BOT_TOKEN = token.readline()


# Директории
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
log_path = os.path.join(parent_dir, 'logs', 'log.txt')
script_dir = os.path.join(parent_dir, 'scripts')
table_path = os.path.join(parent_dir, 'tables', 'students.csv')

# Логирование

logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Инициализация Telegram-бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Асинхронная функция отправки сообщения
async def send_telegram_message(telegram_id, message):
    try:
        await bot.send_message(chat_id=telegram_id, text=message)
        logging.info(f"Сообщение успешно отправлено: Telegram ID {telegram_id}")
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения (Telegram ID {telegram_id}): {e}")

# Асинхронный основной процесс
async def main():
    # Чтение данных из CSV-файла
    try:
        data = pd.read_csv(table_path, delimiter=';')
        logging.info("Файл students.csv успешно загружен.")
    except Exception as e:
        logging.error(f"Ошибка при загрузке файла students.csv: {e}")
        exit("Ошибка: невозможно загрузить файл students.csv")

    # Удаляем лишние пробелы в названиях колонок
    data.columns = data.columns.str.strip()


    # Итерация по данным
    for _, row in data.iterrows():
        name = row.get('name', 'Ученик')
        parent_name = row.get('parent_name', 'Уважаемый родитель')
        ege_result = row.get('ege_results', None)
        telegram_id = row.get('telegram_id', None)
        sex = row.get('sex', None)
        print(telegram_id)

        # Пропускаем, если нет Telegram ID
        if pd.isna(telegram_id):
            logging.warning(f"Пропущен пользователь {name}: отсутствует Telegram ID.")
            continue

        # Формируем сообщение
        if ege_result:
            ege_result = int(ege_result)
            if ege_result >= 80:
                script_template = open(os.path.join(script_dir, 'script_1.txt'), encoding='utf-8').read()
            elif 48 <= ege_result < 80:
                script_template = open(os.path.join(script_dir, 'script_2.txt'), encoding='utf-8').read()
            else:
                script_template = open(os.path.join(script_dir, 'script_3.txt'), encoding='utf-8').read()
            # Отправляем сообщение
            message = eval(f"f'''{script_template}'''")
            await send_telegram_message(telegram_id, message)
        else:
            logging.info(f"Нет результатов последнего пробного экзамена у {name}")



# Запуск основного процесса
if __name__ == "__main__":
    asyncio.run(main())
