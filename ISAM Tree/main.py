from ISAM import ISAM

arvore = ISAM()

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

print("Raiz:")
print(" ", raiz.chaves)

print("\nNível intermediário 1:")
print(" ", no_esq.chaves)
print(" ", no_dir.chaves)

print("\nNível intermediário 2:")
print(" ", no_A.chaves)
print(" ", no_B.chaves)
print(" ", no_C.chaves)
print(" ", no_D.chaves)
print(" ", no_E.chaves)
print(" ", no_F.chaves)

print("\nPáginas folha primárias:")
print(" ", folha_A.registros)
print(" ", folha_B.registros)
print(" ", folha_C.registros)
print(" ", folha_D.registros)
print(" ", folha_E.registros)
print(" ", folha_F.registros)