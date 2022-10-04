import os
from os import environ

from PyQt5 import QtWidgets


SAVE_PATH = os.path.join(environ['APPDATA'], 'krypropro_signer')
SAVE_FILE_NAME = 'saved_thumbprint.txt'
SAVE_FILE_PATH = os.path.join(SAVE_PATH, SAVE_FILE_NAME)


def list_widget_items(list_widget: QtWidgets.QListWidget):
    count = list_widget.count()
    return [list_widget.item(idx) for idx in range(count)]


def remember_choice(thumbprint: str):
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    with open(SAVE_FILE_PATH, 'w') as file:
        file.write(thumbprint)


def get_remembered_thumbprint():
    if os.path.exists(SAVE_FILE_PATH):
        with open(SAVE_FILE_PATH, 'r') as file:
            return file.read()
