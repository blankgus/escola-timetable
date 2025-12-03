3. scheduler_ortools.py
```python
# scheduler_ortools.py
from ortools.sat.python import cp_model
from collections import defaultdict
from models import Aula, DIAS_SEMANA


class GradeHorariaORTools:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = {d.nome: d for d in disciplinas}

        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        self.horarios = [1, 2, 3, 4, 5, 6, 7]

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = 10

        self.disciplinas_por_turma = self._disciplinas_por_turma()
        self.atribuicoes = {}
        self._preparar_dados()
        self._criar_variaveis()
        self._restricoes()

    # --------------------------------------------------------------
    def _disciplinas_por_turma(self):
        out = defaultdict(list)
        for t in self.turmas:
            for d in self.disciplinas.values():
                if t.serie in d.series:
                    out[t.nome].extend([d.nome] * d.carga_semanal)
        return out

    # --------------------------------------------------------------
    def _preparar_dados(self):
        for turma, lista in self.disciplinas_por_turma.items():
            for disc in set(lista):
                for dia in self.dias:
                    for h in self.horarios:
                        profs = [
                            p.nome for p in self.professores
                            if disc in p.disciplinas
                            and dia in p.disponibilidade_dias
                            and h in p.disponibilidade_horarios
                        ]
                        if profs:
                            self.atribuicoes[(turma, disc, dia, h)] = profs

    # --------------------------------------------------------------
    def _criar_variaveis(self):
        self.X = {}
        for (turma, disc, dia, h), profs in self.atribuicoes.items():
            for prof in profs:
                self.X[(turma, disc, dia, h, prof)] = self.model.NewBoolVar(
                    f"x_{turma}_{disc}_{dia}_{h}_{prof}"
                )

    # util
    def _filtra(self, **f):
        return [v for (t, d, dia, h, p), v in self.X.items()
                if (f.get("turma", t) == t and
                    f.get("disc", d) == d and
                    f.get("dia", dia) == dia and
                    f.get("horario", h) == h and
                    f.get("prof", p) == p)]

    # --------------------------------------------------------------
    def _restricoes(self):
        # 1 turma/dia/horário ≤ 1
        for turma in self.disciplinas_por_turma:
            for dia in self.dias:
                for h in self.horarios:
                    v = self._filtra(turma=turma, dia=dia, horario=h)
                    if v:
                        self.model.Add(sum(v) <= 1)

        # 2 carga exata
        for turma, lista in self.disciplinas_por_turma.items():
            for disc, qtd in defaultdict(int, {d: lista.count(d) for d in lista}).items():
                v = self._filtra(turma=turma, disc=disc)
                self.model.Add(sum(v) == qtd)

        # 3 professor não simultâneo
        for p in self.professores:
            for dia in self.dias:
                for h in self.horarios:
                    v = self._filtra(prof=p.nome, dia=dia, horario=h)
                    if v:
                        self.model.Add(sum(v) <= 1)

    # --------------------------------------------------------------
    def resolver(self):
        st = self.solver.Solve(self.model)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("Sem solução viável")

        aulas = []
        for (turma, disc, dia, h, prof), var in self.X.items():
            if self.solver.Value(var):
                aulas.append(Aula(turma, disc, prof, dia, h))
        return aulas
```
