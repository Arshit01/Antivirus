import os
import hashlib
import time
import logging
import sqlite3

# Configure logging
logging.basicConfig(filename='file_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def monitor_filesystem():
    logging.info("Monitoring filesystem...")
    total_files = 0
    valid_files = 0
    scanned_files = set()
    for drive in get_all_drives():
        for root, dirs, files in os.walk(drive):
            for file in files:
                file_path = os.path.join(root, file)
                if is_valid_file(file_path):
                    total_files += 1
    while True:
        for drive in get_all_drives():
            for root, dirs, files in os.walk(drive):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in scanned_files:
                        if is_valid_file(file_path):
                            match_hash(file_path)
                            valid_files += 1
                            show_progress(valid_files, total_files)
                            scanned_files.add(file_path)
        time.sleep(3)  # Adjust the time interval for monitoring


def get_all_drives():
    drives = []
    for drive in range(ord('A'), ord('Z') + 1):
        drive = chr(drive) + ':\\'
        if os.path.exists(drive):
            drives.append(drive)
    return drives


def is_valid_file(file_path):
    # Check if the file extension is one of the known executable file types
    valid_extensions = {'.exe', '.dll', '.sys', '.bat', '.cmd', '.vbs', '.ps1', '.scr', '.ini', '.txt', '.sh', '.msi', '.pdf', '.zip', '.rar'}  # Add more file extensions if needed
    _, ext = os.path.splitext(file_path)
    return ext.lower() in valid_extensions


def match_hash(file_path):
    try:
        with open(u'\\\\?\\' + file_path, "rb") as f:
            sha256_hash = calculate_sha256(f)
            if hash_exists(sha256_hash):
                logging.info(f"Matching hash found for {file_path}: {sha256_hash}")
    except PermissionError as e:
        pass
    except FileNotFoundError as e:
        pass
    except Exception as e:
        pass


def calculate_sha256(file_handle):
    sha256_hash = hashlib.sha256()
    for byte_block in iter(lambda: file_handle.read(4096), b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def hash_exists(sha256_hash):
    conn = sqlite3.connect('hashes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM hashes WHERE sha256 = ?', (sha256_hash,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def show_progress(valid_files, total_files):
    if total_files == 0:
        progress = 0
    else:
        progress = (valid_files / total_files) * 100
    print(f"Progress: {progress:.2f}% ({valid_files}/{total_files} valid files scanned)")

if __name__ == '__main__':
    monitor_filesystem()
