import logging
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    def __init__(self, name: str, user: str, password: str, host: str = 'localhost', port: int = 5432):
        self.conn_params = {
            'dbname': name,
            'user': user,
            'password': password,
            'host': host,
            'port': port,
        }
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cur = self.conn.cursor()
            logging.info('Connected to PostgreSQL')
        except Exception as e:
            logging.error(f'Failed to connect to PostgreSQL {e}')
            raise ConnectionError(f'Failed to connect to PostgreSQL {e}')

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logging.info('Disconnected from PostgreSQL')

    def init_db(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    text VARCHAR(1024) NOT NULL,
                    username VARCHAR(100) NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                )
            """)
            self.conn.commit()
        except Exception as e:
            logging.error(e)
            self.conn.rollback()

    def add_message(self, text: str, username: str, time: datetime = datetime.now()):
        try:
            self.cur.execute("""
            INSERT INTO messages (text, username, time) VALUES (%s, %s, %s)
            """, (text, username, time))
            self.conn.commit()
            logging.info(f'Added message {text} from {username} at {time}')
        except Exception as e:
            logging.error(e)
            self.conn.rollback()

    def get_messages(self):
        try:
            self.cur.execute("""
            SELECT * FROM messages
            """)
            return self.cur.fetchall()
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    db = DatabaseManager(name=os.getenv('PG_DB_NAME'), user=os.getenv('PG_ADMIN'), password=os.getenv('PG_ADMIN_PASS'))
    db.connect()
    db.init_db()
    db.close()
