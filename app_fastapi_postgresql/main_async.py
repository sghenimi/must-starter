import asyncio
from pathlib import Path
import asyncpg
from asyncpg.exceptions import DuplicateTableError, InvalidCatalogNameError
from typing import List, Tuple

# ## 1. Centralized Configuration (Asyncpg uses different keys) ##
DB_CONFIG = {
    "database": "mydb_01",
    "user": "Soufiane",
    "host": "localhost",
    "password": "postgres",
    "port": 5432,
    "min_size": 1,
    "max_size": 10,  # Recommended for a connection pool
}

COURSE_DATA: List[Tuple[str, str, str]] = [
    ('Introduction to SQL - 2', 'Izzy Weber', 'DataBase'),
    ('Analyzing Survey Data in Python - 2', 'EbunOluwa Andrew', 'Data'),
    ('Introduction to ChatGPT - 2', 'James Chapman', 'IA'),
    ('Introduction to Statistics in R - 2', 'Maggie Matsui', 'IA'),
    ('Hypothesis Testing in Python - 2', 'James Chapman', 'Testing'),
]


class AsyncCourseDBManager:
    """Manages database operations asynchronously using asyncpg connection pool."""

    def __init__(self, db_config):
        self.db_config = db_config
        self.pool = None

    async def initialize_pool(self):
        """Creates the asyncpg connection pool."""
        try:
            # Create a connection pool as an attribute
            self.pool = await asyncpg.create_pool(
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database'],
                host=self.db_config['host'],
                port=self.db_config['port'],
                min_size=self.db_config['min_size'],
                max_size=self.db_config['max_size']
            )
            print("# Async database pool initialized.")
        except InvalidCatalogNameError:
            print(f"# Error: Database '{self.db_config['database']}' does not exist.")
            # In a real app, you might try to create the database here.
            self.pool = None
        except Exception as e:
            print(f"# Database connection failed: {e}")
            self.pool = None

    async def close_pool(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            print("# Async database pool closed.")

    async def create_table(self):
        """Creates the datacamp_courses table asynchronously."""
        sql_create_table = """
            CREATE TABLE IF NOT EXISTS datacamp_courses(
                course_id SERIAL PRIMARY KEY,
                course_name VARCHAR (50) UNIQUE NOT NULL,
                course_instructor VARCHAR (100) NOT NULL,
                topic VARCHAR (20) NOT NULL
            );
        """
        if not self.pool: return

        # ##Use pool.acquire() as an async context manager##
        async with self.pool.acquire() as conn:
            try:
                # conn.execute is used for DDL commands
                await conn.execute(sql_create_table)
                print("# Table 'datacamp_courses' created successfully.")
            except DuplicateTableError:
                # Handled by IF NOT EXISTS, but kept for clarity
                print("# Table already exists.")
            except Exception as e:
                print(f"# Error creating table: {e}")

    async def insert_courses(self, data: List[Tuple[str, str, str]]):
        """Inserts multiple courses using bulk insertion."""
        sql_insert = """
            INSERT INTO datacamp_courses(course_name, course_instructor, topic)
            VALUES ($1, $2, $3)
            ON CONFLICT (course_name) DO NOTHING;
        """
        if not self.pool: return

        # ##Use copy_records_to_table for best performance (or execute_many)##
        async with self.pool.acquire() as conn:
            try:
                # `asyncpg` uses $1, $2, $3... for placeholders
                await conn.executemany(sql_insert, data)
                print(f"# Inserted/checked {len(data)} courses asynchronously.")
            except Exception as e:
                print(f"# Error inserting data: {e}")

    async def fetch_all_courses(self):
        """Fetches all rows asynchronously."""
        sql_select = 'SELECT * FROM datacamp_courses;'
        if not self.pool: return

        async with self.pool.acquire() as conn:
            try:
                # conn.fetch returns a list of asyncpg.Record objects
                rows = await conn.fetch(sql_select)
                print("\n## Fetched Courses (Async) ##")
                for row in rows:
                    print(tuple(row))  # Convert Record to tuple for printing
                return rows
            except Exception as e:
                print(f"# Error fetching data: {e}")
                return []


# ## Main Async Execution ##
async def main_async():
    # Original path logging
    _path = Path.home() / "Documents" / "script.py"
    print(f"Script Path: {_path}")
    print("#" * 50)

    # Initialize the async database manager
    db_manager = AsyncCourseDBManager(DB_CONFIG)

    # 1. Initialize the pool (must be awaited)
    await db_manager.initialize_pool()

    if db_manager.pool:
        # 2. Run operations
        await db_manager.create_table()
        await db_manager.insert_courses(COURSE_DATA)
        await db_manager.fetch_all_courses()

    # 3. Close the pool
    await db_manager.close_pool()

    print("#" * 50)


if __name__ == "__main__":
    # The entry point for running an async program
    asyncio.run(main_async())