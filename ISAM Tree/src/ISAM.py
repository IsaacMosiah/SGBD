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

        # nível intermediário
        no_esq = NoIndice()
        no_dir = NoIndice()

        no_esq.chaves = [20, 33]
        no_dir.chaves = [51, 63]

        no_esq.filhos = [folha_A, folha_B, folha_C]
        no_dir.filhos = [folha_D, folha_E, folha_F]

        # raiz
        self.raiz = NoIndice()
        self.raiz.chaves = [40]
        self.raiz.filhos = [no_esq, no_dir]

    def adicionar_registro(self, rec):
        no = self.buscar_no(rec)

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
                    else:
                        ovflw = ovflw.proximo

                new_ovflw = PaginaOverflow()
                new_ovflw.registros.append(rec)
                ovflw.proximo = new_ovflw

        else:   #ainda tem espaço na página folha
            no.registros.append(rec)

    def remover_registro(self, rec):
        # faz o caminho para onde o registro deveria estar
        no = self.buscar_no(rec)

        if rec in no.registros:
            i = no.registros.index(rec)
            no.registros.pop(i)

        elif no.overflow is not None:
            ovflw = no.overflow
            # se o registro não está no no, deve estar nas folhas de overflow
            while True:
                if rec in ovflw.registros:
                    i = ovflw.registros.index(rec)
                    ovflw.registros.pop(i)

                    # se a pagina overflow ficou vazia, vamos excluí-la
                    if len(ovflw.registros) == 0:
                        ovflw.registros.append('x') # marcamos a página a ser excluída
                        prev_ovflw = self.buscar_no(rec)
                        if 'x' in prev_ovflw.overflow.registros: # se a primeira página overflow contém o marcador
                            prev_ovflw.overflow = None
                            break

                        # se não, vamos entrar nas páginas encadeadas procurando o marcador
                        prev_ovflw = prev_ovflw.overflow
                        while True:
                            if 'x' in prev_ovflw.proximo.registros: # se a proxima página overflow contém o marcador
                                if prev_ovflw.proximo.proximo is not None: # se há uma página de overflow após a página com marcador
                                    prev_ovflw.proximo = prev_ovflw.proximo.proximo # 'pulamos' a página marcada
                                    break
                                else:
                                    prev_ovflw.proximo = None
                                    break
                            elif prev_ovflw.proximo is not None:
                                prev_ovflw = prev_ovflw.proximo
                            else:
                                break
                            
                    break
                elif ovflw.proximo is not None:
                    ovflw = ovflw.proximo
                else:
                    print("Registro não está presente na árvore")
                    return

        print("Registro removido.")
        return

    def buscar_no(self, rec):
        no = self.raiz

        while not isinstance(no, PaginaPrimaria):
            i = self.get_filho(no.chaves, rec)
            no = no.filhos[i]

        return no
    
    def get_filho(self, chaves, rec):
        for i in range(len(chaves)):
            if rec <= chaves[i]:
                return i
        return len(chaves)
        
    def quantidade_paginas_folha(self):
        qtd = 0
        for no in self.raiz.filhos:
            for no2 in no.filhos:
                if isinstance(no2, PaginaPrimaria):
                    qtd += 1 
        return qtd
    
    def quantidade_paginas_overflow(self):
        qtd = 0
        for no in self.raiz.filhos:
            for no2 in no.filhos:
                if isinstance(no2, PaginaPrimaria):
                    if no2.overflow is not None:
                        ovflw = no2.overflow
                        qtd += 1
                        # checa páginas de overflow linkadas e adiciona a contagem
                        while True:
                            if ovflw.proximo is not None:
                                qtd += 1
                                ovflw = ovflw.proximo
                            else:
                                break

                    else:
                        qtd += 0
        return qtd

    def busca_por_igualdade(self, rec):
        no = self.raiz
        ordem = []

        while not isinstance(no, PaginaPrimaria):
            ordem.append(list(no.chaves))
            filho = self.get_filho(no.chaves, rec)
            no = no.filhos[filho]

        ordem.append(list(no.registros))
        if rec in no.registros:
            return True, ordem
        
        ovflw = no.overflow

        while ovflw is not None:
            ordem.append(list(ovflw.registros))
            if rec in ovflw.registros:
                return True, ordem
            ovflw = ovflw.proximo

        return False, ordem    


    def busca_por_intervalo(self, rec_ini, rec_fim):
        resultados = []
        for no in self.raiz.filhos:
            for no2 in no.filhos:
                if isinstance(no2, PaginaPrimaria):
                    for rec in no2.registros:
                        if rec_ini <= rec <= rec_fim:
                            resultados.append(rec)
                    if no2.overflow is not None:
                        ovflw = no2.overflow
                        while True:
                            for rec in ovflw.registros:
                                if rec_ini <= rec <= rec_fim:
                                    resultados.append(rec)
                            if ovflw.proximo is not None:
                                ovflw = ovflw.proximo
                            else:
                                break
        return resultados