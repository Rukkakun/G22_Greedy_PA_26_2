from salas import montar_salas, separar_local


def test_separar_local():
    assert separar_local("FCTE - I3 / LAB SS") == ["I3", "LAB SS"]
    assert separar_local("FCTE- LAB NEI 2") == ["LAB NEI 2"]
    assert separar_local("FCTE - I7/I4/I4") == ["I7", "I4"]
    assert separar_local("FCTE - LAB. NIT/LDS") == ["LAB NIT-LDS"]
    assert separar_local("NIT/LDS(segunda)/I1(sexta)") == ["LAB NIT-LDS", "I1"]
    assert separar_local("FCTE - Salas S4 /S4 / S10 / S10  (120 Vagas)") == ["S4", "S10"]
    assert separar_local("FT - UnB / Campus Darcy Ribeiro") == []


def test_montar_salas():
    turmas = [
        {"local": "FCTE - S4", "vagas_ofertadas": 100},
        {"local": "FCTE - S1 / S4", "vagas_ofertadas": 120},
        {"local": "FCTE - LAB SS", "vagas_ofertadas": 20},
    ]
    assert montar_salas(turmas) == [
        {"nome": "LAB SS", "capacidade": 20, "tipo": "laboratorio"},
        {"nome": "S1", "capacidade": 120, "tipo": "sala"},
        {"nome": "S4", "capacidade": 100, "tipo": "sala"},
    ]
