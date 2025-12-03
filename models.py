from dataclasses import dataclass, field
from typing import List, Set
import uuid

DIAS_SEMANA = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]


# ---------- ENTIDADES BÁSICAS ----------
@dataclass
class Disciplina:
    nome: str
    carga_semanal: int           # aulas/semana
    tipo: str                    # pesada | media | leve | pratica
    series: List[str]
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Professor:
    nome: str
    disciplinas: List[str]

    disponibilidade_dias: Set[str]            # {"seg", "ter"...}
    disponibilidade_horarios: Set[int] = field(default_factory=lambda: {1, 2, 3, 5, 6, 7})

    restricoes: Set[str] = field(default_factory=set)          # livre p/ uso futuro
    turmas_permitidas: Set[str] = field(default_factory=set)
    dias_indisponiveis: Set[str] = field(default_factory=set)
    horarios_indisponiveis: Set[int] = field(default_factory=set)

    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Turma:
    nome: str        # 8anoA
    serie: str       # 8ano
    turno: str       # manha | tarde
    tipo: str = "regular"
    disciplinas_turma: List[str] = field(default_factory=list)   # lista de nomes de disciplina
    regras_neuro: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Sala:
    nome: str
    capacidade: int
    tipo: str = "normal"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Feriado:
    data: str
    motivo: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Periodo:
    nome: str
    inicio: str
    fim: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Aula:
    turma: str
    disciplina: str
    professor: str
    dia: str
    horario: int
    sala: str = ""
