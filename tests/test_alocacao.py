import json
from pathlib import Path

from alocacao import alocar, gerar_blocos, lower_bound, salas_por_dia


def bloco(nome, dia, inicio, fim, vagas=10):
    return {"codigo": nome, "turma": "01", "nome": nome, "vagas": vagas, "dia": dia, "inicio": inicio, "fim": fim}


def sala(nome, capacidade):
    return {"nome": nome, "capacidade": capacidade, "tipo": "sala"}


def verificar(alocados, salas):
    """Nenhuma sala com blocos sobrepostos e nenhuma capacidade estourada."""
    cap = {s["nome"]: s["capacidade"] for s in salas}
    por_sala = {}
    for a in alocados:
        assert a["vagas"] <= cap[a["sala"]]
        por_sala.setdefault((a["sala"], a["dia"]), []).append((a["inicio"], a["fim"]))
    for intervalos in por_sala.values():
        intervalos.sort()
        for (_, fim), (inicio, _) in zip(intervalos, intervalos[1:]):
            assert fim <= inicio


def test_gerar_blocos():
    turmas = [{"codigo": "FCTE0005", "turma": "01", "nome": "GRAFOS", "vagas_ofertadas": 80, "horario": "35T23"}]
    assert [(b["dia"], b["inicio"], b["fim"]) for b in gerar_blocos(turmas)] == [
        (3, "14:00", "15:50"), (5, "14:00", "15:50")]


def test_lower_bound():
    blocos = [bloco("A", 2, "08:00", "09:50"), bloco("B", 2, "08:55", "10:55"),
              bloco("C", 2, "09:50", "11:50"), bloco("D", 3, "08:00", "09:50")]
    assert lower_bound(blocos) == 2  # A–B e B–C se sobrepõem; A termina quando C começa


def test_reusa_sala_e_usa_lower_bound():
    blocos = [bloco("A", 2, "08:00", "09:50"), bloco("B", 2, "08:55", "10:55"), bloco("C", 2, "09:50", "11:50")]
    salas = [sala("S1", 50), sala("S2", 50), sala("S3", 50)]
    alocados, nao = alocar(blocos, salas)
    verificar(alocados, salas)
    assert nao == []
    assert salas_por_dia(alocados) == {2: lower_bound(blocos)}


def test_respeita_capacidade_e_reporta_nao_alocados():
    blocos = [bloco("PEQ", 2, "08:00", "09:50", vagas=40), bloco("GRANDE", 2, "08:00", "09:50", vagas=100),
              bloco("OUTRA", 2, "08:00", "09:50", vagas=30)]
    salas = [sala("S1", 120), sala("I1", 45)]
    alocados, nao = alocar(blocos, salas)
    verificar(alocados, salas)
    assert {a["codigo"]: a["sala"] for a in alocados} == {"GRANDE": "S1", "PEQ": "I1"}
    assert [b["codigo"] for b in nao] == ["OUTRA"]


def test_dados_reais():
    turmas = json.loads(Path("data/turmas_2026_2.json").read_text(encoding="utf-8"))
    salas = json.loads(Path("data/salas.json").read_text(encoding="utf-8"))
    blocos = gerar_blocos(turmas)
    alocados, nao = alocar(blocos, salas)
    verificar(alocados, salas)
    assert len(alocados) + len(nao) == len(blocos)


def test_dados_reais_sem_capacidade_atinge_lower_bound():
    """Sem restrição de capacidade, o guloso usa exatamente a profundidade máxima de salas."""
    turmas = json.loads(Path("data/turmas_2026_2.json").read_text(encoding="utf-8"))
    blocos = gerar_blocos(turmas)
    salas = [sala(f"X{i}", 10**6) for i in range(len(blocos))]
    alocados, nao = alocar(blocos, salas)
    verificar(alocados, salas)
    assert nao == []
    assert max(salas_por_dia(alocados).values()) == lower_bound(blocos)
