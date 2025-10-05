# neuro_rules.py
# Regras de neurociência — usadas como OBJETIVO, não como restrição rígida

HORARIO_PESADO_MAX = 4  # Disciplinas cognitivas ideais até o 4º horário

def eh_horario_ideal(tipo_disciplina: str, horario: int) -> bool:
    """
    Retorna True se o horário é ideal para o tipo de disciplina.
    Usado para OTIMIZAÇÃO, não para bloquear atribuições.
    """
    if tipo_disciplina == "pesada":
        return horario <= HORARIO_PESADO_MAX
    elif tipo_disciplina == "pratica":
        return horario >= 4  # Ex: Educação Física no final
    else:
        return True  # 'media' ou 'leve' são flexíveis
