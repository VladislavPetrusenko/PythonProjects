import configparser
import os
import time
import sys
from logger_setup import setup_logger
from cloud_storage import CloudStorage
from sync_engine import initial_sync, sync_once

def read_config(config_path: str) -> dict:
    """
    Читает файл config.ini и возвращает словарь с параметрами. При ошибках завершает программу с сообщением.
    :param config_path: путь к файлу конфигурации
    :return: (dict) словарь с параметрами
    """
    config = configparser.ConfigParser() # создание объекта парсера.
    try:
        config.read(config_path, encoding = "utf-8") # чтение файла. Кодировка UTF-8 для поддержки русских путей
        if "Settings" not in config.sections(): # проверка наличия секции [Settings]
            print("Ошибка: в config.ini отсутствует секция [Settings]") # сообщение пользователю
            sys.exit(1) # завершение программы с кодом ошибки
        section = config["Settings"] # получение секции для удобства
        required_keys = ["local_folder", "cloud_folder", "token", "sync_interval", "log_file"] # список обязательных параметров.

        for key in required_keys: # цикл проверки наличия каждого параметра
            if key not in section: # если параметр отсутствует
                print(f"Ошибка: в секции [Settings] отсутствует параметр {key}")
                sys.exit(1)

        local_folder = section["local_folder"]
        cloud_folder = section["cloud_folder"]
        token = section["token"]
        log_file = section["log_file"]

        try:
            sync_interval = int(section["sync_interval"])
            if sync_interval <= 0:
                print("Ошибка: sync_interval должен быть положительным числом")
                sys.exit(1)
        except ValueError:
            print("Ошибка: sync_interval должен быть целым числом")
            sys.exit(1)

        return {
            "local_folder": local_folder,
            "cloud_folder": cloud_folder,
            "token": token,
            "sync_interval": sync_interval,
            "log_file": log_file
        }
    except Exception as e:
        print(f"Ошибка чтения config.ini: {e}")
        sys.exit(1)

def main():
    """
    Главная логика программы: чтение конфига, инициализация, синхронизация, цикл
    """
    config_params = read_config("config.ini")
    local_folder = config_params["local_folder"]
    cloud_folder = config_params["cloud_folder"]
    token = config_params["token"]
    sync_interval = config_params["sync_interval"]
    log_file = config_params["log_file"]

    if not os.path.isdir(local_folder):
        print(f"Ошибка: локальная папка '{local_folder}' не существует или не является директорией")
        sys.exit(1)

    logger = setup_logger(log_file)
    logger.info(f"Программа запущена. Синхронизируемая папка: {local_folder}")

    try:
        cloud_storage = CloudStorage(token, cloud_folder)
        logger.info("Облачное хранилище успешно инициализировано")
    except Exception as e:
        logger.error(f"Не удалось инициализировать облачное хранилище: {e}")
        print(f"Ошибка: {e}")
        sys.exit(1)

    try:
        previous_state = initial_sync(local_folder, cloud_storage)
        logger.info("Первая синхронизация успешно завершена")
    except Exception as e:
        logger.error(f"Ошибка при первой синхронизации: {e}")
        print(f"Не удалось выполнить начальную синхронизацию: {e}. Программа завершена.")
        sys.exit(1)

    while True:
        try:
            time.sleep(sync_interval)
            logger.info("Запуск очередной синхронизации")
            previous_state = sync_once(local_folder, cloud_storage, previous_state)
            logger.info("Очередная синхронизация завершена")
        except KeyboardInterrupt:
            logger.info("Программа остановлена пользователем")
            break
        except Exception as e:
            logger.error(f"Ошибка в цикле синхронизации: {e}")
    logger.info("Программа завершена")

if __name__ == "__main__":
    main()