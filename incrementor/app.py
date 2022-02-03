from redis import Redis
from flask import Flask, redirect
from flask_restful import Api, Resource
from os import environ as env

app = Flask(__name__)
api = Api(app)
rds = Redis(env.get("REDIS_SERVER"), env.get('REDIS_PORT'))

if not rds.exists('counter'):
    rds.set('counter', 0)
    
class CounterResource(Resource):

    def get(self):
        return int(rds.get('counter').decode('utf-8'))
    
class CounterIncrementResource(Resource):
    def get(self):
        return rds.incr('counter')

class ResetResource(Resource):
    def get(self):
        rds.set('counter', 0)
        return int(rds.get('counter').decode('utf-8'))



api.add_resource(CounterResource, "/counter")
api.add_resource(CounterIncrementResource, "/")
api.add_resource(ResetResource, "/reset")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)