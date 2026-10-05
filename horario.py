
import re

# Horário de cada slot, na ordem do dia. N2–N4 não aparecem nos dados de 2026.2;
# seguem a tabela da UnB.
SLOTS = {
    "M1": ("08:00", "08:55"), "M2": ("08:55", "09:50"), "M3": ("10:00", "10:55"),
    "M4": ("10:55", "11:50"), "M5": ("12:00", "12:55"),
    "T1": ("12:55", "13:50"), "T2": ("14:00", "14:55"), "T3": ("14:55", "15:50"),
    "T4": ("16:00", "16:55"), "T5": ("16:55", "17:50"), "T6": ("18:00", "18:55"),
    "N1": ("18:55", "19:50"), "N2": ("19:50", "20:40"), "N3": ("20:50", "21:40"),
    "N4": ("21:40", "22:30"),
}
ORDEM = list(SLOTS)
BLOCO = re.compile(r"([2-7]+)([MTN])([1-6]+)")


def parse_horario(codigo):
    """Retorna [(dia, inicio, fim), ...] ordenado por dia e início.

    Slots consecutivos no mesmo dia viram um único intervalo, como o SIGAA mostra
    (ex.: "6T2345" -> sexta 14:00 às 17:50).
    """
    codigo = codigo.strip()
    blocos = BLOCO.findall(codigo)
    if not blocos or BLOCO.sub("", codigo).strip():
        raise ValueError(f"horário inválido: {codigo!r}")
    por_dia = {}
    for dias, turno, slots in blocos:
        for d in dias:
            for s in slots:
                por_dia.setdefault(int(d), set()).add(ORDEM.index(turno + s))
    intervalos = []
    for dia in sorted(por_dia):
        idx = sorted(por_dia[dia])
        inicio = idx[0]
        for a, b in zip(idx, idx[1:] + [None]):
            if b != a + 1:
                intervalos.append((dia, SLOTS[ORDEM[inicio]][0], SLOTS[ORDEM[a]][1]))
                inicio = b
    return intervalos
