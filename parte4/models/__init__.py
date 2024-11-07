# models/__init__.py
from .db import db
from .Pessoa import Pessoa
from .Hospedes import Hospedes
from .Quarto import Quarto
from .Reserva import Reserva 
from .Acompanhante import Acompanhante

__all__ = ['db', 'Pessoa', 'Hospede', 'Quarto', 'Reserva', 'Acompanhante']
