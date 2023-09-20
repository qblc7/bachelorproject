
from flask import Flask
from flask_sse import sse

# initialise REST server with redis database and SSE endpoint /stream
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


# define endpoint to accept new events and publish them in the SSE endpoint
@app.route('/event/<action>')
def event(action):
    if action == "finished":
        sse.publish(data="finished", type="finished")
        return {}, 200
    else:
        sse.publish(data=action, type="robotdata")
        return {}, 200
