from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from signer.core.api import GISMTApi, TokenRequestError, SignatureError
from signer.core.cert import CertificatesProvider
from signer.gui.generated.window import Ui_MainWindow
from signer.gui.utils import list_widget_items, remember_choice, \
    get_remembered_thumbprint


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Получение токена авторизации ГИС МТ')
        self._certs_provider = CertificatesProvider()
        self._certs = self._certs_provider.get_list()
        self._init_count_label()
        self._init_certs()
        self._init_actions()

    def _init_actions(self):
        self.search_cert_field.textChanged.connect(self._filter_list)
        self.select_button.clicked.connect(self._select_cert)
        self.copy_token_btn.clicked.connect(self._copy_token)

    def _init_certs(self):
        remembered_thumbprint = get_remembered_thumbprint()
        for cert in self._certs:
            item = QtWidgets.QListWidgetItem(str(cert))
            item.certificate = cert
            self.certs_list_widget.addItem(item)
            if cert.thumbprint == remembered_thumbprint:
                self.certs_list_widget.setCurrentItem(item)
                self.certs_list_widget.scrollToItem(item)
                self.saved_choice_found_label.setText(
                    'Автоматически выбран сохраненный сертификат'
                )

    def _init_count_label(self):
        count = self._certs_provider.count()
        self.certs_count_label.setText(f'Найдено сертификатов: {count}')

    def _filter_list(self):
        text = self.search_cert_field.text()
        for item in list_widget_items(self.certs_list_widget):
            item.setHidden(text not in item.text())

    def _copy_token(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.token_field.text())

    def _request_token(self, certificate):
        api = GISMTApi()
        try:
            token = api.request_token(certificate)
        except TokenRequestError as exc:
            text = f'Ошибка при запросе токена:\n\n{str(exc)}'
            self.request_error_label.setText(text)
        except SignatureError as exc:
            text = f'Ошибка создания подписи:\n\n{str(exc)}'
            self.request_error_label.setText(text)
        else:
            self.token_field.setText(token)

    def _select_cert(self):
        selected = self.certs_list_widget.currentItem()
        if not selected:
            self.request_error_label.setText('Не выбран сертификат')
        else:
            if self.remember_choice_checkbox.isChecked():
                remember_choice(selected.certificate.thumbprint)
            self._request_token(selected.certificate.actual)
