# models/__init__.py
from .db import db
from .Pessoa import Pessoa
from .Hospedes import Hospedes
from .Quarto import Quarto
from .Reserva import Reserva 
from .Acompanhante import Acompanhante
from .Consumo_frigobar import Consumo_frigobar

__all__ = ['db', 'Pessoa', 'Hospede', 'Quarto', 'Reserva', 'Acompanhante', 'Consumo_frigobar']
