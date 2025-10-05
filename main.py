# main.py
from data_generator import gerar_disciplinas, gerar_turmas, gerar_professores
from scheduler_ortools import GradeHorariaORTools
from export import exportar_para_excel

def main():
    print("📚 Gerando ambiente escolar...")
    disciplinas = gerar_disciplinas()
    turmas = gerar_turmas()
    professores = gerar_professores(disciplinas)

    print(f"→ Turmas: {len(turmas)} | Professores: {len(professores)}")
    
    print("🧠 Gerando grade horária com Google OR-Tools...")
    grade = GradeHorariaORTools(turmas, professores, disciplinas)
    aulas = grade.resolver()
    
    print("📤 Exportando para Excel...")
    exportar_para_excel(aulas)
    print("✅ Concluído! Veja 'grade_horaria.xlsx'")

if __name__ == "__main__":
    main()
