
import json
import zlib
from pathlib import Path

import pandas as pd
import streamlit as st

from alocacao import alocar, gerar_blocos, lower_bound, salas_por_dia
from horario import SLOTS

DATA = Path(__file__).parent / "data"
DIAS = {2: "Segunda", 3: "Terça", 4: "Quarta", 5: "Quinta", 6: "Sexta", 7: "Sábado"}


def grade(alocados, dia, salas):
    """Tabela sala × início do slot, com "CODIGO-TURMA" nas células ocupadas. Só salas usadas no dia."""
    df = pd.DataFrame("", index=[s["nome"] for s in salas], columns=[inicio for inicio, _ in SLOTS.values()])
    for a in alocados:
        if a["dia"] == dia:
            for inicio, fim in SLOTS.values():
                if a["inicio"] <= inicio and fim <= a["fim"]:
                    df.loc[a["sala"], inicio] = f"{a['codigo']}-{a['turma']}"
    return df[(df != "").any(axis=1)]


def cor(celula):
    """Cor fixa por disciplina (o código antes do hífen)."""
    if not celula:
        return ""
    return f"background-color: hsl({zlib.crc32(celula.split('-')[0].encode()) % 360}, 70%, 80%); color: #000"


def main():
    st.set_page_config(page_title="Alocação de salas FCTE", layout="wide")
    st.title("Alocação de salas da FCTE")
    st.caption("Interval Partitioning guloso: cada bloco (turma × dia) vai para uma sala livre que comporta a turma.")

    arquivo = st.selectbox("Semestre", sorted(DATA.glob("turmas_*.json")),
                           format_func=lambda p: p.stem.removeprefix("turmas_").replace("_", "."))
    if st.button("Rodar Interval Partitioning", type="primary"):
        salas = json.loads((DATA / "salas.json").read_text(encoding="utf-8"))
        blocos = gerar_blocos(json.loads(arquivo.read_text(encoding="utf-8")))
        st.session_state.resultado = (arquivo, blocos, salas, *alocar(blocos, salas))
    if st.session_state.get("resultado", [None])[0] != arquivo:
        st.info("Escolha o semestre e clique em **Rodar Interval Partitioning**.")
        return
    _, blocos, salas, alocados, nao_alocados = st.session_state.resultado

    por_dia = salas_por_dia(alocados)
    c = st.columns(5)
    c[0].metric("Blocos alocados", f"{len(alocados)}/{len(blocos)}")
    c[1].metric("Salas usadas", f"{len({a['sala'] for a in alocados})} de {len(salas)}")
    c[2].metric("Pico de salas num dia", max(por_dia.values(), default=0))
    c[3].metric("Limite inferior", lower_bound(blocos))
    c[4].metric("Não alocados", len(nao_alocados))

    for aba, dia in zip(st.tabs(list(DIAS.values())), DIAS):
        with aba:
            g = grade(alocados, dia, salas)
            if g.empty:
                st.write("Sem aulas neste dia.")
                continue
            st.dataframe(g.style.map(cor), use_container_width=True, height=(len(g) + 1) * 35 + 3)
            with st.expander("Turmas do dia"):
                st.dataframe(pd.DataFrame([a for a in alocados if a["dia"] == dia]).drop(columns="dia"),
                             hide_index=True, use_container_width=True)

    st.subheader("Não alocados")
    if nao_alocados:
        st.dataframe(pd.DataFrame(nao_alocados), hide_index=True, use_container_width=True)
    else:
        st.success("Todos os blocos foram alocados.")


if __name__ == "__main__":
    main()
