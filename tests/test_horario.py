import pytest

from horario import parse_horario

# Casos reais de 2026.2, conferidos com o texto que o SIGAA mostra para cada turma.
CASOS = {
    "35T23": [(3, "14:00", "15:50"), (5, "14:00", "15:50")],
    "6T2345": [(6, "14:00", "17:50")],
    "7M1234": [(7, "08:00", "11:50")],
    "35M5 35T1": [(3, "12:00", "13:50"), (5, "12:00", "13:50")],
    "24T6 24N1": [(2, "18:00", "19:50"), (4, "18:00", "19:50")],
    "3M125 5M12": [(3, "08:00", "09:50"), (3, "12:00", "12:55"), (5, "08:00", "09:50")],
    "46M12 2T4": [(2, "16:00", "16:55"), (4, "08:00", "09:50"), (6, "08:00", "09:50")],
    "3M5 2T45 3T1": [(2, "16:00", "17:50"), (3, "12:00", "13:50")],
}


@pytest.mark.parametrize("codigo,esperado", CASOS.items())
def test_parse_horario(codigo, esperado):
    assert parse_horario(codigo) == esperado


@pytest.mark.parametrize("codigo", ["", "8M1", "3X1", "35T23 lixo"])
def test_invalido(codigo):
    with pytest.raises(ValueError):
        parse_horario(codigo)
