# conftest.py
import pytest
import psycopg2
# Import the class and config from the file under test
from app_fastapi_postgresql.main2 import DB_CONFIG, CourseDBManager, get_db_connection


def cleanup_table(conn):
    """Drops the table to reset the state."""
    if conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS datacamp_courses;")
            conn.commit()


@pytest.fixture(scope="function")
def db_manager():
    """
    Fixture that initializes and cleans up the CourseDBManager instance.
    """
    # 1. SETUP: Get a temporary connection for cleanup
    conn_setup = get_db_connection()
    if conn_setup is None:
        pytest.skip("Could not connect to database. Skipping DB tests.")
        return

    # 2. SETUP: Ensure a clean table state before test runs
    cleanup_table(conn_setup)
    conn_setup.close()

    # 3. SETUP: Initialize the Manager instance that will be used by tests
    manager = CourseDBManager(DB_CONFIG)

    # 4. YIELD: Provide the manager instance to the test function
    yield manager

    # 5. TEARDOWN: Get a new connection to clean up after the test
    conn_teardown = get_db_connection()
    if conn_teardown:
        cleanup_table(conn_teardown)
        conn_teardown.close()