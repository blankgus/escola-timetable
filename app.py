# app.py
import streamlit as st
from session_state import init_session_state
from models import Turma, Professor, Disciplina
from scheduler_ortools import GradeHorariaORTools
from export import exportar_para_excel
import pandas as pd
import io

# Inicializar estado da sessão
init_session_state()

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# Abas
aba1, aba2, aba3, aba4 = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas"])

# =================== ABA 1: INÍCIO (GERAR GRADE) ===================
with aba1:
    st.header("Gerar Grade Horária")
    st.write("Use os dados cadastrados nas abas ao lado para gerar sua grade.")
    
    if st.button("🚀 Gerar Grade com Dados Atuais"):
        with st.spinner("Gerando grade com Google OR-Tools..."):
            try:
                grade = GradeHorariaORTools(
                    st.session_state.turmas,
                    st.session_state.professores,
                    st.session_state.disciplinas
                )
                aulas = grade.resolver()
                
                # Preparar DataFrame
                dados = []
                for aula in aulas:
                    dados.append({
                        "Turma": aula.turma,
                        "Disciplina": aula.disciplina,
                        "Professor": aula.professor,
                        "Dia": aula.dia,
                        "Horário": aula.horario
                    })
                
                df = pd.DataFrame(dados)
                tabela = df.pivot_table(
                    index=["Turma", "Horário"],
                    columns="Dia",
                    values="Disciplina",
                    aggfunc=lambda x: x.iloc[0],
                    fill_value=""
                ).reindex(columns=["seg", "ter", "qua", "qui", "sex"], fill_value="")
                
                st.success("✅ Grade gerada com sucesso!")
                st.dataframe(tabela, use_container_width=True)
                
                # Download
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    tabela.to_excel(writer, sheet_name="Grade por Turma")
                    df.to_excel(writer, sheet_name="Dados Brutos", index=False)
                output.seek(0)
                
                st.download_button(
                    label="📥 Baixar Excel",
                    data=output,
                    file_name="grade_horaria_personalizada.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")

# =================== ABA 2: DISCIPLINAS ===================
with aba2:
    st.header("Gerenciar Disciplinas")
    
    # Formulário para adicionar
    with st.form("add_disciplina"):
        st.subheader("Adicionar Disciplina")
        nome_disc = st.text_input("Nome")
        carga = st.number_input("Carga Semanal", min_value=1, max_value=6, value=3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
        series_input = st.text_input("Séries (separadas por vírgula)", value="6ano,7ano,8ano,9ano,1em,2em,3em")
        series = [s.strip() for s in series_input.split(",") if s.strip()]
        
        if st.form_submit_button("➕ Adicionar"):
            if nome_disc and series:
                st.session_state.disciplinas.append(Disciplina(nome_disc, int(carga), tipo, series))
                st.success(f"Disciplina '{nome_disc}' adicionada!")
            else:
                st.error("Preencha todos os campos.")
    
    # Listar e editar
    st.subheader("Disciplinas Cadastradas")
    for i, disc in enumerate(st.session_state.disciplinas[:]):
        with st.expander(f"{disc.nome} (carga: {disc.carga_semanal})"):
            with st.form(f"edit_disc_{i}"):
                nome = st.text_input("Nome", disc.nome, key=f"nome_{i}")
                carga = st.number_input("Carga", min_value=1, max_value=6, value=disc.carga_semanal, key=f"carga_{i}")
                tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], index=["pesada", "media", "leve", "pratica"].index(disc.tipo), key=f"tipo_{i}")
                series_str = st.text_input("Séries", ", ".join(disc.series), key=f"series_{i}")
                series = [s.strip() for s in series_str.split(",") if s.strip()]
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.disciplinas[i] = Disciplina(nome, carga, tipo, series)
                    st.success("Atualizado!")
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.disciplinas.pop(i)
                    st.rerun()

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("Gerenciar Professores")
    
    # Formulário para adicionar
    with st.form("add_prof"):
        st.subheader("Adicionar Professor")
        nome_prof = st.text_input("Nome do Professor")
        disc_nomes = [d.nome for d in st.session_state.disciplinas]
        disc_selecionadas = st.multiselect("Disciplinas", disc_nomes)
        dias = ["seg", "ter", "qua", "qui", "sex"]
        disp_selecionada = st.multiselect("Disponibilidade", dias, default=dias)
        
        if st.form_submit_button("➕ Adicionar"):
            if nome_prof and disc_selecionadas:
                st.session_state.professores.append(Professor(nome_prof, disc_selecionadas, set(disp_selecionada)))
                st.success(f"Professor '{nome_prof}' adicionado!")
            else:
                st.error("Preencha nome e pelo menos uma disciplina.")
    
    # Listar e editar
    st.subheader("Professores Cadastrados")
    for i, prof in enumerate(st.session_state.professores[:]):
        with st.expander(f"{prof.nome}"):
            with st.form(f"edit_prof_{i}"):
                nome = st.text_input("Nome", prof.nome, key=f"p_nome_{i}")
                disc_nomes = [d.nome for d in st.session_state.disciplinas]
                disc_atual = st.multiselect("Disciplinas", disc_nomes, default=prof.disciplinas, key=f"p_disc_{i}")
                dias = ["seg", "ter", "qua", "qui", "sex"]
                disp_atual = st.multiselect("Disponibilidade", dias, default=list(prof.disponibilidade), key=f"p_disp_{i}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.professores[i] = Professor(nome, disc_atual, set(disp_atual))
                    st.success("Atualizado!")
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.professores.pop(i)
                    st.rerun()

# =================== ABA 4: TURMAS ===================
with aba4:
    st.header("Gerenciar Turmas")
    
    with st.form("add_turma"):
        st.subheader("Adicionar Turma")
        nome_turma = st.text_input("Nome da Turma (ex: 8anoA)")
        serie_turma = st.text_input("Série (ex: 8ano)")
        turno = st.selectbox("Turno", ["manha", "tarde"])
        
        if st.form_submit_button("➕ Adicionar"):
            if nome_turma and serie_turma:
                st.session_state.turmas.append(Turma(nome_turma, serie_turma, turno))
                st.success(f"Turma '{nome_turma}' adicionada!")
            else:
                st.error("Preencha nome e série.")
    
    st.subheader("Turmas Cadastradas")
    for i, turma in enumerate(st.session_state.turmas[:]):
        with st.expander(f"{turma.nome} ({turma.serie})"):
            with st.form(f"edit_turma_{i}"):
                nome = st.text_input("Nome", turma.nome, key=f"t_nome_{i}")
                serie = st.text_input("Série", turma.serie, key=f"t_serie_{i}")
                turno = st.selectbox("Turno", ["manha", "tarde"], index=["manha", "tarde"].index(turma.turno), key=f"t_turno_{i}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.turmas[i] = Turma(nome, serie, turno)
                    st.success("Atualizado!")
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.turmas.pop(i)
                    st.rerun()
