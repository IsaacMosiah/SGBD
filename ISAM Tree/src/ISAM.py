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

    # funções para percorrer a árvore
    def get_filho(self, chaves, rec):
        for i in range(len(chaves)):
            if rec < chaves[i]:
                return i
        return len(chaves)
    
    def buscar_no(self, rec):
        no = self.raiz

        while not isinstance(no, PaginaPrimaria):
            i = self.get_filho(no.chaves, rec)
            no = no.filhos[i]

        return no
    
    # funções para adicionar e remover registros
    def adicionar_registro(self, rec):
        no = self.buscar_no(rec)

        # página folha lotada
        if len(no.registros) == no.CAPACIDADE:
            if not no.overflow:
                new_ovflw = PaginaOverflow()
                new_ovflw.registros.append(rec)
                no.overflow = new_ovflw
                print("Registro " + str(rec) + " adicionado em nova página de overflow.")

            # se já tem uma página de overflow, checa se tem espaço
            else:
                ovflw = no.overflow

                # percorre a lista de nós overflow
                while True:
                    if len(ovflw.registros) < ovflw.CAPACIDADE:
                        ovflw.registros.append(rec)
                        print("Registro " + str(rec) + " adicionado em página de overflow existente.")
                        return
                    # se não tem espaço, verifica se há outro nó de overflow
                    if not ovflw.proximo:
                        break
                    ovflw = ovflw.proximo

                new_ovflw = PaginaOverflow()
                new_ovflw.registros.append(rec)
                ovflw.proximo = new_ovflw
                print("Registro " + str(rec) + " adicionado em nova página de overflow.")

        else:
            no.registros.append(rec)
            # se a página de folha primária está cheia, verificamos se está corretamente ordenada
            if len(no.registros) == no.CAPACIDADE:
                if no.registros[1] < no.registros[0]:
                    no.registros[0], no.registros[1] = no.registros[1], no.registros[0]

            print("Registro " + str(rec) + " adicionado em página folha primária.")

    def remover_registro(self, rec):
        # faz o caminho para onde o registro deveria estar
        no = self.buscar_no(rec)

        # remove o registro da página primária
        if rec in no.registros:
            no.registros.remove(rec)
            print("Registro " + str(rec) + " removido.")
            return

        elif no.overflow:
            ovflw = no.overflow
            prev = no

            while ovflw:
                if rec in ovflw.registros:
                    ovflw.registros.remove(rec)
                    break

                prev = ovflw
                ovflw = ovflw.proximo

            if not ovflw:
                print("Registro " + str(rec) + " não encontrado.")
                return
            
            print("Registro " + str(rec) + " removido.")

            # verificando se a página de overflow ficou vazia após a exclusão
            if not ovflw.registros:
                if isinstance(prev, PaginaPrimaria):
                    prev.overflow = ovflw.proximo
                else:
                    prev.proximo = ovflw.proximo
                
                print("Página de Overflow vazia apagada.")
                return
            return
        
        print("Registro " + str(rec) + " não encontrado.")
        return

    # funções de busca
    def busca_por_igualdade(self, rec):
        no = self.raiz
        ordem = []
        quant = 0

        while not isinstance(no, PaginaPrimaria):
            ordem.append(list(no.chaves))
            quant += 1
            filho = self.get_filho(no.chaves, rec)
            no = no.filhos[filho]

        ordem.append(list(no.registros))
        quant += 1
        if rec in no.registros:
            return True, quant, ordem
        
        ovflw = no.overflow

        while ovflw is not None:
            ordem.append(list(ovflw.registros))
            quant += 1
            if rec in ovflw.registros:
                return True, quant, ordem
            ovflw = ovflw.proximo

        return False, quant, ordem


    def busca_por_intervalo(self, rec_ini, rec_fim):
        resultados = []
        quant = 1

        for no in self.raiz.filhos:
            quant += 1
            for no2 in no.filhos:
                quant += 1
                if isinstance(no2, PaginaPrimaria):
                    for rec in no2.registros:
                        if rec_ini <= rec <= rec_fim:
                            resultados.append(rec)
                    if no2.overflow is not None:
                        ovflw = no2.overflow
                        while True:
                            quant += 1
                            for rec in ovflw.registros:
                                if rec_ini <= rec <= rec_fim:
                                    resultados.append(rec)
                            if ovflw.proximo is not None:
                                ovflw = ovflw.proximo
                            else:
                                break
        return quant, resultados
    
    # funções para métricas
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

    def media_cadeias_overflow(self):
        comprimentos = []
        for no_intermediario in self.raiz.filhos:
            for filho in no_intermediario.filhos:
                if isinstance(filho, PaginaPrimaria):
                    tamanho = 0
                    ovflw = filho.overflow
                    while ovflw is not None:
                        tamanho += 1
                        ovflw = ovflw.proximo
                    comprimentos.append(tamanho)

        folhas_com_overflow = [c for c in comprimentos if c > 0]

        if not comprimentos:
            return 0, 0

        media_todas = sum(comprimentos)/len(comprimentos)
        
        if folhas_com_overflow:
            media_com_overflow = sum(folhas_com_overflow)/len(folhas_com_overflow)
        else:
            media_com_overflow = 0

        return media_todas, media_com_overflow

    def contar_ocorrencias(self, chave):
        total = 0
        for no_intermediario in self.raiz.filhos:
            for filho in no_intermediario.filhos:
                if isinstance(filho, PaginaPrimaria):
                    total += filho.registros.count(chave)
                    ovflw = filho.overflow
                    while ovflw is not None:
                        total += ovflw.registros.count(chave)
                        ovflw = ovflw.proximo
        return total