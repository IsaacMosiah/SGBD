from ISAM import ISAM

# montar árvore padrão
arvore = ISAM()

# extrair os nós para exibir 
raiz = arvore.raiz

no_esq = raiz.filhos[0]
no_dir = raiz.filhos[1]

folha_A = no_esq.filhos[0]
folha_B = no_esq.filhos[1]
folha_C = no_esq.filhos[2]
folha_D = no_dir.filhos[0]
folha_E = no_dir.filhos[1]
folha_F = no_dir.filhos[2]

# exibição dos nós
print("raiz:")
print(raiz.chaves)

print("nível intermediário:")
print(no_esq.chaves, no_dir.chaves)

print("páginas folha primárias:")
print(folha_A.registros, folha_B.registros, folha_C.registros, folha_D.registros, folha_E.registros, folha_F.registros)

# testar métricas
print("\nquantidade de páginas folha primárias: ", arvore.quantidade_paginas_folha())
print("quantidade de páginas de overflow: ", arvore.quantidade_paginas_overflow())

# teste de adiconar registro
arvore.adicionar_registro(18)
arvore.adicionar_registro(22)
arvore.adicionar_registro(27)
arvore.adicionar_registro(35)
arvore.adicionar_registro(41)
arvore.adicionar_registro(44)
arvore.adicionar_registro(63)
arvore.adicionar_registro(67)
arvore.adicionar_registro(83)
arvore.adicionar_registro(86)
arvore.adicionar_registro(121)
arvore.adicionar_registro(145)

# exibição de nós
print("páginas folha primárias:")
print(folha_A.registros, folha_B.registros, folha_C.registros, folha_D.registros, folha_E.registros, folha_F.registros)

print("páginas overflow:")  # --- PRECISA MELHORAR ISSO AQUI --
print(folha_A.overflow.registros, folha_B.overflow.registros, folha_C.overflow.registros, folha_D.overflow.registros, folha_E.overflow.registros, folha_F.overflow.registros, folha_F.overflow.proximo.registros, folha_F.overflow.proximo.proximo.registros)

# testar métricas após inserção
print("\nquantidade de páginas folha primárias: ", arvore.quantidade_paginas_folha())
print("quantidade de páginas de overflow: ", arvore.quantidade_paginas_overflow())

# testes de busca 
print("\nbusca por igualdade:")
print(arvore.busca_por_igualdade(18))
print(arvore.busca_por_igualdade(22))
print(arvore.busca_por_igualdade(145))
print("\nbusca por intervalo:")
print(arvore.busca_por_intervalo(27, 44))

# teste de remover registros
arvore.remover_registro(86)
arvore.remover_registro(121)
arvore.remover_registro(200)

# exibição de nós
print("páginas folha primárias:")
print(folha_A.registros, folha_B.registros, folha_C.registros, folha_D.registros, folha_E.registros, folha_F.registros)

print("páginas overflow:")  # --- PRECISA MELHORAR ISSO AQUI --
print(folha_A.overflow.registros, folha_B.overflow.registros, folha_C.overflow.registros, folha_D.overflow.registros, folha_E.overflow, folha_F.overflow.registros, folha_F.overflow.proximo.registros, folha_F.overflow.proximo.proximo)

# testar métricas após remoção
print("\nquantidade de páginas folha primárias: ", arvore.quantidade_paginas_folha())
print("quantidade de páginas de overflow: ", arvore.quantidade_paginas_overflow())

# adicionar registro após exclusão
arvore.adicionar_registro(145)

# exibição de nós
print("páginas folha primárias:")
print(folha_A.registros, folha_B.registros, folha_C.registros, folha_D.registros, folha_E.registros, folha_F.registros)

print("páginas overflow:")  # --- PRECISA MELHORAR ISSO AQUI --
print(folha_A.overflow.registros, folha_B.overflow.registros, folha_C.overflow.registros, folha_D.overflow.registros, folha_E.overflow, folha_F.overflow.registros, folha_F.overflow.proximo.registros, folha_F.overflow.proximo.proximo)

# testar métricas após remoção
print("\nquantidade de páginas folha primárias: ", arvore.quantidade_paginas_folha())
print("quantidade de páginas de overflow: ", arvore.quantidade_paginas_overflow())

# testes de busca após remoção
print("\nbusca por igualdade:")
print(arvore.busca_por_igualdade(18))
print(arvore.busca_por_igualdade(22))
print(arvore.busca_por_igualdade(145))
print("\nbusca por intervalo:")
print(arvore.busca_por_intervalo(27, 44))
