import os
import json
import sqlite3
from datetime import datetime

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
        self.create_user_to_transaction_table()
        self.create_transaction_table()

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
    
    def create_user_to_transaction_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE conversion (
                    ID INTEGER PRIMARY KEY,
                    USER_ID INTEGER NOT NULL,
                    TRANSACTION_ID INT NOT NULL
                );
            """)
        except Exception as e:
            print(e)

    def create_transaction_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE transactions (
                    ID INTEGER PRIMARY KEY,
                    TIMESTAMP TEXT NOT NULL,
                    SENDER_ID INT NOT NULL,
                    RECEIVER_ID INT NOT NULL,
                    AMOUNT FLOAT NOT NULL,
                    MESSAGE TEXT NOT NULL,
                    ACCEPTED BOOLEAN
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

    def create_user(self, name, username, balance):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (name, username, balance) VALUES (?, ?, ?);', (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM users WHERE ID == ?;', (id, ))
        for row in cursor:
            return {'id': row[0], 'name': row[1], 'username': row[2], 'balance': row[3], 'transactions': self.get_transactions_by_user_id(id)}
        return None
    
    def delete_user_by_id(self, id):
        cursor = self.conn.cursor()
        return_val = self.get_user_by_id(id)
        cursor.execute('DELETE FROM users WHERE ID == ?;', (id, ))
        return return_val
    
    def get_transactions_by_user_id(self, id):
            cursor = self.conn.execute("SELECT TRANSACTION_ID FROM conversion WHERE USER_ID == ?;", (id, ))
            transactions = []
            for row in cursor:
                transactions.append(self.get_transaction_by_id(row[0]))
            return transactions
    
    def get_transaction_by_id(self, transaction_id):
        cursor = self.conn.execute('SELECT * FROM transactions WHERE ID == ?;', (transaction_id, ))
        for row in cursor:
            return {'id': row[0], 'timestamp': row[1], 'sender_id': row[2], 'receiver_id': row[3], 'amount': row[4], 'message': row[5], 'accepted': row[6]}
        return None

    def send_money(self, sender_id, receiver_id, amount, message):
        if (self.get_user_by_id(sender_id) != None and self.get_user_by_id(receiver_id) != None):
            sender_money = self.get_user_by_id(sender_id)['balance']
            if sender_money >= amount:
                receiver_money = self.get_user_by_id(receiver_id)['balance']
                sender_money = sender_money - amount
                receiver_money = receiver_money + amount
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                dt = datetime.fromtimestamp(timestamp)
                cursor = self.conn.cursor()
                cursor.execute('UPDATE users SET balance=? WHERE ID == ?;', (sender_money, sender_id))
                cursor.execute('UPDATE users SET balance=? WHERE ID == ?;', (receiver_money, receiver_id))
                cursor.execute('INSERT INTO transactions (timestamp, sender_id, receiver_id, amount, message, accepted) VALUES (?, ?, ?, ?, ?, ?);', (dt, sender_id, receiver_id, amount, message, True))
                transaction_id = cursor.lastrowid
                cursor.execute('INSERT INTO conversion (user_id, transaction_id) VALUES (?, ?);', (sender_id, transaction_id))
                cursor.execute('INSERT INTO conversion (user_id, transaction_id) VALUES (?, ?);', (receiver_id, transaction_id))
                self.conn.commit()
                return self.get_transaction_by_id(transaction_id)
        return None

    def request_money(self, sender_id, receiver_id, amount, message):
        if (self.get_user_by_id(sender_id) != None and self.get_user_by_id(receiver_id) != None):
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            dt = datetime.fromtimestamp(timestamp)
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO transactions (timestamp, sender_id, receiver_id, amount, message, accepted) VALUES (?, ?, ?, ?, ?, ?);', (dt, sender_id, receiver_id, amount, message, None))
            transaction_id = cursor.lastrowid
            cursor.execute('INSERT INTO conversion (user_id, transaction_id) VALUES (?, ?);', (sender_id, transaction_id))
            cursor.execute('INSERT INTO conversion (user_id, transaction_id) VALUES (?, ?);', (receiver_id, transaction_id))
            self.conn.commit()
            return self.get_transaction_by_id(transaction_id)
        return None

    def accept_payment(self, transaction_id):
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction is not None and transaction['accepted'] is None:
            sender = self.get_user_by_id(transaction['sender_id'])
            if sender['balance'] >= transaction['amount']:
                amount = transaction['amount']
                sender_money = sender['balance']
                receiver_money = self.get_user_by_id(transaction['receiver_id'])['balance']
                sender_money = sender_money - amount
                receiver_money = receiver_money + amount
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                dt = datetime.fromtimestamp(timestamp)
                cursor = self.conn.cursor()
                cursor.execute('UPDATE users SET balance=? WHERE ID == ?;', (sender_money, transaction['sender_id']))
                cursor.execute('UPDATE users SET balance=? WHERE ID == ?;', (receiver_money, transaction['receiver_id']))
                cursor.execute('UPDATE transactions SET accepted=? WHERE ID == ?;', (True, transaction_id))
                cursor.execute('UPDATE transactions SET timestamp=? WHERE ID == ?;', (dt, transaction_id))
                self.conn.commit()
                return self.get_transaction_by_id(transaction_id), True
            return self.get_transaction_by_id(transaction_id), False
        return None, None
    
    def reject_payment(self, transaction_id):
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction is not None and transaction['accepted'] is None:
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            dt = datetime.fromtimestamp(timestamp)
            cursor = self.conn.cursor()
            cursor.execute('UPDATE transactions SET accepted=? WHERE ID == ?;', (False, transaction_id))
            cursor.execute('UPDATE transactions SET timestamp=? WHERE ID == ?;', (dt, transaction_id))
            self.conn.commit()
            return self.get_transaction_by_id(transaction_id)
        return None

