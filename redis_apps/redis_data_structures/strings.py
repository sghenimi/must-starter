# 1. SET command: store a string under 'mykey'
r.set("mykey12345", "My value 12345")

# 2. GET command: retrieve the value stored at 'mykey'
value = r.get("mykey12345")
print(value)   # Output is b'hello from Windows', since redis-py returns bytes.

# 3. Convert bytes to string
print(value.decode())  # prints "hello from Windows"

# 4. DEL command: remove 'mykey' from Redis
res = r.delete("mykey12345")
print(res)