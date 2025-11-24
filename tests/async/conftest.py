# conftest.py
import pytest
import asyncpg
from app_fastapi_postgresql.main_async import DB_CONFIG, AsyncCourseDBManager


@pytest.fixture(scope="function")
async def db_pool():
    """
    Fixture de session pour créer un pool de connexions à la BD.
    Le pool est créé une seule fois et partagé par tous les tests.
    """
    try:
        # asyncpg utilise create_pool()
        pool = await asyncpg.create_pool(**DB_CONFIG)
    except Exception as e:
        pytest.skip(f"Impossible de se connecter à la base de données: {e}", allow_module_level=True)
        return

    yield pool

    # Nettoyage après la session de test
    await pool.close()


async def cleanup_table(pool):
    """Fonction asynchrone pour supprimer la table de test."""
    sql_drop = "DROP TABLE IF EXISTS datacamp_courses;"
    async with pool.acquire() as conn:
        await conn.execute(sql_drop)


@pytest.fixture
async def db_manager(db_pool):
    """
    Fixture pour initialiser et nettoyer l'AsyncCourseDBManager.
    S'exécute pour chaque fonction de test.
    """
    # 1. SETUP: Nettoyage de la table avant le test
    await cleanup_table(db_pool)

    # 2. INITIALISATION: Crée l'instance du Manager
    manager = AsyncCourseDBManager(db_pool)

    # 3. YIELD: Fournit l'instance à la fonction de test
    yield manager

    # 4. TEARDOWN: Nettoyage de la table après le test
    await cleanup_table(db_pool)