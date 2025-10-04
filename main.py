from data_generator import gerar_disciplinas, gerar_turmas, gerar_professores
from scheduler import GradeHoraria
from export import exportar_para_excel

def main():
    print("📚 Gerando ambiente escolar...")
    disciplinas = gerar_disciplinas()
    turmas = gerar_turmas()
    professores = gerar_professores(disciplinas)

    print(f"→ Turmas: {len(turmas)} | Professores: {len(professores)}")
    
    print("🧠 Gerando grade horária inteligente...")
    grade = GradeHoraria(turmas, professores, disciplinas)
    grade.gerar_grade()
    
    print("📤 Exportando para Excel...")
    exportar_para_excel(grade.solucao)
    print("✅ Concluído! Veja 'grade_horaria.xlsx'")

if __name__ == "__main__":
    main()
