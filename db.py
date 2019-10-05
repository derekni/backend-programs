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
        self.conn = sqlite3.connect('todo.db', check_same_thread=False)
        self.create_task_table()

    def create_task_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE task (
                    ID INTEGER PRIMARY KEY,
                    DESCRIPTION TEXT NOT NULL,
                    DONE BOOLEAN NOT NULL
                );
            """)
        except Exception as e:
            print(e)

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM task;")
        tasks = []
        for row in cursor:
            tasks.append({'id': row[0], 'description': row[1], 'done': row[2]})
        return tasks

    def insert_task(self, description, done):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO tasks (DESCRIPTION, DONE) VALUES (?, ?);', (description, done))
        self.conn.commit()
        return cursor.lastrowid

    def get_task_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM task WHERE ID == ?;', (id, ))
        for row in cursor:
            return {'id': row[0], 'description': row[1], 'done': row[2]}
        return None
