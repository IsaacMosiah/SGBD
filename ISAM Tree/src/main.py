from ISAM import ISAM
from PaginaPrimaria import PaginaPrimaria

INSERCOES_OBRIGATORIAS = [18, 22, 27, 35, 41, 44, 63, 67, 83, 86, 121, 145]
REMOCOES_OBRIGATORIAS = [27, 44, 67, 83, 145]
BUSCAS_IGUALDADE = [22, 35, 44, 90]
BUSCAS_INTERVALO = [(20, 50), (60, 90), (120, 150)]

# funções para imprimir o estado da árvore e os percursos de busca
def percurso_intervalo(arvore):
	percurso = [arvore.raiz.chaves]
	for no_intermediario in arvore.raiz.filhos:
		percurso.append(list(no_intermediario.chaves))
		for filho in no_intermediario.filhos:
			if isinstance(filho, PaginaPrimaria):
				percurso.append(list(filho.registros))
				ovflw = filho.overflow
				while ovflw is not None:
					percurso.append(list(ovflw.registros))
					ovflw = ovflw.proximo
	return percurso

# função para auxiliar no print
def imprimir_estado(arvore, titulo):
	print("\n" + "=" * 70)
	print(titulo)
	print("=" * 70)

	folhas = []
	for no_intermediario in arvore.raiz.filhos:
		for filho in no_intermediario.filhos:
			if isinstance(filho, PaginaPrimaria):
				folhas.append(filho)

	for i, folha in enumerate(folhas, start=1):
		cadeia = []
		ovflw = folha.overflow
		while ovflw is not None:
			cadeia.append(list(ovflw.registros))
			ovflw = ovflw.proximo
		print("Folha " + str(i) + " primária: " + str(folha.registros) + " | overflow: " + str(cadeia))

	media_todas, media_com_overflow = arvore.media_cadeias_overflow()
	print("\nMétricas:")
	print("- Quantidade de páginas folha: " + str(arvore.quantidade_paginas_folha()))
	print("- Quantidade de páginas overflow: " + str(arvore.quantidade_paginas_overflow()))
	print("- Tamanho médio das cadeias (todas as folhas): " + f"{media_todas:.2f}")
	print("- Tamanho médio das cadeias (folhas com overflow): " + f"{media_com_overflow:.2f}")

# funções para imprimir percursos de busca por igauldade
def imprimir_percurso_igualdade(arvore, chave):
	encontrado, custo, ordem = arvore.busca_por_igualdade(chave)
	print("\nExemplo de percurso - busca por igualdade(" + str(chave) + ")")
	print("Páginas visitadas, na ordem:")
	for i, pagina in enumerate(ordem, start=1):
		print(str(i) + ". " + str(pagina))
	print("Custo aproximado (nós/páginas percorridos): " + str(custo))
	print("Resultado: " + ("encontrado" if encontrado else "não encontrado"))

# funções para imprimir percursos de busca por intervalo
def imprimir_percurso_intervalo(arvore, ini, fim):
	custo, resultados = arvore.busca_por_intervalo(ini, fim)
	percurso = percurso_intervalo(arvore)
	print("\nExemplo de percurso - busca por intervalo(" + str(ini) + ", " + str(fim) + ")")
	print("Páginas visitadas, na ordem:")
	for i, pagina in enumerate(percurso, start=1):
		print(str(i) + ". " + str(pagina))
	print("Custo aproximado (nós/páginas percorridos): " + str(custo))
	print("Resultado: " + str(sorted(resultados)))

def main():
	arvore = ISAM()

	imprimir_estado(arvore, "ESTADO INICIAL")

	print("\nAplicando inserções obrigatórias...")
	for chave in INSERCOES_OBRIGATORIAS:
		arvore.adicionar_registro(chave)
	imprimir_estado(arvore, "APÓS INSERÇÕES OBRIGATÓRIAS")

	print("\nAplicando remoções obrigatórias...")
	removidos_efetivos = 0
	for chave in REMOCOES_OBRIGATORIAS:
		antes = arvore.contar_ocorrencias(chave)
		arvore.remover_registro(chave)
		depois = arvore.contar_ocorrencias(chave)
		if depois == max(antes - 1, 0):
			removidos_efetivos += 1
	imprimir_estado(arvore, "APÓS REMOÇÕES OBRIGATÓRIAS")
	print("- Quantidade de registros removidos (efetivos): " + str(removidos_efetivos))

	print("\nBuscas obrigatórias para medição de custo")
	for chave in BUSCAS_IGUALDADE:
		encontrado, custo, _ = arvore.busca_por_igualdade(chave)
		print("- buscar(" + str(chave) + "): custo = " + str(custo) + ", encontrado = " + str(encontrado))

	for ini, fim in BUSCAS_INTERVALO:
		custo, resultados = arvore.busca_por_intervalo(ini, fim)
		print("- buscar_intervalo(" + str(ini) + ", " + str(fim) + "): custo = " + str(custo) + ", resultados = " + str(sorted(resultados)))

	# explicação pedida no enunciado: caminho de uma igualdade e de um intervalo.
	imprimir_percurso_igualdade(arvore, 22)
	imprimir_percurso_intervalo(arvore, 20, 50)

if __name__ == "__main__":
	main()