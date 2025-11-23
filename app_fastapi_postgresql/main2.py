from pathlib import Path
import psycopg2
from psycopg2 import OperationalError
import sqlalchemy as db

# Centralized Configuration
DB_CONFIG = {
    "database": "mydb_01",
    "user": "Soufiane",
    "host": "localhost",
    "password": "postgres",
    "port": 5432,
}

# Data to be inserted
COURSE_DATA = [
    ('Introduction to SQL', 'Izzy Weber', 'Julia'),
    ('Analyzing Survey Data in Python', 'EbunOluwa Andrew', 'Python'),
    ('Introduction to ChatGPT', 'James Chapman', 'Theory'),
    ('Introduction to Statistics in R', 'Maggie Matsui', 'R'),
    ('Hypothesis Testing in Python', 'James Chapman', 'Python'),
]


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        # 2. Context Manager usage is preferred for connection management,
        # but for a function that *returns* the connection, we handle the `with`
        # in the calling methods (like CourseDBManager's methods).
        return psycopg2.connect(**DB_CONFIG)
    except OperationalError as e:
        print(f"# Database connection failed: {e}")
        return None


#  3. Encapsulation using a Class 
class CourseDBManager:
    """Manages database operations for the datacamp_courses table."""

    def __init__(self, db_config):
        self.db_config = db_config

    def _get_connection(self):
        """Helper to get a connection using the class's config."""
        return get_db_connection()

    def create_table(self):
        """Creates the datacamp_courses table if it doesn't exist."""
        sql_create_table = """
            CREATE TABLE IF NOT EXISTS datacamp_courses(
                course_id SERIAL PRIMARY KEY,
                course_name VARCHAR (50) UNIQUE NOT NULL,
                course_instructor VARCHAR (100) NOT NULL,
                topic VARCHAR (20) NOT NULL
            );
        """
        conn = self._get_connection()
        if conn:
            # 2. Use context manager for cursor
            with conn.cursor() as cur:
                try:
                    cur.execute(sql_create_table)
                    conn.commit()
                    print("# Table 'datacamp_courses' created successfully (or already exists).")
                except Exception as e:
                    print(f"# Error creating table: {e}")
                finally:
                    conn.close()

    def insert_courses(self, data):
        """Inserts multiple courses into the table using parameterized queries."""
        # 4. Use parameterized query for security and clarity
        sql_insert = """
            INSERT INTO datacamp_courses(course_name, course_instructor, topic)
            VALUES (%s, %s, %s)
            ON CONFLICT (course_name) DO NOTHING;
        """
        conn = self._get_connection()
        if conn:
            with conn.cursor() as cur:
                try:
                    # Use executemany for bulk insertion
                    cur.executemany(sql_insert, data)
                    conn.commit()
                    print(f"# Inserted {cur.rowcount} courses.")
                except Exception as e:
                    conn.rollback()
                    print(f"# Error inserting data: {e}")
                finally:
                    conn.close()

    def fetch_all_courses(self):
        """Fetches and prints all rows from the datacamp_courses table."""
        sql_select = 'SELECT * FROM datacamp_courses;'
        conn = self._get_connection()
        rows = []
        if conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(sql_select)
                    rows = cur.fetchall()
                    print(" Fetched Courses ")
                    for row in rows:
                        print(row)
                except Exception as e:
                    print(f"# Error fetching data: {e}")
                finally:
                    conn.close()
        return rows


#  5. ORM Operation (Kept separate and cleaner) 
def run_orm_query(db_config):
    """Executes a simple query using SQLAlchemy Core."""
    print("\n Running SQLAlchemy ORM Query ")

    # Construct a proper connection URL
    url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

    try:
        engine = db.create_engine(url)
        # 2. Use context manager for connection
        with engine.connect() as conn:
            output = conn.execute(db.text("SELECT * FROM datacamp_courses"))
            results = output.fetchall()
            print("# SQLAlchemy Results:")
            for row in results:
                print(row)
    except Exception as e:
        print(f"# Error running ORM query: {e}")


def main():
    # Original path logging (kept for reference)
    _path = Path.home() / "Documents" / "script.py"
    print(f"Script Path: {_path}")
    print("#" * 50)

    # Initialize the database manager
    db_manager = CourseDBManager(DB_CONFIG)

    # 1. Create the table
    db_manager.create_table()

    # 2. Insert data (only inserts if course_name is unique)
    db_manager.insert_courses(COURSE_DATA)

    # 3. Retrieve and print data
    db_manager.fetch_all_courses()

    # 4. Run ORM query
    run_orm_query(DB_CONFIG)

    print("#" * 50)


if __name__ == "__main__":
    main()
