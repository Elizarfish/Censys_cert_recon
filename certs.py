import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="Domain to search certificates for")
args = parser.parse_args()

try:
    # Получение домена из аргументов командной строки
    domain = args.domain

    # Поиск сертификатов по домену и извлечение их хэшей
    print(f'Searching for certificates related to {domain}...')
    cmd = f'censys search "{domain}" --index-type certs --max-record 100 | jq -c \'.[] | {{"Certificateshash": ."parsed.fingerprint_sha256"}}\''
    cert_hashes = os.popen(cmd).read().splitlines()

    # Поиск доменов, связанных с каждым сертификатом, и сохранение их в файл
    print('Extracting domains from certificates...')
    for cert_hash in cert_hashes:
        cert_hash = json.loads(cert_hash)['Certificateshash']
        cmd = f'censys search "parsed.fingerprint_sha256: {cert_hash}" --index-type certs --max-record 100 --fields parsed.names,parsed.fingerprint_sha256parsed.fingerprint_sha256,parsed.subject_dn | jq -r \'.[] | .["parsed.names"][]\''
        domains = os.popen(cmd).read().splitlines()
        for domain in domains:
            if domain:
                with open('output.txt', 'a') as f:
                    f.write(f'{domain}\n')
                    print(f'Found domain: {domain}')

    print('Done.')

except KeyboardInterrupt:
    print('Скрипт остановлен по запросу пользователя')
