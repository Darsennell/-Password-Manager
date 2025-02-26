from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

def store_password(service, password, key):
    encrypted_password = encrypt_password(password, key)
    with open("passwords.txt", "a") as f:
        f.write(f"{service}: {encrypted_password.decode()}\n")

def retrieve_password(service, key):
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            if service in line:
                encrypted_password = line.split(": ")[1].strip()
                decrypted_password = decrypt_password(encrypted_password.encode(), key)
                return decrypted_password
    return None

def main():
    if not os.path.exists("secret.key"):
        key = generate_key()
        save_key(key)
    else:
        key = load_key()

    while True:
        print("\nOptions:")
        print("1. Store Password")
        print("2. Retrieve Password")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            service = input("Enter service name (e.g., Gmail, Facebook): ")
            password = input("Enter password: ")
            store_password(service, password, key)
        elif choice == '2':
            service = input("Enter service name to retrieve password: ")
            password = retrieve_password(service, key)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("Service not found.")
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
