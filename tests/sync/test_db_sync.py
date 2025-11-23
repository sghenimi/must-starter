# test_db_manager_sync.py
import pytest
from app_fastapi_postgresql.main2 import CourseDBManager  # Assumes db_manager_sync.py exists

TEST_COURSE_DATA = [
    ('Test Course 1', 'Test Instructor A', 'Test Topic'),
    ('Test Course 2', 'Test Instructor B', 'Test Topic'),
]


def test_create_table_and_fetch_empty(db_manager: CourseDBManager):
    """Test table creation and ensure it's empty initially."""
    # Act
    db_manager.create_table()
    rows = db_manager.fetch_all_courses()

    # Assert
    assert rows is not None
    assert len(rows) == 0, "Table should be empty after creation."


def test_insert_courses_success(db_manager: CourseDBManager):
    """Test inserting data into the table."""
    # Arrange
    db_manager.create_table()

    # Act
    db_manager.insert_courses(TEST_COURSE_DATA)
    rows = db_manager.fetch_all_courses()

    # Assert
    assert len(rows) == len(TEST_COURSE_DATA), "Inserted and fetched row count mismatch."
    # Check that the inserted data is present
    course_names = {row[1] for row in rows}
    assert 'Test Course 1' in course_names
    assert 'Test Course 2' in course_names


def test_insert_duplicate_courses(db_manager: CourseDBManager):
    """Test that inserting duplicate unique rows is handled correctly (via ON CONFLICT DO NOTHING)."""
    # Arrange
    db_manager.create_table()
    # Data with a duplicate
    duplicate_data = TEST_COURSE_DATA + [('Test Course 1', 'Another Instructor', 'Another Topic')]

    # Act
    db_manager.insert_courses(duplicate_data)
    rows = db_manager.fetch_all_courses()

    # Assert: Should only have 2 unique rows
    assert len(rows) == 2, "Duplicate insertion should be ignored, resulting in only 2 rows."
    # Check that the original instructor is maintained (since it inserted first)
    assert rows[0][2] == 'Test Instructor A' or rows[1][2] == 'Test Instructor A'


def test_fetch_returns_correct_data_type(db_manager: CourseDBManager):
    """Test that fetch_all_courses returns a list of tuples (psycopg2 default)."""
    # Arrange
    db_manager.create_table()
    db_manager.insert_courses(TEST_COURSE_DATA)

    # Act
    rows = db_manager.fetch_all_courses()

    # Assert
    assert isinstance(rows, list)
    assert isinstance(rows[0], tuple)
    # Each row should have 4 elements (ID, Name, Instructor, Topic)
    assert len(rows[0]) == 4