import bcrypt

users = {
    "luiz": "luiz2601*",
    "alisson": "alisson2833*",
    "barbara": "barbara6782*"
}

for user, password in users.items():
    password_bytes = password.encode('utf-8')
    # Usando rounds=12 conforme solicitado
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    print(f"{user}: {hashed.decode('utf-8')}")
