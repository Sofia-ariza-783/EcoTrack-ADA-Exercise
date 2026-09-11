from ecotrack.parser import analizar, total_kg_co2e


def test_caso_canonico_separa_comida_de_transporte():
    actividades = analizar("Hoy comí carne y viajé 20km en bus")

    assert len(actividades) == 2
    assert total_kg_co2e(actividades) == 8.71


def test_cada_segmento_usa_su_propio_medio_de_transporte():
    actividades = analizar("fui 5km en bici y 30km en carro")

    etiquetas = {actividad.etiqueta: actividad.kg_co2e for actividad in actividades}
    assert etiquetas["Bicicleta / caminando"] == 0.0
    assert etiquetas["Auto particular"] == 5.13


def test_texto_sin_actividades_reconocibles_devuelve_lista_vacia():
    assert analizar("hoy fue un día tranquilo en casa") == []


def test_texto_vacio_devuelve_lista_vacia():
    assert analizar("") == []
    assert analizar("   ") == []


def test_cantidad_escrita_en_palabras():
    actividades = analizar("comí dos porciones de pollo")

    assert len(actividades) == 1
    assert actividades[0].cantidad == 2.0
    assert actividades[0].kg_co2e == 1.84


def test_avion_y_pescado_no_se_confunden():
    actividades = analizar("Volé 500km en avión y comí pescado")

    etiquetas = {actividad.etiqueta: actividad.kg_co2e for actividad in actividades}
    assert etiquetas["Avión"] == 123.0
    assert etiquetas["Pescado"] == 0.81
