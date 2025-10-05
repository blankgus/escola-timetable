# neuro_rules.py
def eh_horario_ideal(tipo_disciplina: str, horario: int) -> bool:
    """
    Usado apenas para OTIMIZAÇÃO (não é restrição rígida).
    """
    if tipo_disciplina == "pesada":
        return horario <= 4  # até o 4º horário (não 3º)
    elif tipo_disciplina == "pratica":
        return horario >= 4
    else:
        return True
