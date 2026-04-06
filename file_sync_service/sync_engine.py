import os
import logging
from typing import Dict, Set, Tuple

logger = logging.getLogger("sync_logger")

def get_local_files_info(local_folder: str) -> Dict[str, float]:
    """
    Сканирует локальную папку (только файлы, без подпапок) и возвращает словарь: имя файла - время последней модификации
    :param local_folder: (str) локальная папка
    :return: (dict) словарь с информацией об файлах
    """
    files_info = {} # инициализация пустого словаря для результата
    try:
        items = os.listdir(local_folder) # получаем список имён (файлов и папок) в указанной папке
        for item in items:
            item_path = os.path.join(local_folder, item) # формируем полный путь к элементу
            if os.path.isfile(item_path): # проверяем, является ли элемент файлом (а не папкой
                try:
                    mtime = os.path.getmtime(item_path) # получаем время последней модификации файла
                    files_info[item] = mtime # сохраняем в словарь
                except (OSError, PermissionError) as e: # если не удалось прочитать атрибуты файла
                    logger.error(f"Не удалось получить информацию о файле {item}: {e}") # запись ошибки в лог
    except (FileNotFoundError, PermissionError) as e: # если сама папка не найдена или нет доступа к ней
        logger.error(f"Не удалось прочитать локальную папку {local_folder}: {e}") # логируем ошибку
        return {} # возвращаем пустой словарь (синхронизация невозможна, но программа не падает)
    return files_info # возврат словаря с информацией о локальных файлах.

def get_cloud_files_info(cloud_storage) -> Set[str]:
    """
    Получает из облачного хранилища список имён файлов (через cloud_storage.get_info()) и возвращает множество имён.
    :param cloud_storage: объект класса CloudStorage
    :return: (set) множество имён
    """
    try:
        file_list = cloud_storage.get_info() # вызов метода, который возвращает информацию о файлах
        if not isinstance(file_list, list): # если по какой-то причине вернулось не список
            logger.error("Метод get_info вернул некорректный формат данных") # запись ошибки
            return set() # возвращаем пустое множество
        return set(file_list) # преобразуем список в множество для быстрого сравнения
    except Exception as e: # перехват любых неожиданных ошибок
        logger.error(f"Ошибка при получении списка файлов из облака: {e}")
        return set() # возвращаем пустое множество, чтобы синхронизация могла продолжиться

def compare_files(current_local: Dict[str, float], previous_local: Dict[str, float], cloud_files: Set[str]) -> Tuple[Set[str], Set[str]]:
    """
    Сравнивает локальные и облачные файлы и возвращает два множества
    :param current_local: текущие локальные файлы с mtime
    :param previous_local: состояние на момент предыдущей синхронизации
    :param cloud_files: множество имён файлов в облаке
    :return:
        1) to_upload — файлы, которые нужно загрузить (новые или изменённые).
        2) to_delete — файлы, которые нужно удалить из облака (удалены локально).
    """
    to_upload = set() # множество для файлов, которые надо загрузить
    to_delete = set() # множество для файлов, которые надо удалить из облака
    locally_deleted = cloud_files - set(current_local.keys()) # разность множеств: имена, которые есть в облаке, но нет в текущей локальной папке
    to_delete.update(locally_deleted) # добавляем в to_delete

    for filename, current_mtime in current_local.items(): # цикл по текущим локальным файлам
        if filename not in cloud_files: # если файла нет в облаке - он новый
            to_upload.add(filename) # добавляем в загрузку
        elif filename in previous_local: # если файл был в предыдущем состоянии
            previous_mtime = previous_local.get(filename) # получаем предыдущее время
        if current_mtime != previous_mtime: # если время изменилось
            to_upload.add(filename) # добавляем в загрузку
    return to_upload, to_delete # возвращаем два множества

def sync_once(local_folder: str, cloud_storage, previous_local_state: dict) -> dict:
    """
    Выполняет одну итерацию синхронизации: получает текущее состояние локальной папки, сравнивает с облаком и с
    предыдущим состоянием, загружает новые/изменённые файлы, удаляет из облака те, которых нет локально. Возвращает
    новое состояние локальной папки (словарь mtime) для следующей итерации.
    :param local_folder: путь к папке
    :param cloud_storage: объект облачного хранилища
    :param previous_local_state: словарь предыдущего состояния (может быть пустым при первом запуске)
    :return: новое состояние локальной папки (словарь mtime) для следующей итерации
    """
    current_local = get_local_files_info(local_folder) # получить текущее состояние локальной папки
    if not current_local and not os.path.exists(local_folder): # если папка не существует или недоступна
        logger.error(f"Синхронизация прервана: локальная папка {local_folder} недоступна") # логируем
        return previous_local_state # возвращаем неизменённое предыдущее состояние

    cloud_files = get_cloud_files_info(cloud_storage) # получить список файлов в облаке
    to_upload, to_delete = compare_files(current_local, previous_local_state, cloud_files) # cравнить и определить действия

    for filename in to_delete: # цикл по файлам, которые нужно удалить
        result = cloud_storage.delete(filename) # вызов метода удаления
        if not result: # если удаление не удалось (метод вернул False)
            logger.error(f"Не удалось удалить {filename} из облака")

    for filename in to_upload: # цикл по файлам для загрузки
        local_path = os.path.join(local_folder, filename) # полный путь
        if not os.path.exists(local_path): # если файл исчез
            logger.warning(f"Файл {filename} исчез перед загрузкой") # предупреждение (можно INFO)
            continue

        result = cloud_storage.reload(local_path) # для загрузки и перезаписи используем метод reload
        if not result: # если ошибка
            logger.error(f"Ошибка при загрузке {filename}") # дополнительное логирование

    if to_upload:
        logger.info(f"Загружено файлов: {len(to_upload)}")
    if to_delete:
        logger.info(f"Удалено из облака файлов: {len(to_delete)}")

    return current_local # возвращаем словарь с актуальными mtime

def initial_sync(local_folder: str, cloud_storage) -> dict:
    """
    Выполняет полную начальную синхронизацию: приводит облачное хранилище в соответствие с локальной папкой
    (удаляет лишние файлы из облака, загружает все локальные файлы). Используется при первом запуске
    :param local_folder: путь к папке
    :param cloud_storage: объект облачного хранилища
    :return: (dict) возвращаем состояние для последующих циклов
    """
    logger.info("Начало полной синхронизации") # запись в лог
    current_local = get_local_files_info(local_folder) # получаем локальные файлы
    cloud_files = get_cloud_files_info(cloud_storage) # облачные файлы

    files_to_delete = cloud_files - set(current_local.keys()) # определяем файлы, которые нужно удалить из облака (есть в облаке, но нет локально)

    for filename in files_to_delete: # цикл удаления
        cloud_storage.delete(filename) # вызов delete, логирование внутри

    for filename in current_local.keys(): # цикл по локальным файлам
        local_path = os.path.join(local_folder, filename) # полный путь
        cloud_storage.reload(local_path) # загружаем/перезаписываем

    logger.info("Полная синхронизация завершена")
    return current_local