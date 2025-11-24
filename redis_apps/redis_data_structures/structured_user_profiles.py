from redis_apps.redis_db import r

def create_user_profile(user_id, name, email):
    """
    Creates a user profile in Redis under the key 'user:{user_id}'.
    'name' and 'email' are stored as separate fields in the hash.
    """
    user_key = f"user:{user_id}"
    r.hset(user_key, mapping={"name": name, "email": email})

def get_user_profile(user_id):
    """
    Retrieves and returns all fields in the user profile hash
    as a Python dictionary. Keys and values are decoded from bytes.
    """
    user_key = f"user:{user_id}"
    profile_data = r.hgetall(user_key)
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in profile_data.items()}

def delete_user_profile(user_id):
    """
    Deletes the entire user profile key from Redis.
    """
    user_key = f"user:{user_id}"
    r.delete(user_key)

# Usage demonstration
create_user_profile(1002, "Bob", "bob@example.com")
print(get_user_profile(1002))  # e.g. {'name': 'Bob', 'email': 'bob@example.com'}
delete_user_profile(1002)