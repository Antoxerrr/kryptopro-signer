import base64
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import win32com.client


@dataclass
class Certificate:

    store_index: int
    serial_number: str
    thumbprint: str
    subject_name: str
    valid_from_date: str
    valid_to_date: str

    actual: Any

    def __str__(self):
        return (
            f'SerialNumber: {self.serial_number}\n'
            f'SubjectName: {self.subject_name}\n'
            f'Thumbprint: {self.thumbprint}\n'
            f'ValidFrom: {self.valid_from_date}\n'
            f'ValidTo: {self.valid_to_date}\n'
        )


class CertificatesProvider:
    """Провайдер сертификатов."""

    def __init__(self):
        self._com_store = win32com.client.Dispatch('CAdESCOM.Store')
        self._store_args = (2, 'MY', 0)

    def get_list(self):
        self._com_store.Open(*self._store_args)
        result = [
            self._struct_from_certificate(
                self._com_store.Certificates.Item(i + 1), i + 1
            )
            for i in range(0, self._com_store.Certificates.Count)
        ]
        self._com_store.Close()
        return result

    def count(self):
        return len(self.get_list())

    def _struct_from_certificate(self, certificate, store_index):
        return Certificate(
            store_index=store_index,
            serial_number=certificate.SerialNumber,
            subject_name=certificate.SubjectName,
            thumbprint=certificate.Thumbprint,
            valid_from_date=certificate.ValidFromDate,
            valid_to_date=certificate.ValidToDate,
            actual=certificate
        )


def sign_data(data: str, certificate):
    to_sign = base64.b64encode(bytes(data, 'utf-8')).decode('utf-8')
    to_sign = ''.join(to_sign.splitlines())

    signer = win32com.client.Dispatch('CAdESCOM.CPSigner')
    signer.Certificate = certificate

    signing_time_attr = win32com.client.Dispatch('CAdESCOM.CPAttribute')
    signing_time_attr.Name = 0
    signing_time_attr.Value = datetime.now()
    signer.AuthenticatedAttributes2.Add(signing_time_attr)

    signed_data = win32com.client.Dispatch('CAdESCOM.CadesSignedData')
    signed_data.ContentEncoding = 1
    signed_data.Content = to_sign

    return signed_data.SignCades(signer, 1, False, 0)
