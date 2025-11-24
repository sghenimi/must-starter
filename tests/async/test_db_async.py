# test_db_manager_async.py
import pytest
# Assurez-vous d'importer la classe du fichier
from app_fastapi_postgresql.main_async import AsyncCourseDBManager

TEST_COURSE_DATA = [
    ('Test Async Course 1', 'Async Instructor X', 'Async Topic A'),
    ('Test Async Course 2', 'Async Instructor Y', 'Async Topic B'),
]


# Les fonctions de test doivent être définies comme 'async def'
# si vous utilisez une version récente de pytest-asyncio.
@pytest.mark.asyncio
async def test_create_table_and_fetch_empty(db_manager: AsyncCourseDBManager):
    """Test de la création de table et vérifie qu'elle est vide."""
    # Act
    await db_manager.create_table()
    rows = await db_manager.fetch_all_courses()

    # Assert
    assert rows is not None
    assert len(rows) == 0, "La table devrait être vide après la création."

@pytest.mark.asyncio
async def test_insert_courses_success(db_manager: AsyncCourseDBManager):
    """Test de l'insertion et de la récupération des données."""
    # Arrange
    await db_manager.create_table()

    # Act
    await db_manager.insert_courses(TEST_COURSE_DATA)
    rows = await db_manager.fetch_all_courses()

    # Assert
    assert len(rows) == len(TEST_COURSE_DATA), "Le nombre de lignes insérées et récupérées est incorrect."

    # asyncpg.Record permet d'accéder aux colonnes comme dans un dictionnaire ou un tuple
    course_names = {row['course_name'] for row in rows}
    assert 'Test Async Course 1' in course_names
    assert 'Test Async Course 2' in course_names

@pytest.mark.asyncio
async def test_insert_duplicate_courses(db_manager: AsyncCourseDBManager):
    """Test la gestion des doublons (ON CONFLICT DO NOTHING)."""
    # Arrange
    await db_manager.create_table()
    # Données avec un doublon basé sur le nom du cours
    duplicate_data = TEST_COURSE_DATA + [
        ('Test Async Course 1', 'Autre Instructeur', 'Autre Sujet')
    ]

    # Act
    await db_manager.insert_courses(duplicate_data)
    rows = await db_manager.fetch_all_courses()

    # Assert: Seules 2 lignes uniques devraient être insérées
    assert len(rows) == 2, "L'insertion d'un doublon aurait dû être ignorée."

    # Vérifiez que le premier cours inséré a conservé son instructeur initial
    row_1 = next(row for row in rows if row['course_name'] == 'Test Async Course 1')
    assert row_1['course_instructor'] == 'Async Instructor X'