import pymysql
from pymysql.cursors import DictCursor
from config import Config

class DatabaseConnector:
    """Singleton database connection manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def get_connection(self):
        """Get database connection"""
        try:
            if self.connection is None or not self.connection.open:
                self.connection = pymysql.connect(
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    cursorclass=DictCursor,
                    autocommit=True
                )
            return self.connection
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.open:
            self.connection.close()
            self.connection = None
    
    def __del__(self):
        self.close_connection()

db = DatabaseConnector()

def get_user_by_email(email):
    """Get user from database by email"""
    conn = db.get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def authenticate_user(email, password):
    """Authenticate user against database"""
    user = get_user_by_email(email) 
    if user and user['password'] == password: 
        return user
    return None