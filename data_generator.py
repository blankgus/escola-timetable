# data_generator.py
from models import Turma, Professor, Disciplina
import random

def gerar_disciplinas():
    ef2 = [
        Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"]),  # ⚠️ Reduzido para 4
        Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"]),  # ⚠️ Reduzido para 4
        Disciplina("Ciências", 3, "media", ["6ano", "7ano"]),
        Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Geografia", 3, "media", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Inglês", 3, "media", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Artes", 1, "leve", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"]),
    ]
    em = [
        Disciplina("Português", 4, "pesada", ["1em", "2em", "3em"]),  # ⚠️ Reduzido para 4
        Disciplina("Matemática", 4, "pesada", ["1em", "2em", "3em"]),  # ⚠️ Reduzido para 4
        Disciplina("Biologia", 3, "media", ["1em", "2em", "3em"]),
        Disciplina("Física", 3, "pesada", ["2em", "3em"]),
        Disciplina("Química", 3, "pesada", ["1em", "2em", "3em"]),
        Disciplina("História", 3, "media", ["1em", "2em", "3em"]),
        Disciplina("Geografia", 2, "media", ["1em"]),
        Disciplina("Filosofia", 2, "leve", ["1em", "2em", "3em"]),
        Disciplina("Sociologia", 2, "leve", ["2em", "3em"]),
        Disciplina("Inglês", 3, "media", ["1em", "2em", "3em"]),
        Disciplina("Artes", 1, "leve", ["1em", "2em", "3em"]),
        Disciplina("Educação Física", 2, "pratica", ["1em", "2em", "3em"]),
    ]
    todas = ef2 + em
    return {d.nome: d for d in todas}

def gerar_turmas():
    turmas = []
    series = ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"]
    for serie in series:
        for letra in ["A", "B"]:
            turmas.append(Turma(f"{serie}{letra}", serie, "manha"))
    return turmas

def gerar_professores(disciplinas_dict):
    nomes_base = ["Ana", "Bruno", "Carla", "Diego", "Eliane", "Fábio", "Gisele", "Hugo", "Isabel", "Jorge",
                  "Lúcia", "Marcelo", "Natália", "Otávio", "Paula", "Ricardo", "Sofia", "Thiago", "Vanessa", "Yuri"]
    random.seed(42)
    random.shuffle(nomes_base)
    
    # Aumentado número de professores nas disciplinas críticas
    disc_por_prof = {
        "Português": 4,
        "Matemática": 4,
        "Ciências": 3,
        "Biologia": 3,
        "Física": 3,
        "Química": 3,
        "História": 3,
        "Geografia": 3,
        "Inglês": 3,
        "Artes": 2,
        "Educação Física": 2,
        "Filosofia": 2,
        "Sociologia": 2,
    }

    professores = []
    idx = 0
    dias = ["seg", "ter", "qua", "qui", "sex"]

    for disc, qtd in disc_por_prof.items():
        carga = disciplinas_dict[disc].carga_semanal
        for i in range(qtd):
            nome = nomes_base[idx % len(nomes_base)]
            if idx >= len(nomes_base):
                nome += str(idx // len(nomes_base) + 1)
            idx += 1

            # Professores de disciplinas com 4+ aulas → 5 dias de disponibilidade
            if carga >= 4:
                disp = set(dias)  # todos os dias
            else:
                disp = set(dias)  # para simplificar, todos com 5 dias

            professores.append(Professor(nome, [disc], disp))
    
    return professores
