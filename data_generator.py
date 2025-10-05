# data_generator.py
from models import Turma, Professor, Disciplina
import random

def gerar_disciplinas():
    ef2 = [
        Disciplina("Português", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Matemática", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Ciências", 3, "media", ["6ano", "7ano"]),
        Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Geografia", 3, "media", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Inglês", 3, "media", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Artes", 1, "leve", ["6ano", "7ano", "8ano", "9ano"]),
        Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"]),
    ]
    em = [
        Disciplina("Português", 5, "pesada", ["1em", "2em", "3em"]),
        Disciplina("Matemática", 5, "pesada", ["1em", "2em", "3em"]),
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
    
    disc_por_prof = {
        "Português": 3,
        "Matemática": 3,
        "Ciências": 2,
        "Biologia": 2,
        "Física": 2,
        "Química": 2,
        "História": 2,
        "Geografia": 2,
        "Inglês": 2,
        "Artes": 1,
        "Educação Física": 1,
        "Filosofia": 1,
        "Sociologia": 1,
    }

    professores = []
    idx = 0
    dias = ["seg", "ter", "qua", "qui", "sex"]

    for disc, qtd in disc_por_prof.items():
        for _ in range(qtd):
            nome = nomes_base[idx % len(nomes_base)]
            if idx >= len(nomes_base):
                nome += str(idx // len(nomes_base) + 1)
            idx += 1
            # Garantir disponibilidade VIÁVEL: pelo menos 4 dias
            k = random.randint(4, 5)
            disp = set(random.sample(dias, k=k))
            professores.append(Professor(nome, [disc], disp))
    
    return professores
