import json
from datetime import datetime
from typing import List


class Validity:
    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        self.start_date = start_date
        self.end_date = end_date


class CertificateElement:
    def __init__(self, certificate_data: str, issuer: str, subject: str, validity: Validity) -> None:
        self.certificate_data = certificate_data
        self.issuer = issuer
        self.subject = subject
        self.validity = validity


class Certificate:
    def __init__(self, message_type: str, certificates: List[CertificateElement]) -> None:
        self.message_type = message_type
        self.certificates = certificates


def load_certificate(json_data: dict) -> Certificate:
    try:
        certificate_objects = []
        for certificate in json_data['certificates']:
            start_date = datetime.strptime(certificate['validity']['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(certificate['validity']['end_date'], '%Y-%m-%d')
            validity = Validity(start_date, end_date)
            certificate_obj = CertificateElement(certificate['certificate_data'], certificate['issuer'], certificate['subject'], validity)
            certificate_objects.append(certificate_obj)

        certificate = Certificate(json_data['message_type'], certificate_objects)
        return certificate
    except KeyError as e:
        print('必要なキーが見つかりません')
        print(f'キーが見つからなかった要素: {e}')
        return None
    except ValueError as e:
        print('値の変換エラーが発生しました')
        print(f'変換エラーが発生した要素: {e}')
        return None
    except Exception as e:
        print(f'エラーが発生しました: {e}')
        return None

def print_certificate_data(certificate: Certificate) -> None:
    print("print_certificate_data")
    try:
        certificates = certificate.certificates
        for cert in certificates:
            print(cert.certificate_data)
            print(cert.issuer)
            print(cert.subject)
            print(cert.validity.start_date)
            print(cert.validity.end_date)
    except Exception as e:
        print(f'エラーが発生しました: {e}')
        return


"""-------------------------------"""


def load_json_from_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError as e:
        print(f'ファイルが見つかりません: {e}')
        return {}
    except json.JSONDecodeError:
        print(f'JSONデータの解析エラー: {e}')
        return {}
    except Exception as e:
        print(f'エラーが発生しました: {e}')
        return {}
    
"""-------------------------------"""
# スクリプトが直接実行された場合にのみ実行されるコード
if __name__ == '__main__':
    # ここから必要な処理を記述する

    file_path = "D:/Learnning/Python/JSON/test.json"
    print(file_path)
    json_data = load_json_from_file(file_path)
    certificate = load_certificate(json_data)
    #print_certificate_data(certificate)
