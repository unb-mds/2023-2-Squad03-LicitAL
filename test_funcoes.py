import unittest
from diario_municipal import Municipio, Diario  

class TestMunicipio(unittest.TestCase):
    def test_criacao_municipio(self):
        nome_municipio = "Maceió"
        municipio = Municipio(nome_municipio)
        
        self.assertEqual(municipio.nome, nome_municipio)
        self.assertEqual(municipio.id, "maceio")

    def test_criacao_municipio_com_caracteres_especiais(self):
        nome_municipio = "São Miguel dos Campos"
        municipio = Municipio(nome_municipio)

        self.assertEqual(municipio.nome, nome_municipio)
        self.assertEqual(municipio.id, "sao-miguel-dos-campos")

    def test_criacao_municipio_com_barra_AL(self):
        nome_municipio = "Viçosa/AL"
        municipio = Municipio(nome_municipio)

        self.assertEqual(municipio.nome, "Viçosa")
        self.assertEqual(municipio.id, "vicosa")

class TestDiario(unittest.TestCase):
    def test_criacao_diario(self):
        municipio = Municipio("Maceió")
        cabecalho = "17 de Janeiro de 2023"
        texto = "Conteúdo do diário..."

        diario = Diario(municipio, cabecalho, texto)

        self.assertEqual(diario.municipio, "Maceió")
        self.assertEqual(diario.id, "maceio")
        self.assertEqual(diario.cabecalho, cabecalho)
        self.assertEqual(diario.texto, texto)
        self.assertEqual(diario.data_publicacao.year, 2023)
        self.assertEqual(diario.data_publicacao.month, 1)
        self.assertEqual(diario.data_publicacao.day, 17)

if __name__ == '__main__':
    unittest.main()
