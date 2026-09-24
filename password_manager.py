import json
import os
import time
import hashlib
import base64

try:
    from cryptography.fernet import Fernet
    
except ImportError:
    os.system('python -m pip install cryptography')
    os.system('clear')
    from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENC_FILE_PATH = os.path.join(BASE_DIR, 'passwords.enc')
MASTER_HASH_PATH = os.path.join(BASE_DIR, 'master.hash')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_key(password):
    hash_bytes = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes)

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_bytes, key):
    f = Fernet(key)
    return f.decrypt(encrypted_bytes).decode()
    
def master_password_check():

    if not os.path.exists(MASTER_HASH_PATH):
        print('First launch, create master password')
        master_password = input('Enter new master password: ~> ')
        confirm = input('Confirm master password: ~> ')

        if master_password != confirm:
            print('Password do not match. Exiting...')
            time.sleep(1.5)
            return None
        
        with open(MASTER_HASH_PATH, 'w') as f:
            f.write(hash_password(master_password))
        print("Master password created successfully!")
        time.sleep(1)
        return master_password

    with open(MASTER_HASH_PATH, 'r') as f:
        stored_hash = f.read().strip()

    for attempts in range(3):
        master_password = input('Enter master password: ~> ')
        if hash_password(master_password) == stored_hash:
            print("Access granted.")
            time.sleep(0.5)
            return master_password
            time.sleep(1.5)
            clear()
        else:
            print(f"Wrong password. {2 - attempts} attempts left.")
    
    print("Too many failed attempts. Exiting...")
    time.sleep(2)
    return None

def load_password(key):

    if not os.path.exists(ENC_FILE_PATH):
        return []

    with open(ENC_FILE_PATH, 'rb') as f:
        encrypted_data = f.read()
    
    try:
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    except Exception:
        print("Failed to decrypt. Wrong master password or corrupted file.")
        exit()

def save_password(passwords, key):
    data = json.dumps(passwords, indent=4)
    encrypted_data = encrypt_data(data, key)

    with open(ENC_FILE_PATH, 'wb') as f:
        f.write(encrypted_data)

def add_password(key):
    site = input('Enter name of site: ~> ')
    login = input('Enter login: ~> ')
    password = input('Enter password: ~> ')

    passwords = load_password(key)

    entry = {
        'site': site,
        'login': login,
        'password': password
    }

    passwords.append(entry)
    save_password(passwords, key)

    print()
    time.sleep(0.5)
    print('Entry data saved...')
    time.sleep(0.5)
    print()
    clear()

def show_password(key):

    passwords = load_password(key)
    if not passwords:
        print('You dont have any saved entry data')
        time.sleep(1)
        
    else:
        print('Saved entry data:')
        for i, entry in enumerate(passwords, start=1):
            print(f'{i}. {entry["site"]} | {entry["login"]} | {entry["password"]}')

    input('Press Enter to continue')
    clear()

def search_password(key):
    passwords = load_password(key)
    searching_site = input('Enter name of site for searching: ~> ')
    found = False
    for entry in passwords:
        if searching_site.lower() in entry["site"].lower():
            print(f'Found: {entry["site"]} | {entry["login"]} | {entry["password"]}')
            found = True

    if not found:
        print('No matching sites found')
    
    input('Press Enter to continue...')
    clear()

def delete_password(key):
    passwords = load_password(key)
    
    if not passwords:
        print('No data to delete.')
        input('Press Enter to continue')
        clear()
        return
    
    print('Entry data: ')
    for i, entry in enumerate(passwords, start=1):
        print(f'{i}. {entry["site"]} | {entry["login"]} | {entry["password"]}')

    try:
        deleting_password = int(input('Enter number of the entry data which you want delete: ~> '))
        
        if deleting_password < 1 or deleting_password > len(passwords):
            print(f'Error: number must be between 1 and {len(passwords)}')
            input('Press Enter to continue')
            clear()
            return

        print('Are you sure? [Y/N]')
        uschoice = input('~> ')

        if uschoice == 'Y' or uschoice == 'y':
            deleted = passwords.pop(deleting_password - 1)
            save_password(passwords, key)
            time.sleep(0.5)
            print(f'Entry data for {deleted["site"]} has been deleted')
            time.sleep(1)
            clear()
        else:
            print('Back to menu...')
            time.sleep(1)
            clear()

    except ValueError:
        print('Error: Please enter a valid number')
        time.sleep(1)
        clear()
    except Exception as e:
        print(f'Unexpected error: {e}')
        time.sleep(1)
        clear()
    
    input('Press Enter to continue')
    clear()

def clear():
    os.system('cls')

master_password = master_password_check()
if master_password is None:
    exit()
key = get_key(master_password)

while True:
    print('Password manager 1.0')
    time.sleep(0.5)
    print(f'0 - Exit'), time.sleep(0.2)
    print('1 - Add and save entry data'), time.sleep(0.2)
    print('2 - Show saved entry data'), time.sleep(0.2)
    print('3 - Search saved entry data'), time.sleep(0.2)
    print('4 - Delete saved entry data'), time.sleep(0.2)
    time.sleep(0.2)
    choice = input('~> ')

    if choice == '0':
        break

    elif choice == '1':
        clear()
        add_password(key)

    elif choice == '2':
        clear()
        show_password(key)

    elif choice == '3':
        clear()
        search_password(key)

    elif choice == '4':
        clear()
        delete_password(key)

    else:
        print()
        print('Error!')
        time.sleep(1)
        print()
        clear()
