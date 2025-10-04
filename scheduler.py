from models import Aula
from neuro_rules import eh_horario_ideal
from collections import defaultdict
import random

class GradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = {p.nome: p for p in professores}
        self.disciplinas = disciplinas
        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        self.horarios = list(range(1, 7))
        self.solucao = []
        self.prof_aulas = defaultdict(list)
        self.turma_aulas = defaultdict(list)
        self.disc_por_turma = self._calcular_carga()

    def _calcular_carga(self):
        from collections import defaultdict
        carga = defaultdict(lambda: defaultdict(int))
        for turma in self.turmas:
            for nome_disc, disc in self.disciplinas.items():
                if turma.serie in disc.series:
                    carga[turma.nome][nome_disc] = disc.carga_semanal
        return carga

    def gerar_grade(self, max_tentativas=20):
        for tentativa in range(max_tentativas):
            try:
                self._reset()
                self._atribuir_todas_aulas()
                return True
            except Exception:
                continue
        raise Exception("Falha: não foi possível gerar grade válida.")

    def _reset(self):
        self.solucao = []
        self.prof_aulas = defaultdict(list)
        self.turma_aulas = defaultdict(list)

    def _atribuir_todas_aulas(self):
        pendentes = []
        for turma_nome in self.disc_por_turma:
            for disc, carga in self.disc_por_turma[turma_nome].items():
                for _ in range(carga):
                    pendentes.append((turma_nome, disc))
        pendentes.sort(key=lambda x: 0 if self.disciplinas[x[1]].tipo == "pesada" else 1)

        for turma_nome, disc_nome in pendentes:
            if not self._atribuir_aula(turma_nome, disc_nome):
                raise Exception(f"Impossível atribuir {disc_nome} → {turma_nome}")

    def _atribuir_aula(self, turma_nome, disc_nome):
        profs = [p for p in self.professores.values() if disc_nome in p.disciplinas]
        if not profs:
            return False
        random.shuffle(profs)

        combinacoes = []
        for dia in self.dias:
            for horario in self.horarios:
                ideal = eh_horario_ideal(self.disciplinas[disc_nome].tipo, horario)
                combinacoes.append((dia, horario, ideal))
        combinacoes.sort(key=lambda x: x[2], reverse=True)

        for prof in profs:
            for dia, horario, _ in combinacoes:
                if self._pode_agendar(turma_nome, disc_nome, prof.nome, dia, horario):
                    aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario)
                    self.solucao.append(aula)
                    self.prof_aulas[prof.nome].append(aula)
                    self.turma_aulas[turma_nome].append(aula)
                    return True
        return False

    def _pode_agendar(self, turma, disc, prof, dia, horario):
        if dia not in self.professores[prof].disponibilidade:
            return False
        for a in self.prof_aulas[prof]:
            if a.dia == dia and a.horario == horario:
                return False
        for a in self.turma_aulas[turma]:
            if a.dia == dia and a.horario == horario:
                return False
        return True
