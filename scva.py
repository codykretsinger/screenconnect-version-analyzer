import csv
import re
import requests
from requests.exceptions import Timeout, ConnectionError
import ipaddress

def is_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def check_version(ip, port):
    try:
        if not is_ipv4(ip):
            print(f"Skipping IPv6 address {ip}")
            return None
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        response = requests.head(f'http://{ip}:{port}', headers=headers, timeout=5)
        if response.status_code == 200:
            version_string = response.headers.get('Server', '').strip()  # Assuming the version number is in the Server header
            match = re.search(r'ScreenConnect/(\d+\.\d+\.\d+)', version_string)
            if match:
                version_number = match.group(1)
                if version_less_than_23_9_8(version_number):
                    return version_number
        return None
    except Timeout:
        return None
    except ConnectionError:
        # Do not print error message for aborted connections
        return None
    except Exception as e:
        print(f"Error occurred while checking version for {ip}:{port}: {e}")
        return None

def version_less_than_23_9_8(version):
    parts = version.split('.')
    parts = [int(part) for part in parts]
    return tuple(parts) < (23, 9, 8)

def main():
    csv_file = '/home/user/Desktop/cwsc_us_v1.csv'  # Change this to your CSV file path
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            ip, port = row
            version = check_version(ip, port)
            if version:
                print(f"Version less than 23.9.8 found at {ip}:{port} with version {version}")

if __name__ == "__main__":
    main()
