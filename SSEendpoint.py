
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

# how to run the app from terminal:
# docker run --name redis-sse -p 6379:6379 -d redis (to stop container: docker stop <container id> oder <container name>)
# nächstes mal: docker start <container name>
# gunicorn SSEendpoint:app --worker-class gevent --bind 127.0.0.1:5000

# how to run docker robot simulation:
# docker run --rm -it universalrobots/ursim_e-series

# distance similarity measure: discrete frechet distance --> libraries: similaritymeasures
