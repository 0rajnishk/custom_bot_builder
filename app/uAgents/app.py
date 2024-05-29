from flask import Flask,jsonify,request
from uagents.query import query
from uagents import Model
import json
from flask_cors import CORS
import asyncio

app = Flask(__name__)
CORS(app,origins='*')


agent_address = 'agent1qww3ju3h6kfcuqf54gkghvt2pqe8qp97a7nzm2vp8plfxflc0epzcjsv79t'


class AgentRequest(Model):
    recipe_name : str
    email: str
    allowed: str
    restricted: str

@app.route('/')
def home():
    return "Welcome to home page"


@app.route('/getinfo/<string:recipe_name>',methods=['Get'])
async def get_Info(recipe_name):
    response = await query(destination=agent_address,message=AgentRequest(recipe_name=recipe_name, email="0rajnishk@gmail.com", allowed="data science related stuffs", restricted="politics"))
    data = json.loads(response.decode_payload())
    print(data)
    print(data["nutritions"])
    return data


if __name__ == '__main__':
    app.run(port=8000,debug=True)
