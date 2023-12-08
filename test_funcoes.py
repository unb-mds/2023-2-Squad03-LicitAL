import unittest
import tempfile
import os
import json
from extrator_valores import extrair_valores

class TestExtratorValores(unittest.TestCase):

    def setUp(self):
        # Cria um arquivo temporário para o teste
        self.arquivo_temporario = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
        self.arquivo_temporario.close()

        # Caminho para o arquivo temporário
        self.caminho_temporario = self.arquivo_temporario.name

    def tearDown(self):
        # Remove o arquivo temporário após o teste
        os.remove(self.caminho_temporario)

    def test_extrair_valores_uma_licitacao(self):
        # Dados de exemplo para o arquivo JSON de entrada
        dados_entrada = [
            '{"municipio": "Cidade1", "valor_licitacao": 1000.00, "quantidade": 1}',
        ]

        # Escreve os dados no arquivo temporário
        with open(self.caminho_temporario, 'w', encoding='utf-8') as arquivo_entrada:
            arquivo_entrada.write('\n'.join(dados_entrada))

        # Caminho para o arquivo de resultado
        resultado_json = 'resultado_teste_uma_licitacao.json'

        # Executa a função de teste
        extrair_valores(self.caminho_temporario, resultado_json)

        # Lê os resultados do arquivo de resultado
        with open(resultado_json, 'r', encoding='utf-8') as arquivo_resultado:
            resultados_obtidos = json.load(arquivo_resultado)

        # Resultados esperados para um caso com uma licitação
        resultados_esperados = [
            {"municipio": "Cidade1", "valores_gastos": 1000.0, "quantidade_licitacoes": 1, "ano": 2023, "mes": 12},
        ]

        # Verifica se os resultados obtidos são iguais aos resultados esperados
        self.assertEqual(resultados_obtidos, resultados_esperados)

    def test_extrair_valores_multiplas_licitacoes(self):
        # Dados de exemplo para o arquivo JSON de entrada
        dados_entrada = [
            '{"municipio": "Cidade1", "valor_licitacao": 1000.00, "quantidade": 1}',
            '{"municipio": "Cidade2", "valor_licitacao": 2500.00, "quantidade": 1}',
            '{"municipio": "Cidade1", "valor_licitacao": 500.00, "quantidade": 1}',
        ]

        # Escreve os dados no arquivo temporário
        with open(self.caminho_temporario, 'w', encoding='utf-8') as arquivo_entrada:
            arquivo_entrada.write('\n'.join(dados_entrada))

        # Caminho para o arquivo de resultado
        resultado_json = 'resultado_teste_multiplas_licitacoes.json'

        # Executa a função de teste
        extrair_valores(self.caminho_temporario, resultado_json)

        # Lê os resultados do arquivo de resultado
        with open(resultado_json, 'r', encoding='utf-8') as arquivo_resultado:
            resultados_obtidos = json.load(arquivo_resultado)

        # Resultados esperados para um caso com múltiplas licitações
        resultados_esperados = [
            {"municipio": "Cidade1", "valores_gastos": 1500.0, "quantidade_licitacoes": 2, "ano": 2023, "mes": 12},
            {"municipio": "Cidade2", "valores_gastos": 2500.0, "quantidade_licitacoes": 1, "ano": 2023, "mes": 12},
        ]

        # Verifica se os resultados obtidos são iguais aos resultados esperados
        self.assertEqual(resultados_obtidos, resultados_esperados)

if __name__ == '__main__':
    unittest.main()
