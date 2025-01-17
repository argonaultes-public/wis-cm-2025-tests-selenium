from models.models import Base, Agent, Materiel
from sqlalchemy import create_engine

from sqlalchemy.orm import Session
from sqlalchemy import select

import pytest


class TestModels:

    def setup_method(self):
        self.engine = create_engine("sqlite://", echo=True)
        Base.metadata.create_all(self.engine)

    def test_create_db_sqlite(self):
        with Session(self.engine) as session:
            lampe = Materiel(nom='lampe', quantite=15)
            blouson = Materiel(nom='blouson', quantite=30)

            bobsponge = Agent(photo='/path/to/photo', prenom='bob', nom='sponge', emprunt_materiel=[blouson])

            session.add_all([lampe, blouson, bobsponge])
            session.commit()

        session = Session(self.engine)
        stmt = select(Agent).where(Agent.nom.in_(['sponge']))
        agents = session.scalars(stmt).fetchall()
        assert len(agents) == 1
        for agent in agents:
            materiels = agent.emprunt_materiel
            assert len(materiels) == 1
            assert materiels[0].nom == 'blouson'

    def test_manage_quantity(self):
        with pytest.raises(ValueError):
            with Session(self.engine) as session:
                lampe = Materiel(nom='lampe', quantite=2)

                bobsponge = Agent(photo='/path/to/photo', prenom='bob', nom='sponge', emprunt_materiel=[lampe])
                clarkkent = Agent(photo='/path/to/photo', prenom='clark', nom='kent', emprunt_materiel=[lampe])
                brucewayne = Agent(photo='/path/to/photo', prenom='bruce', nom='wayne', emprunt_materiel=[lampe])

                session.add_all([lampe, bobsponge, clarkkent, brucewayne])
                session.commit()
