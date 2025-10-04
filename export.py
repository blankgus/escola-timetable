import pandas as pd

def exportar_para_excel(aulas, caminho="grade_horaria.xlsx"):
    df = pd.DataFrame([
        {
            "Turma": a.turma,
            "Disciplina": a.disciplina,
            "Professor": a.professor,
            "Dia": a.dia,
            "Horário": a.horario
        }
        for a in aulas
    ])

    tabela = df.pivot_table(
        index=["Turma", "Horário"],
        columns="Dia",
        values="Disciplina",
        aggfunc=lambda x: x.iloc[0],
        fill_value=""
    ).reindex(columns=["seg", "ter", "qua", "qui", "sex"], fill_value="")

    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        tabela.to_excel(writer, sheet_name="Grade por Turma")
        df.to_excel(writer, sheet_name="Dados Brutos", index=False)
