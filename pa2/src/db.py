import os
import json
import sqlite3

# From: https://goo.gl/YzypO
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance()


class DB(object):
    """
    DB driver for the To-Do app - deals with writing entities
    to the DB and reading entities from the DB 
    """

    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.create_user_table()

    def create_user_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE users (
                    ID INTEGER PRIMARY KEY,
                    NAME TEXT NOT NULL,
                    USERNAME TEXT NOT NULL,
                    BALANCE FLOAT NOT NULL
                );
            """)
        except Exception as e:
            print(e)

    def get_all_users(self):
        cursor = self.conn.execute("SELECT ID, NAME, USERNAME FROM users;")
        users = []
        for row in cursor:
            users.append({'id': row[0], 'name': row[1], 'username': row[2]})
        return users

    def create_user(self, name, username):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (name, username, balance) VALUES (?, ?, ?);', (name, username, 0))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM users WHERE ID == ?;', (id, ))
        for row in cursor:
            return {'id': row[0], 'name': row[1], 'username': row[2], 'balance': row[3]}
        return None
    
    def delete_user_by_id(self, id):
        cursor = self.conn.cursor()
        return_val = self.get_user_by_id(id)
        cursor.execute('DELETE FROM users WHERE ID == ?;', (id, ))
        return return_val
    
    def send_money(self, sender_id, receiver_id, amount):
        if (self.get_user_by_id(sender_id) != None and self.get_user_by_id(receiver_id) != None):
            sender_money = self.get_user_by_id(sender_id)['balance']
            if sender_money >= amount:
                receiver_money = self.get_user_by_id(receiver_id)['balance']
                sender_money = sender_money - amount
                receiver_money = receiver_money + amount
                cursor = self.conn.cursor()
                cursor.execute('UPDATE users SET balance=? WHERE ID == ?;', (sender_money, sender_id))
                cursor.execute('UPDATE users SET balance=? WHERE ID == ?;', (receiver_money, receiver_id))
                return True
        return False

