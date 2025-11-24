from redis_apps.redis_db import r
def enqueue_task(queue_name, task):
    """
    Appends a task to the end (right) of the Redis list named queue_name.
    """
    r.rpush(queue_name, task)

def dequeue_task(queue_name):
    """
    Removes a task from the front (left) of the Redis list named queue_name.
    Returns the task as a string, or None if the queue is empty.
    """
    task = r.lpop(queue_name)
    return task.decode('utf-8') if task else None

# Example usage:
enqueue_task("my_queue", "send_email")
enqueue_task("my_queue", "generate_report")

while True:
    task = dequeue_task("my_queue")
    if not task:
        print("No more tasks in queue.")
        break
    print(f"Processing task: {task}")