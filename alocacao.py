
import argparse
import json
from pathlib import Path

from horario import parse_horario


def gerar_blocos(turmas):
    """Um bloco {codigo, turma, nome, vagas, dia, inicio, fim} por dia de aula de cada turma."""
    return [
        {"codigo": t["codigo"], "turma": t["turma"], "nome": t["nome"], "vagas": t["vagas_ofertadas"],
         "dia": dia, "inicio": inicio, "fim": fim}
        for t in turmas
        for dia, inicio, fim in parse_horario(t["horario"])
    ]


def lower_bound(blocos):
    """Profundidade máxima: o maior número de blocos acontecendo ao mesmo tempo."""
    # No empate de horário o fim (-1) vem antes do início (+1): 12:55–12:55 não conflita.
    eventos = sorted((b["dia"], h, d) for b in blocos for h, d in ((b["inicio"], 1), (b["fim"], -1)))
    prof = maior = 0
    for _, _, d in eventos:
        prof += d
        maior = max(maior, prof)
    return maior


def alocar(blocos, salas):
    """Retorna (alocados, nao_alocados). Cada alocado é o bloco com a chave "sala".

    Percorre os blocos por dia e hora de início. Entre as salas livres que comportam
    a turma, prefere uma já aberta naquele dia (o guloso clássico) e, depois, a menor,
    para guardar as salas grandes para as turmas grandes.
    """
    livre_em = {}  # (sala, dia) -> hora em que a sala fica livre; ausente = sala ainda fechada no dia
    alocados, nao_alocados = [], []
    # No empate de início, a turma maior escolhe primeiro.
    for b in sorted(blocos, key=lambda b: (b["dia"], b["inicio"], -b["vagas"])):
        livres = [s for s in salas
                  if s["capacidade"] >= b["vagas"] and livre_em.get((s["nome"], b["dia"]), "") <= b["inicio"]]
        if not livres:
            nao_alocados.append(b)
            continue
        sala = min(livres, key=lambda s: ((s["nome"], b["dia"]) not in livre_em, s["capacidade"]))
        livre_em[(sala["nome"], b["dia"])] = b["fim"]
        alocados.append({**b, "sala": sala["nome"]})
    return alocados, nao_alocados


def salas_por_dia(alocados):
    """{dia: nº de salas distintas usadas naquele dia}."""
    usadas = {}
    for a in alocados:
        usadas.setdefault(a["dia"], set()).add(a["sala"])
    return {dia: len(s) for dia, s in sorted(usadas.items())}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("turmas", type=Path)
    p.add_argument("--salas", type=Path, default=Path("data/salas.json"))
    a = p.parse_args()
    blocos = gerar_blocos(json.loads(a.turmas.read_text(encoding="utf-8")))
    salas = json.loads(a.salas.read_text(encoding="utf-8"))
    alocados, nao_alocados = alocar(blocos, salas)
    por_dia = salas_por_dia(alocados)

    print(f"{len(alocados)}/{len(blocos)} blocos alocados")
    print(f"salas usadas: {len({x['sala'] for x in alocados})} de {len(salas)} "
          f"(pico num dia: {max(por_dia.values())}, limite inferior: {lower_bound(blocos)})")
    if nao_alocados:
        print("\nNão alocados (falta sala livre com capacidade):")
        for b in nao_alocados:
            print(f"  {b['codigo']}-{b['turma']} {b['nome']} | dia {b['dia']} "
                  f"{b['inicio']}-{b['fim']} | {b['vagas']} vagas")


if __name__ == "__main__":
    main()
