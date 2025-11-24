import redis

# Instantiate a Redis client, connecting to localhost on port 6379
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0  # The default Redis database index
)
