import requests
import logging
import os

logger = logging.getLogger("sync_logger") # получаем уже настроенный логгер

class CloudStorage:
    def __init__(self, token: str, cloud_folder: str) -> None:
        """
        Конструктор принимает токен доступа и имя папки в облаке
        :param token (str):  токен от Яндекс.Диска для доступа к API
        :param cloud_folder (str): имя папки в облаке
        """
        self.token = token # сохраняем токен как атрибут
        self.cloud_folder = cloud_folder # сохраняем облачную папку как атрибут
        self.base_url = "https://cloud-api.yandex.net/v1/disk" # базовый URL для API Яндекс.Диска
        self.headers = {"Authorization": f"OAuth {self.token}"} # заголовок авторизации для всех запросов
        logger.info(f"Инициализировано облачное хранилище. Папка: {cloud_folder}") # запись в лог успешной инициализации

    def _request(self, method: str, url: str, params = None, json = None, files = None) -> requests.Response | None:
        """
        Внутренний приватный метод для унификации запросов. Принимает HTTP-метод, полный URL (или путь), параметры запроса и т.д
        :param method (str): HTTP-метод
        :param url (str): полный URL
        :return:
        """
        try:
            response = requests.request(method, url, headers = self.headers, params = params, json = json, files = files,
                                        timeout = 30) # выполнение запроса с таймаутом
            response.raise_for_status() # если статус-код 4хх или 5хх, вызовет исключение
            return response # если все успешно, возвращает объект ответа
        except requests.exceptions.RequestException as e: # перехват любых ошибок сети, таймаутов, некорректных статусов
            logger.error(f"Ошибка HTTP-запроса {method} {url}: {e}") # запись в лог с уровнем ERROR
            return None

    def load(self, local_path: str) -> bool:
        """
        Загрузка нового файла облачное хранилище
        :param local_path: путь к локальному файлу
        :return: (bool) True если файл загружен, False если ошибка
        """
        filename = os.path.basename(local_path) # извлекаем имя файла

        try:
            with open(local_path, "rb") as file: # открываем файл в бинарном режиме
                file_data = file.read() # читаем содержимое
        except (FileNotFoundError, PermissionError) as e: # если файл не найден или нет доступа
            logger.error(f"Не удалось прочитать локальный файл {local_path}: {e}")
            return False # индикатор неудачи

        upload_url = f"{self.base_url}/resources/upload" # URL для получения ссылки на загрузку
        params = {"path": f"disk:/{self.cloud_folder}/{filename}", "overwrite": True} # параметры: путь и разрешение перезаписи

        response = self._request("GET", upload_url, params = params) # получаем ссылку для загрузки
        if response is None: # если запрос не удался
            return False

        href = response.json().get("href") # извлекаем URL для PUT-запроса
        if not href: # если ссылка отсутствует
            logger.error("Не получена ссылка для загрузки файла")
            return False

        put_response = requests.put(href, data = file_data, headers = {"Content-Type": "application/octet-stream"}) # загружаем файл
        if put_response.status_code in (200, 201): # успех
            logger.info(f"Файл {filename} успешно загружен в облако")
            return True
        else: # ошибка при загрузке
            logger.error(f"Ошибка загрузки {filename}: {put_response.status_code}")
            return False

    def reload(self, local_path: str) -> bool:
        """
        По ТЗ перезаписывает файл. Для Яндекс.Диска логика полностью совпадает с load, так как параметр overwrite = True уже задан.
        :param local_path: путь к локальному файлу
        :return:
        """
        return self.load(local_path) # просто вызываем load

    def delete(self, filename: str) -> bool:
        """
        Удаляет файл из облака
        :param filename: (str) принимает имя файла (не полный путь)
        :return: (bool) True если файл удален, False если ошибка
        """
        url = f"{self.base_url}/resources" # URL для удаления
        params = {"path": f"disk:/{self.cloud_folder}/{filename}", "permanently": True} # удаляем без корзины

        response = self._request("DELETE", url, params = params) # выполняем DELETE-запрос
        if response is None: # ошибка
            logger.error(f"Не удалось удалить {filename} из облака")
            return False

        if response.status_code == 204: # успешное удаление
            logger.info(f"Файл {filename} удалён из облака")
            return True
        else: # неожиданный статус
            logger.error(f"Ошибка удаления {filename}: {response.status_code}")
            return False

    def get_info(self) -> list:
        """
        Возвращает информацию о файлах в облачной папке
        :return: (list) список файлов
        """
        url = f"{self.base_url}/resources" # URL
        params = {"path": f"disk:/{self.cloud_folder}", "limit": 100, "fields": "items.name"} # запрашиваем только имена файлов

        response = self._request("GET", url, params = params)
        if response is None: # ошибка
            logger.error("Не удалось получить список файлов из облака")
            return [] # возвращаем пустой список (программа продолжит работу)

        data = response.json() # разбираем JSON
        items = data.get("_embedded", {}).get("items", []) # извлекаем список элементов
        file_names = [item["name"] for item in items if item["type"] == "file"] # оставляем только файлы

        logger.info(f"Получено {len(file_names)} файлов из облака")
        return file_names # возвращаем список имён