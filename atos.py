import json
import re


def extrair(texto_diario: str):
    atos = []
    matches = re.findall(
        r"^[\s\S]*?Código Identificador:.*$(?:\n|)", texto_diario, re.MULTILINE)
    for match in matches:
        atos.append(AtoNormativo(match.strip()))
    return atos


class AtoNormativo:
    # Expressão regular para encontrar valores gastos em licitações
    re_valores_licitacoes = r"R\$.+"

    def __init__(self, texto: str):
        self.texto = texto
        self.cod = self._extrai_cod(texto)
        self.valores_licitacoes = self._extrai_valores_licitacoes()

    def _extrai_cod(self, texto: str):
        matches = re.findall(r'Código Identificador:(.*)', texto)
        return matches[0].strip()

    def _extrai_valores_licitacoes(self):
        valores_licitacoes = re.findall(self.re_valores_licitacoes, self.texto)
        return valores_licitacoes

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)