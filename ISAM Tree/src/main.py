from ISAM import ISAM

# montar árvore padrão
arvore = ISAM()

# extrair os nós para exibir 
raiz = arvore.raiz
no_esq = raiz.filhos[0]
no_dir = raiz.filhos[1]

no_A = no_esq.filhos[0]
no_B = no_esq.filhos[1]
no_C = no_esq.filhos[2]
no_D = no_dir.filhos[0]
no_E = no_dir.filhos[1]
no_F = no_dir.filhos[2]

folha_A = no_A.filhos[0]
folha_B = no_B.filhos[0]
folha_C = no_C.filhos[0]
folha_D = no_D.filhos[0]
folha_E = no_E.filhos[0]
folha_F = no_F.filhos[0]

# exibição dos nós
print("raiz:")
print(raiz.chaves)

print("nível intermediário 1:")
print(no_esq.chaves, no_dir.chaves)

print("nível intermediário 2:")
print(no_A.chaves, no_B.chaves, no_C.chaves, no_D.chaves, no_E.chaves, no_F.chaves)

print("páginas folha primárias:")
print(folha_A.registros, folha_B.registros, folha_C.registros, folha_D.registros, folha_E.registros, folha_F.registros)

# testar métricas
print("\nquantidade de páginas folha primárias: ", arvore.quantidade_paginas_folha())
print("quantidade de páginas de overflow: ", arvore.quantidade_paginas_overflow())