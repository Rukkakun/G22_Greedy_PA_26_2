
import argparse
import json
import re
from pathlib import Path

# Nomes com "/" que não separam salas.
JUNTOS = {
    "NIT/LDS": "NIT-LDS",
    "TERMOFLUIDOS/TERMO-SUP": "TERMOFLUIDOS",
    "TERMODINÂMICA / TERMO-SUP": "TERMODINÂMICA",
}
APELIDOS = {"NIT-LDS": "LAB NIT-LDS", "TERMOFLUIDOS": "LAB TERMOFLUIDOS"}


def separar_local(local):
    """'FCTE - I3 / LAB SS' -> ['I3', 'LAB SS']. Locais fora da FCTE -> []."""
    s = local.upper()
    if s.startswith("FT "):
        return []
    s = re.sub(r"^FCTE\s*[-/]\s*", "", s)
    s = re.sub(r"\(.*?\)", "", s).replace("LAB.", "LAB").replace("SALAS ", "")
    for velho, novo in JUNTOS.items():
        s = s.replace(velho, novo)
    salas = []
    for nome in s.split("/"):
        nome = " ".join(nome.split())
        nome = APELIDOS.get(nome, nome)
        if nome and nome not in salas:
            salas.append(nome)
    return salas


def tipo(nome):
    return "laboratorio" if nome.startswith("LAB") or "LDTEA" in nome or nome in {"SHP", "MULTIUSO"} else "sala"


def montar_salas(turmas):
    sozinha, composta = {}, {}
    for t in turmas:
        salas = separar_local(t["local"])
        alvo = sozinha if len(salas) == 1 else composta
        for nome in salas:
            alvo[nome] = max(alvo.get(nome, 0), t["vagas_ofertadas"])
    nomes = sorted(sozinha.keys() | composta.keys())
    return [{"nome": n, "capacidade": sozinha.get(n) or composta[n], "tipo": tipo(n)} for n in nomes]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("turmas", type=Path)
    p.add_argument("--saida", type=Path, default=Path("data/salas.json"))
    a = p.parse_args()
    salas = montar_salas(json.loads(a.turmas.read_text(encoding="utf-8")))
    a.saida.write_text(json.dumps(salas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(salas)} salas -> {a.saida}")


if __name__ == "__main__":
    main()
