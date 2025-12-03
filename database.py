2. database.py
```python
# database.py
import sqlite3
import json
from typing import List
from models import Turma, Professor, Disciplina, Sala, Feriado, Periodo, Aula

DBNAME = "escola.db"


def _conn():
    return sqlite3.connect(DBNAME)


# ------------------------------------------------------------------
def init_db():
    conn = _conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            serie TEXT,
            turno TEXT,
            tipo TEXT,
            disciplinas_turma TEXT,
            regras_neuro TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id TEXT PRIMARY KEY,
            nome TEXT,
            disciplinas TEXT,
            disponibilidade_dias TEXT,
            disponibilidade_horarios TEXT,
            restricoes TEXT,
            turmas_permitidas TEXT,
            dias_indisponiveis TEXT,
            horarios_indisponiveis TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            carga_semanal INTEGER,
            tipo TEXT,
            series TEXT,
            cor_fundo TEXT,
            cor_fonte TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            capacidade INTEGER,
            tipo TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS periodos (
            id TEXT PRIMARY KEY,
            nome TEXT,
            inicio TEXT,
            fim TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feriados (
            id TEXT PRIMARY KEY,
            data TEXT,
            motivo TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id TEXT PRIMARY KEY,
            turma TEXT,
            disciplina TEXT,
            professor TEXT,
            dia TEXT,
            horario INTEGER,
            sala TEXT
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------- TURMAS -------------------------------
def salvar_turmas(turmas: List[Turma]):
    conn = _conn(); cur = conn.cursor()
    cur.execute("DELETE FROM turmas")
    for t in turmas:
        cur.execute("""
            INSERT INTO turmas VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            t.id, t.nome, t.serie, t.turno, t.tipo,
            json.dumps(t.disciplinas_turma),
            json.dumps(t.regras_neuro)
        ))
    conn.commit(); conn.close()


def carregar_turmas() -> List[Turma]:
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM turmas")
    rows = cur.fetchall(); conn.close()
    return [
        Turma(
            nome=r[1], serie=r[2], turno=r[3], tipo=r[4],
            disciplinas_turma=json.loads(r[5]), regras_neuro=json.loads(r[6]), id=r[0]
        ) for r in rows
    ]


# -------------------------- PROFESSORES ----------------------------
def salvar_professores(profs: List[Professor]):
    conn = _conn(); cur = conn.cursor()
    cur.execute("DELETE FROM professores")
    for p in profs:
        cur.execute("""
            INSERT INTO professores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p.id, p.nome,
            json.dumps(p.disciplinas),
            json.dumps(list(p.disponibilidade_dias)),
            json.dumps(list(p.disponibilidade_horarios)),
            json.dumps(list(p.restricoes)),
            json.dumps(list(p.turmas_permitidas)),
            json.dumps(list(p.dias_indisponiveis)),
            json.dumps(list(p.horarios_indisponiveis)),
        ))
    conn.commit(); conn.close()


def carregar_professores() -> List[Professor]:
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM professores")
    rows = cur.fetchall(); conn.close()
    return [
        Professor(
            nome=r[1],
            disciplinas=json.loads(r[2]),
            disponibilidade_dias=set(json.loads(r[3])),
            disponibilidade_horarios=set(json.loads(r[4])),
            restricoes=set(json.loads(r[5])),
            turmas_permitidas=set(json.loads(r[6])),
            dias_indisponiveis=set(json.loads(r[7])),
            horarios_indisponiveis=set(json.loads(r[8])),
            id=r[0]
        ) for r in rows
    ]


# -------------------------- DISCIPLINAS ----------------------------
def salvar_disciplinas(discs: List[Disciplina]):
    conn = _conn(); cur = conn.cursor()
    cur.execute("DELETE FROM disciplinas")
    for d in discs:
        cur.execute("""
            INSERT INTO disciplinas VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            d.id, d.nome, d.carga_semanal, d.tipo,
            json.dumps(d.series), d.cor_fundo, d.cor_fonte
        ))
    conn.commit(); conn.close()


def carregar_disciplinas() -> List[Disciplina]:
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM disciplinas")
    rows = cur.fetchall(); conn.close()
    return [
        Disciplina(
            nome=r[1], carga_semanal=r[2], tipo=r[3],
            series=json.loads(r[4]), cor_fundo=r[5], cor_fonte=r[6], id=r[0]
        ) for r in rows
    ]


# ----------------------------- SALAS -------------------------------
def salvar_salas(salas: List[Sala]):
    conn = _conn(); cur = conn.cursor()
    cur.execute("DELETE FROM salas")
    for s in salas:
        cur.execute("INSERT INTO salas VALUES (?, ?, ?, ?)", (s.id, s.nome, s.capacidade, s.tipo))
    conn.commit(); conn.close()


def carregar_salas() -> List[Sala]:
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM salas")
    rows = cur.fetchall(); conn.close()
    return [Sala(nome=r[1], capacidade=r[2], tipo=r[3], id=r[0]) for r in rows]


# --------------------------- PERÍODOS ------------------------------
def salvar_periodos(periodos: List[dict]):
    conn = _conn(); cur = conn.cursor()
    cur.execute("DELETE FROM periodos")
    for p in periodos:
        cur.execute("INSERT INTO periodos VALUES (?, ?, ?, ?)", (p["id"], p["nome"], p["inicio"], p["fim"]))
    conn.commit(); conn.close()


def carregar_periodos() -> List[dict]:
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM periodos")
    rows = cur.fetchall(); conn.close()
    return [{"id": r[0], "nome": r[1], "inicio": r[2], "fim": r[3]} for r in rows]


# --------------------------- FERIADOS ------------------------------
def salvar_feriados(feriados: List[dict]):
    conn = _conn(); cur = conn.cursor()
    cur.execute("DELETE FROM feriados")
    for f in feriados:
        cur.execute("INSERT INTO feriados VALUES (?, ?, ?)", (f["id"], f["data"], f["motivo"]))
    conn.commit(); conn.close()


def carregar_feriados() -> List[dict]:
    conn = _conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM feriados")
    rows = cur.fetchall(); conn.close()
    return [{"id": r[0], "data": r[1], "motivo": r[2]} for r in rows]
```
