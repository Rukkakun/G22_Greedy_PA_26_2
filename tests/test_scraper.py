from scraper import extrair_turmas

HTML = """
<table class="listagem">
<tr><th>Código</th></tr>
<tr class="agrupador"><td>FCTE0005 - ALGORITMOS EM GRAFOS</td></tr>
<tr class="linhaPar">
  <td>01</td><td>2026.2</td><td>EDSON ALVES (60h)</td>
  <td> 35M5  35T1 (10/08/2026 - 14/12/2026) <img/>
    <span><div class="popUp">Terça-feira 12:00 às 13:50<br/>Quinta-feira 12:00 às 13:50 <br/></div></span>
  </td>
  <td></td><td>80</td><td>71</td><td>FCTE - I9/I10</td>
</tr>
<tr><td>1 turmas encontrada(s)</td></tr>
</table>
"""


def test_extrair_turmas():
    assert extrair_turmas(HTML) == [{
        "codigo": "FCTE0005",
        "nome": "ALGORITMOS EM GRAFOS",
        "turma": "01",
        "periodo": "2026.2",
        "docente": "EDSON ALVES (60h)",
        "horario": "35M5 35T1",
        "horario_texto": ["Terça-feira 12:00 às 13:50", "Quinta-feira 12:00 às 13:50"],
        "vagas_ofertadas": 80,
        "vagas_ocupadas": 71,
        "local": "FCTE - I9/I10",
    }]


def test_sem_tabela():
    assert extrair_turmas("<html></html>") == []
