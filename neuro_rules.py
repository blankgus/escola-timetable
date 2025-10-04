HORARIO_PESADO_MAX = 3  # Disciplinas cognitivas só até o 3º horário

def eh_horario_ideal(tipo_disciplina: str, horario: int) -> bool:
    """Retorna True se o horário é ideal para o tipo de disciplina."""
    if tipo_disciplina == "pesada":
        return horario <= HORARIO_PESADO_MAX
    elif tipo_disciplina == "pratica":
        return horario >= 4  # Ex: Educação Física no final
    else:
        return True  # 'media' ou 'leve' são flexíveis
