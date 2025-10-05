# app.py
import streamlit as st
from data_generator import gerar_disciplinas, gerar_turmas, gerar_professores
from scheduler_ortools import GradeHorariaORTools
from export import exportar_para_excel
import pandas as pd
import io

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")
st.markdown("Para Ensino Fundamental II e Ensino Médio — com base em neurociência educacional")

if st.button("🚀 Gerar Grade Horária"):
    with st.spinner("Gerando grade com Google OR-Tools... (até 30s)"):
        try:
            disciplinas = gerar_disciplinas()
            turmas = gerar_turmas()
            professores = gerar_professores(disciplinas)
            
            grade = GradeHorariaORTools(turmas, professores, disciplinas)
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
                file_name="grade_horaria.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            st.info("Verifique se há professores suficientes e com disponibilidade compatível.")
