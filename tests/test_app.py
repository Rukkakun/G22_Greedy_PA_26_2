from streamlit.testing.v1 import AppTest

from app import grade


def test_grade():
    alocados = [{"codigo": "FCTE0005", "turma": "01", "dia": 6, "inicio": "14:00", "fim": "15:50", "sala": "S1"}]
    salas = [{"nome": "S1"}, {"nome": "S2"}]
    g = grade(alocados, 6, salas)
    assert list(g.index) == ["S1"]
    assert [c for c in g.columns if g.loc["S1", c]] == ["14:00", "14:55"]
    assert grade(alocados, 2, salas).empty


def test_app_roda():
    at = AppTest.from_file("app.py", default_timeout=30).run()
    at.button[0].click().run()
    assert not at.exception
    assert [m.label for m in at.metric] == [
        "Blocos alocados", "Salas usadas", "Pico de salas num dia", "Lower bound", "Não alocados"]
    assert at.metric[0].value == "430/430"
