# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina

def init_session_state():
    if "turmas" not in st.session_state:
        st.session_state.turmas = [
            Turma("8anoA", "8ano", "manha"),
            Turma("1emA", "1em", "manha"),
        ]
    if "professores" not in st.session_state:
        st.session_state.professores = [
            Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Bruno", ["Português"], {"seg", "ter", "qua", "qui", "sex"}),
        ]
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = [
            Disciplina("Matemática", 4, "pesada", ["8ano", "1em"]),
            Disciplina("Português", 4, "pesada", ["8ano", "1em"]),
            Disciplina("História", 2, "media", ["8ano", "1em"]),
            Disciplina("Educação Física", 2, "pratica", ["8ano", "1em"]),
        ]
