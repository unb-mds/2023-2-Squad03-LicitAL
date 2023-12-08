import unittest
import tempfile
import os
import json
from extrator_valores import extrair_valores

class TestExtratorValores(unittest.TestCase):

    def setUp(self):
        # Cria arquivos temporários para os testes
        self.arquivo_temporario_uma_licitacao = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
        self.arquivo_temporario_multiplas_licitacoes = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')

        # Caminhos para os arquivos temporários
        self.caminho_temporario_uma_licitacao = self.arquivo_temporario_uma_licitacao.name
        self.caminho_temporario_multiplas_licitacoes = self.arquivo_temporario_multiplas_licitacoes.name

    def tearDown(self):
        # Remove os arquivos temporários após os testes
        os.remove(self.caminho_temporario_uma_licitacao)
        os.remove(self.caminho_temporario_multiplas_licitacoes)

    def test_extrair_valores_uma_licitacao(self):
        # Cria o arquivo de resultado
        resultado_json = self.caminho_temporario_uma_licitacao

        # Executa a função de teste
        extrair_valores(self.caminho_temporario, resultado_json)

        # Verifica se o arquivo de resultado foi criado corretamente
        self.assertTrue(os.path.exists(resultado_json))

        # Carrega os resultados como JSON
        with open(resultado_json, 'r', encoding='utf-8') as arquivo_resultado:
            resultados_obtidos = json.load(arquivo_resultado)

        # Resultados esperados para um caso com uma licitação
        resultados_esperados = [
            {"municipio": "Cidade1", "valores_gastos": 1000.0, "quantidade_licitacoes": 1},
        ]

        # Verifica se os resultados obtidos são iguais aos resultados esperados
        self.assertEqual(resultados_obtidos, resultados_esperados)

    def test_extrair_valores_multiplas_licitacoes(self):
        # Cria o arquivo de resultado
        resultado_json = self.caminho_temporario_multiplas_licitacoes

        # Executa a função de teste
        extrair_valores(self.caminho_temporario, resultado_json)

        # Verifica se o arquivo de resultado foi criado corretamente
        self.assertTrue(os.path.exists(resultado_json))

        # Carrega os resultados como JSON
        with open(resultado_json, 'r', encoding='utf-8') as arquivo_resultado:
            resultados_obtidos = json.load(arquivo_resultado)

        # Resultados esperados para um caso com múltiplas licitações
        resultados_esperados = [
            {"municipio": "Cidade1", "valores_gastos": 1500.0, "quantidade_licitacoes": 2},
            {"municipio": "Cidade2", "valores_gastos": 2500.0, "quantidade_licitacoes": 1},
        ]

        # Verifica se os resultados obtidos são iguais aos resultados esperados
        self.assertEqual(resultados_obtidos, resultados_esperados)

if __name__ == '__main__':
    unittest.main()
