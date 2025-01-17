from typing import List
from sqlalchemy import String, Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from sqlalchemy.orm import mapped_column

from sqlalchemy import create_engine

from sqlalchemy.orm import validates

class Base(DeclarativeBase):
    pass


emprunte = Table(
    "emprunte",
    Base.metadata,
    Column("agent_id", ForeignKey("agent.agent_id")),
    Column("materiel_id", ForeignKey("materiel.materiel_id")),
)

class Materiel(Base):
    __tablename__ = 'materiel'

    materiel_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(35))
    quantite: Mapped[int]
    quantite_emprunte: Mapped[int] = mapped_column(Integer, default=0, insert_default=0)

    def __repr__(self):
        return f'{self.nom}: {self.quantite_emprunte} / {self.quantite}'

class Agent(Base):
    __tablename__ = 'agent'

    agent_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    photo: Mapped[str]
    nom: Mapped[str] = mapped_column(String(35))
    prenom: Mapped[str] = mapped_column(String(35))

    # children: Mapped[List[Child]] = relationship(secondary=association_table)
    emprunt_materiel: Mapped[List[Materiel]] = relationship(secondary=emprunte)

    @validates('emprunt_materiel')
    def validates_emprunt_materiel(self, key, materiel):
        print(f'####### {materiel}')
        if materiel.quantite <= 0:
            raise ValueError('Quantite insuffisante')
        if materiel.quantite_emprunte is None:
            materiel.quantite_emprunte = 1
        else:
            materiel.quantite_emprunte += 1
        if materiel.quantite_emprunte > materiel.quantite:
            raise ValueError('Quantite insuffisante')
        return materiel



if __name__ == '__main__':
    engine = create_engine("sqlite:///tst.db", echo=True)
    Base.metadata.create_all(engine)