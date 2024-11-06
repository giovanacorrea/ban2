# models/__init__.py
from .db import db
from .Pessoa import Pessoa
from .Hospedes import Hospedes
from .Quarto import Quarto

__all__ = ['db', 'Pessoa', 'Hospede', 'Quarto']
