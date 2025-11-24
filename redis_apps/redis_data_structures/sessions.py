import redis
import uuid

r = redis.Redis(
    host='localhost',
    port=6379,
    db=0  # The default Redis database index
)

def store_user_session(user_id):
    """
    Generates a unique session token (UUID) for a user and stores it in Redis.
    The session is stored under the key pattern: user:{user_id}:session
    """
    session_key = f"user:{user_id}:session"
    token = str(uuid.uuid4())   # Generate a random UUID as a session token
    r.set(session_key, token)   # Store token in Redis
    return token

def get_user_session(user_id):
    """
    Retrieves the stored session token for the given user_id.
    Returns None if the session does not exist or is expired.
    """
    session_key = f"user:{user_id}:session"
    token = r.get(session_key)
    return token.decode('utf-8') if token else None

def delete_user_session(user_id):
    """
    Deletes the session entry from Redis for the specified user_id.
    """
    session_key = f"user:{user_id}:session"
    r.delete(session_key)

# Usage demonstration
session_token = store_user_session(1001)
print(f"Stored session token: {session_token}")

retrieved_token = get_user_session(1001)
print(f"Retrieved session token: {retrieved_token}")

delete_user_session(1001)
print(f"Session after delete: {get_user_session(1001)}")  # Should be None or empty