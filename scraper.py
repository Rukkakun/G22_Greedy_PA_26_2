"""Coleta as turmas de graduação da FCTE (campus Gama) no SIGAA público da UnB.

Uso: python -m scraper --ano 2026 --periodo 2
"""
import argparse
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://sigaa.unb.br/sigaa/public"
URL = f"{BASE}/turmas/listar.jsf"
FCTE = "673"  # CAMPUS UNB GAMA: FACULDADE DE CIÊNCIAS E TECNOLOGIAS EM ENGENHARIA


def buscar_html(ano, periodo, unidade=FCTE):
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    # Sem visitar a home antes, o POST é redirecionado para /sigaa/public/.
    s.get(f"{BASE}/home.jsf", timeout=30)
    form = BeautifulSoup(s.get(URL, timeout=30).content, "html.parser").find("form", id="formTurma")
    dados = {i["name"]: i.get("value", "") for i in form.find_all("input")
             if i.get("name") and i.get("type") != "submit"}
    buscar = next(i["name"] for i in form.find_all("input", type="submit") if i["value"] == "Buscar")
    dados.update({
        "formTurma:inputNivel": "G",
        "formTurma:inputDepto": unidade,
        "formTurma:inputAno": str(ano),
        "formTurma:inputPeriodo": str(periodo),
        buscar: "Buscar",
    })
    r = s.post(URL, data=dados, headers={"Referer": URL, "Origin": "https://sigaa.unb.br"},
               allow_redirects=False, timeout=60)
    r.raise_for_status()
    if r.status_code != 200:
        raise RuntimeError(f"SIGAA redirecionou para {r.headers.get('Location')}")
    return r.content


def extrair_turmas(html):
    tabela = BeautifulSoup(html, "html.parser").find("table", class_="listagem")
    if tabela is None:
        return []
    turmas, codigo, nome = [], None, None
    for tr in tabela.find_all("tr"):
        classes = tr.get("class") or []
        if "agrupador" in classes:
            codigo, nome = tr.get_text(" ", strip=True).split(" - ", 1)
            continue
        if "linhaPar" not in classes and "linhaImpar" not in classes:
            continue
        td = tr.find_all("td")
        # O popup dentro da célula de horário traz o texto legível ("Sexta-feira 14:00 às 17:50").
        popup = td[3].find("div", class_="popUp")
        horario_texto = [x.strip() for x in popup.stripped_strings] if popup else []
        if popup:
            popup.parent.decompose()
        horario = re.sub(r"\(.*?\)", "", td[3].get_text(" ", strip=True))
        turmas.append({
            "codigo": codigo,
            "nome": nome,
            "turma": td[0].get_text(strip=True),
            "periodo": td[1].get_text(strip=True),
            "docente": td[2].get_text(" ", strip=True),
            "horario": " ".join(horario.split()),
            "horario_texto": horario_texto,
            "vagas_ofertadas": int(td[5].get_text(strip=True) or 0),
            "vagas_ocupadas": int(td[6].get_text(strip=True) or 0),
            "local": td[7].get_text(" ", strip=True),
        })
    return turmas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ano", type=int, default=2026)
    p.add_argument("--periodo", type=int, default=2)
    p.add_argument("--saida", type=Path)
    a = p.parse_args()
    turmas = extrair_turmas(buscar_html(a.ano, a.periodo))
    saida = a.saida or Path("data") / f"turmas_{a.ano}_{a.periodo}.json"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(turmas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(turmas)} turmas salvas em {saida}")


if __name__ == "__main__":
    main()
