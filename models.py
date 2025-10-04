from dataclasses import dataclass
from typing import List, Set

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str  # 'pesada', 'media', 'leve', 'pratica'
    series: List[str]

@dataclass
class Professor:
    nome: str
    disciplinas: List[str]
    disponibilidade: Set[str]  # ex: {'seg', 'ter', 'qua', 'qui', 'sex'}
    max_aulas_dia: int = 6

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str  # 'manha' ou 'tarde'

@dataclass
class Aula:
    turma: str
    disciplina: str
    professor: str
    dia: str
    horario: int
