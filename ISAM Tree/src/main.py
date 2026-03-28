from ISAM import ISAM
from PaginaPrimaria import PaginaPrimaria

INSERCOES_OBRIGATORIAS = [18, 22, 27, 35, 41, 44, 63, 67, 83, 86, 121, 145]
REMOCOES_OBRIGATORIAS = [27, 44, 67, 83, 145]
BUSCAS_IGUALDADE = [22, 35, 44, 90]
BUSCAS_INTERVALO = [(20, 50), (60, 90), (120, 150)]

def folhas_em_ordem(arvore):
	folhas = []
	for no_intermediario in arvore.raiz.filhos:
		for filho in no_intermediario.filhos:
			if isinstance(filho, PaginaPrimaria):
				folhas.append(filho)
	return folhas

def descricao_overflow(folha):
	cadeia = []
	ovflw = folha.overflow
	while ovflw is not None:
		cadeia.append(list(ovflw.registros))
		ovflw = ovflw.proximo
	return cadeia

def metricas_cadeia_overflow(arvore):
	comprimentos = []
	for folha in folhas_em_ordem(arvore):
		tamanho = 0
		ovflw = folha.overflow
		while ovflw is not None:
			tamanho += 1
			ovflw = ovflw.proximo
		comprimentos.append(tamanho)

	folhas_com_overflow = [x for x in comprimentos if x > 0]
	media_todas = sum(comprimentos) / len(comprimentos)
	media_com_overflow = 0 if not folhas_com_overflow else sum(folhas_com_overflow) / len(folhas_com_overflow)
	return media_todas, media_com_overflow

def contar_ocorrencias(arvore, chave):
	total = 0
	for folha in folhas_em_ordem(arvore):
		total += folha.registros.count(chave)
		ovflw = folha.overflow
		while ovflw is not None:
			total += ovflw.registros.count(chave)
			ovflw = ovflw.proximo
	return total

def percurso_intervalo_config_atual(arvore):
	percurso = []
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

def imprimir_estado(arvore, titulo):
	print("\n" + "=" * 70)
	print(titulo)
	print("=" * 70)

	folhas = folhas_em_ordem(arvore)
	for i, folha in enumerate(folhas, start=1):
		cadeia = descricao_overflow(folha)
		print("Folha " + str(i) + " primária: " + str(folha.registros) + " | overflow: " + str(cadeia))

	media_todas, media_com_overflow = metricas_cadeia_overflow(arvore)
	print("\nMétricas:")
	print("- Quantidade de páginas folha: " + str(arvore.quantidade_paginas_folha()))
	print("- Quantidade de páginas overflow: " + str(arvore.quantidade_paginas_overflow()))
	print("- Tamanho médio das cadeias (todas as folhas): " + f"{media_todas:.2f}")
	print("- Tamanho médio das cadeias (folhas com overflow): " + f"{media_com_overflow:.2f}")

def imprimir_percurso_igualdade(arvore, chave):
	encontrado, custo, ordem = arvore.busca_por_igualdade(chave)
	print("\nExemplo de percurso - busca por igualdade(" + str(chave) + ")")
	print("Páginas visitadas, na ordem:")
	for i, pagina in enumerate(ordem, start=1):
		print(str(i) + ". " + str(pagina))
	print("Custo aproximado (nós/páginas percorridos): " + str(custo))
	print("Resultado: " + ("encontrado" if encontrado else "não encontrado"))

def imprimir_percurso_intervalo(arvore, ini, fim):
	custo, resultados = arvore.busca_por_intervalo(ini, fim)
	percurso = percurso_intervalo_config_atual(arvore)
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
		antes = contar_ocorrencias(arvore, chave)
		arvore.remover_registro(chave)
		depois = contar_ocorrencias(arvore, chave)
		if depois == max(antes - 1, 0):
			removidos_efetivos += 1
	imprimir_estado(arvore, "APÓS REMOÇÕES OBRIGATÓRIAS")
	print("- Quantidade de registros removidos (efetivos): " + str(removidos_efetivos))

	print("\nBuscas obrigatórias para medição de custo")
	for chave in BUSCAS_IGUALDADE:
		encontrado, custo, _ = arvore.busca_por_igualdade(chave)
		print("- buscar(" + str(chave) + "): custo=" + str(custo) + ", encontrado=" + str(encontrado))

	for ini, fim in BUSCAS_INTERVALO:
		custo, resultados = arvore.busca_por_intervalo(ini, fim)
		print("- buscar_intervalo(" + str(ini) + ", " + str(fim) + "): custo=" + str(custo) + ", resultados=" + str(sorted(resultados)))

	# Explicação pedida no enunciado: caminho de uma igualdade e de um intervalo.
	imprimir_percurso_igualdade(arvore, 22)
	imprimir_percurso_intervalo(arvore, 20, 50)

if __name__ == "__main__":
	main()