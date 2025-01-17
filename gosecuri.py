from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import Base, Agent

import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    engine = create_engine(os.getenv('DB_URL'), echo=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    stmt = select(Agent)
    agents = session.scalars(stmt).fetchall()
    print("####################")
    print(agents)
    agents_response = map(lambda agent: f'<a href=\"/agent/{agent.agent_id}\">{agent.nom}</a>' , agents)
    print("------------------")
    result = '<br>'.join(list(agents_response))
    return f'<p>{result}</p>'

@app.route("/agent/<int:agent_id>")
def agent_details(agent_id):
    engine = create_engine(os.getenv('DB_URL'), echo=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    stmt = select(Agent).where(Agent.agent_id == agent_id)
    agent = session.scalars(stmt).first()
    return f"<p class=\"agent\">{agent}</p>"
