from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
key = Fernet.generate_key()
f = Fernet(key)

# Get input from the user
message = input("Enter a message to encrypt: ")

# Encrypt the message
encrypted_message = f.encrypt(message.encode())
print("Encrypted message:", encrypted_message)

# Decrypt the message
decrypted_message = f.decrypt(encrypted_message).decode()
print("Decrypted message:", decrypted_message)