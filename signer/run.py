import sys
from pathlib import Path


def include_pycades():
    path = Path(__file__).resolve().parent
    pycades_build_path = path / 'pycades-build'
    sys.path.append(str(pycades_build_path))


include_pycades()
import pycades

store = pycades.Store()
store.Open(
    pycades.CADESCOM_CONTAINER_STORE,
    pycades.CAPICOM_MY_STORE,
    pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
)
certs = store.Certificates

if certs.Count != 0:
    print('Есть какие-то сертификаты\n')
    print(certs)
else:
    print('Сертификаты не найдены')
