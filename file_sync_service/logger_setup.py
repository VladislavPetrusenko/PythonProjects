import logging

def setup_logger(log_file_path: str) -> logging.Logger:
    """
    Настраивает логгер для записи в указанный файл.
    :param (str) log_file_path: путь к файлу лога (из config.ini)
    :return: logging.Logger: настроенный объект логгера
    """
    # Создаем логгер с именем "sync_logger"
    logger = logging.getLogger("sync_logger")
    # Устанавливаем уровень логирования: INFO и выше
    logger.setLevel(logging.INFO)

    # Создаем обработчик  для записи в файл
    file_handler = logging.FileHandler(log_file_path, encoding = "utf-8")
    # Определяем формат сообщений:
    #   - %(asctime)s - дата и время
    #   - %(levelname)s - уровень логирования
    #   - %(message)s - само сообщение, переданное в logger.info() / logger.error()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Привязываем формат к обработчику файла
    file_handler.setFormatter(formatter)
    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    return logger