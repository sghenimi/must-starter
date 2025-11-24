from redis_apps.redis_db import r
###### simple set
# SADD: Add multiple members to a set
r.sadd("tags:python", "redis", "windows", "backend")

# SMEMBERS: Retrieve all unique members in the set
tags = r.smembers("tags:python")
print(tags)  # {b'redis', b'windows', b'backend'}

###### Sorted sets
# ZADD: Add members with scores
r.zadd("leaderboard", {"player1": 10, "player3": 30, "player4": 40, "player2": 20})

# ZRANGE: Retrieve members in ascending order of score
leaders = r.zrange("leaderboard", 0, -1, withscores=True)
print(leaders)
