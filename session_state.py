# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina

def init_session_state():
    if "turmas" not in st.session_state:
        st.session_state.turmas = [
            Turma("6anoA", "6ano", "manha"),
            Turma("7anoA", "7ano", "manha"),
            Turma("8anoA", "8ano", "manha"),
            Turma("9anoA", "9ano", "manha"),
            Turma("1emA", "1em", "manha"),
            Turma("2emA", "2em", "manha"),
            Turma("3emA", "3em", "manha"),
        ]
    if "professores" not in st.session_state:
        st.session_state.professores = [
            Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Bruno", ["Português"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Carla", ["História", "Geografia"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Diego", ["Ciências", "Biologia"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Eliane", ["Inglês"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Fábio", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Gisele", ["Artes"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Hugo", ["Física", "Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Isabel", ["Química"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Jorge", ["Filosofia", "Sociologia"], {"seg", "ter", "qua", "qui", "sex"}),
        ]
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = [
            Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
            Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
            Disciplina("Ciências", 3, "media", ["6ano", "7ano", "8ano"]),
            Disciplina("Biologia", 3, "media", ["9ano", "1em", "2em", "3em"]),
            Disciplina("Física", 3, "pesada", ["2em", "3em"]),
            Disciplina("Química", 3, "pesada", ["9ano", "1em", "2em", "3em"]),
            Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
            Disciplina("Geografia", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em"]),
            Disciplina("Inglês", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
            Disciplina("Artes", 1, "leve", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
            Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
            Disciplina("Filosofia", 2, "leve", ["1em", "2em", "3em"]),
            Disciplina("Sociologia", 2, "leve", ["2em", "3em"]),
        ]
