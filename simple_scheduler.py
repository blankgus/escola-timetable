4. simple_scheduler.py  (algoritmo aleatório opcional)
```python
# simple_scheduler.py
import random
from collections import defaultdict
from models import Aula


class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = {p.nome: p for p in professores}
        self.disciplinas = {d.nome: d for d in disciplinas}

        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        self.horarios = [1, 2, 3, 4, 5, 6, 7]

        # carga por turma/disciplina
        self.carga = defaultdict(lambda: defaultdict(int))
        for t in turmas:
            for d in disciplinas:
                if t.serie in d.series:
                    self.carga[t.nome][d.nome] = d.carga_semanal

    # --------------------------------------------------------------
    def gerar_grade(self):
        aulas = []
        for turma in self.turmas:
            disp = [(d, h) for d in self.dias for h in self.horarios]
            random.shuffle(disp)
            for disc, qtd in self.carga[turma.nome].items():
                for _ in range(qtd):
                    dia, hor = disp.pop()
                    profs = [p for p in self.professores.values()
                             if disc in p.disciplinas and
                                dia in p.disponibilidade_dias and
                                hor in p.disponibilidade_horarios]
                    if not profs:
                        raise RuntimeError(f"Sem professor para {disc}")
                    prof = random.choice(profs)
                    aulas.append(Aula(turma.nome, disc, prof.nome, dia, hor))
        return aulas
```
