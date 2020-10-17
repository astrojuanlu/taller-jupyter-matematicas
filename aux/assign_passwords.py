import dbm
import bcrypt
import os

import pandas as pd


def read_users():
    df = pd.read_csv(os.environ["USER_DATA_PATH"])
    yield from df["Username"].dropna().unique().tolist()


def read_passwords():
    df = pd.read_csv(os.environ["PASSWORD_FILE_PATH"])
    yield from df["Password"].unique().tolist()


def set_password(db, username: str, password: str):
    db[username.encode()] = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def main():
    with open(os.environ["DBM_PATH"], "w") as db:
        for username, password in zip(read_users(), read_passwords()):
            print(username, password)
            # set_password(username, password)


if __name__ == "__main__":
    main()
