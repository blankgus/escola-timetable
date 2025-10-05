# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session_state():
    try:
        # Inicializar banco
        database.init_db()
        
        # Carregar turmas
        if "turmas" not in st.session_state:
            try:
                turmas = database.carregar_turmas()
                if turmas is None:
                    turmas = []
                st.session_state.turmas = turmas or [
                    Turma("6anoA", "6ano", "manha"),
                    Turma("7anoA", "7ano", "manha"),
                    Turma("8anoA", "8ano", "manha"),
                    Turma("9anoA", "9ano", "manha"),
                    Turma("1emA", "1em", "manha"),
                    Turma("2emA", "2em", "manha"),
                    Turma("3emA", "3em", "manha"),
                ]
                logger.info(f"✅ Turmas carregadas: {len(st.session_state.turmas)}")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar turmas: {e}")
                st.session_state.turmas = [
                    Turma("6anoA", "6ano", "manha"),
                    Turma("7anoA", "7ano", "manha"),
                ]

        # Carregar professores
        if "professores" not in st.session_state:
            try:
                professores = database.carregar_professores()
                if professores is None:
                    professores = []
                st.session_state.professores = professores or [
                    Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
                    Professor("Bruno", ["Português"], {"seg", "ter", "qua", "qui", "sex"}),
                ]
                logger.info(f"✅ Professores carregados: {len(st.session_state.professores)}")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar professores: {e}")
                st.session_state.professores = [
                    Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
                ]

        # Carregar disciplinas
        if "disciplinas" not in st.session_state:
            try:
                disciplinas = database.carregar_disciplinas()
                if disciplinas is None:
                    disciplinas = []
                st.session_state.disciplinas = disciplinas or [
                    Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
                    Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
                ]
                logger.info(f"✅ Disciplinas carregadas: {len(st.session_state.disciplinas)}")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar disciplinas: {e}")
                st.session_state.disciplinas = [
                    Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]),
                ]

        # Carregar salas
        if "salas" not in st.session_state:
            try:
                salas = database.carregar_salas()
                if salas is None:
                    salas = []
                st.session_state.salas = salas or [
                    Sala("Sala 1", 30, "normal"),
                    Sala("Laboratório de Ciências", 25, "laboratório"),
                ]
                logger.info(f"✅ Salas carregadas: {len(st.session_state.salas)}")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar salas: {e}")
                st.session_state.salas = [
                    Sala("Sala 1", 30, "normal"),
                ]

        # Carregar períodos
        if "periodos" not in st.session_state:
            try:
                periodos = database.carregar_periodos()
                if periodos is None:
                    periodos = []
                st.session_state.periodos = periodos or [
                    {"nome": "1º Bimestre", "inicio": "2025-02-01", "fim": "2025-03-31"},
                    {"nome": "2º Bimestre", "inicio": "2025-04-01", "fim": "2025-05-31"},
                ]
                logger.info(f"✅ Períodos carregados: {len(st.session_state.periodos)}")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar períodos: {e}")
                st.session_state.periodos = [
                    {"nome": "1º Bimestre", "inicio": "2025-02-01", "fim": "2025-03-31"},
                ]

    except Exception as e:
        logger.error(f"❌ Erro geral na inicialização: {e}")
        # Fallback: dados mínimos
        st.session_state.turmas = [Turma("6anoA", "6ano", "manha")]
        st.session_state.professores = [Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"})]
        st.session_state.disciplinas = [Disciplina("Matemática", 4, "pesada", ["6ano"])]
        st.session_state.salas = [Sala("Sala 1", 30, "normal")]
        st.session_state.periodos = [{"nome": "1º Bimestre", "inicio": "2025-02-01", "fim": "2025-03-31"}]
