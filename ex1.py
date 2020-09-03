from flask import Flask, request
import redis
from rq import Queue

import time

app = Flask(__name__)

# Connecting to Redis
# Create a redis object
r = redis.Redis()

# Create a Queue
q = Queue(connection=r)

def background_task(n):

    delay = 2

    print("Task running")
    print(f"Simulation {delay} second delay")

    time.sleep(delay)

    print(len(n))
    print("Task complete")

@app.route("/task")
def add_task():
    if request.args.get("n"):
        
        job = q.enqueue(background_task,request.args.get("n"))

        q_len = len(q)

        return f"Task {job.id} added to queue {job.enqueued_at}. {q_len} tasks in the queue."

    return "No value for n"
    

if __name__ == "__main__":
    app.run(debug=True)

