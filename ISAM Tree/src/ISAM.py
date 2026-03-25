from No import NoIndice
from PaginaPrimaria import PaginaPrimaria
from PaginaOverflow import PaginaOverflow

class ISAM:
    def __init__(self):
        # páginas folha primárias
        folha_A = PaginaPrimaria()
        folha_B = PaginaPrimaria()
        folha_C = PaginaPrimaria()
        folha_D = PaginaPrimaria()
        folha_E = PaginaPrimaria()
        folha_F = PaginaPrimaria()

        folha_A.registros = [10, 15]
        folha_B.registros = [20, 27]
        folha_C.registros = [33, 37]
        folha_D.registros = [40, 46]
        folha_E.registros = [51, 55]
        folha_F.registros = [63, 97]

        # nível intermediário 2
        no_A = NoIndice()
        no_B = NoIndice()
        no_C = NoIndice()
        no_D = NoIndice()
        no_E = NoIndice()
        no_F = NoIndice()

        no_A.chaves = [10, 15]
        no_B.chaves = [20, 27]
        no_C.chaves = [33, 37]
        no_D.chaves = [40, 46]
        no_E.chaves = [51, 55]
        no_F.chaves = [63, 97]

        no_A.filhos = [folha_A]
        no_B.filhos = [folha_B]
        no_C.filhos = [folha_C]
        no_D.filhos = [folha_D]
        no_E.filhos = [folha_E]
        no_F.filhos = [folha_F]

        # nível intermediário 1
        no_esq = NoIndice()
        no_dir = NoIndice()

        no_esq.chaves = [20, 33]
        no_dir.chaves = [51, 63]

        no_esq.filhos = [no_A, no_B, no_C]
        no_dir.filhos = [no_D, no_E, no_F]

        # raiz
        self.raiz = NoIndice()
        self.raiz.chaves = [40]
        self.raiz.filhos = [no_esq, no_dir]

    def adicionar_registro(self, rec):
        no = self.buscar_no(rec)
        no = no.filhos[0]

        if len(no.registros) == no.CAPACIDADE: # página folha lotada
            if not no.overflow: #não há overflow
                new_ovflw = PaginaOverflow()
                new_ovflw.registros.append(rec)
                no.overflow = new_ovflw

            # se já tem uma página de overflow, checa se tem espaço
            else:
                ovflw = no.overflow

                # percorre a lista de nós overflow
                while True:
                    if len(ovflw.registros) < ovflw.CAPACIDADE:
                        ovflw.registros.append(rec)
                        return
                    # se não tem espaço, verifica se há outro nó de overflow
                    if not ovflw.proximo:
                        break
                    ovflw = ovflw.proximo

                new_ovflw = PaginaOverflow()
                new_ovflw.registros.append(rec)
                ovflw.proximo = new_ovflw

        else:   #ainda tem espaço na página folha
            no.chaves.append(rec)
            
            

    def buscar_no(self, rec):
        no = self.raiz

        while len(no.filhos) > 1:
            i = self.get_filho(no.chaves, rec)
            no = no.filhos[i]

        return no
    
    def get_filho(self, chaves, rec):
        for i in range(len(chaves)):
            if rec < chaves[i]:
                return i
        return len(chaves)
        
    def quantidade_paginas_folha(self):
        qtd = 0
        for no in self.raiz.filhos:
            for no2 in no.filhos:
                for no3 in no2.filhos:
                    if isinstance(no3, PaginaPrimaria):
                        qtd += 1 
        return qtd
    
    def quantidade_paginas_overflow(self):
        qtd = 0
        for no in self.raiz.filhos:
            for no2 in no.filhos:
                for no3 in no2.filhos:
                    if isinstance(no3, PaginaPrimaria):
                        if no3.overflow is not None:
                            qtd += 1
                        else:
                            qtd += 0
        return qtd