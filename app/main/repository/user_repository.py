import hashlib
import uuid


class UserRepository:

    def __init__(self, m_db):
        self.user_collection = m_db['users']

    def register(self, user_name, password):
        if self.user_collection.find({"username": user_name}).count() > 0:
            raise ValueError("User already exists")
        hashed_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.user_collection.insert_one({"username": user_name, "md_pass": hashed_pass})

    def check_user(self, user_name, password):
        users = self.user_collection.find({"username": user_name})
        if users.count() == 0:
            raise ValueError("User not found")

        hashed_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        if users[0]['md_pass'] != hashed_pass:
            raise ValueError("Invalid password")
        return True

    def check_token(self, token):
        users = self.user_collection.find({"token": token})
        if users.count() == 0:
            raise ValueError("Invalid token")
        else:
            return users[0]["username"]

    def login(self, username):
        token = uuid.uuid4()
        find_user = {"username": username}
        set_token = {"$set": {"token": str(token)}}

        self.user_collection.update_one(find_user, set_token)
        return token

    def logout(self, username):
        find_user = {"username": username}
        set_token = {"$set": {"token": None}}

        self.user_collection.update_one(find_user, set_token)
        return True
