5. session_state.py
```python
# session_state.py
import streamlit as st
import database as db
from models import Turma, Professor, Disciplina, Sala


def init_session_state():
    db.init_db()

    # ---------- TURMAS ----------
    if "turmas" not in st.session_state:
        st.session_state.turmas = db.carregar_turmas() or [
            Turma("6anoA", "6ano", "manha"),
            Turma("7anoA", "7ano", "manha"),
            Turma("8anoA", "8ano", "manha"),
        ]

    # ---------- DISCIPLINAS ----------
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = db.carregar_disciplinas() or [
            Disciplina("Matemática", 5, "pesada", ["6ano", "7ano", "8ano"]),
            Disciplina("Português", 5, "pesada", ["6ano", "7ano", "8ano"]),
            Disciplina("História", 2, "media", ["6ano", "7ano", "8ano"]),
        ]

    # ---------- PROFESSORES ----------
    if "professores" not in st.session_state:
        st.session_state.professores = db.carregar_professores() or [
            Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Bruno", ["Português"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Carla", ["História"], {"seg", "ter", "qua", "qui", "sex"}),
        ]

    # ---------- SALAS ----------
    if "salas" not in st.session_state:
        st.session_state.salas = db.carregar_salas() or [
            Sala("Sala 1", 40),
            Sala("Sala 2", 40),
        ]

    # ---------- PERÍODOS & FERIADOS ----------
    if "periodos" not in st.session_state:
        st.session_state.periodos = db.carregar_periodos()

    if "feriados" not in st.session_state:
        st.session_state.feriados = db.carregar_feriados()
```
