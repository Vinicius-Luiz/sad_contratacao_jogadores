import Model as Mdl

class Knapsack_Problem():
    def __init__(self, totalCaixa):
        self.totalCaixa = totalCaixa
    
    def run(self, csvJogadores):
        jogadores      = {}
        for i in range(1, len(csvJogadores)+1):
            jogador = csvJogadores[i-1]
            jogador = jogador.split(';')
            jogador = (jogador[0], int(jogador[1]), int(jogador[2]))
            jogadores[i] = jogador

        result = self.melhorCombo(len(csvJogadores), self.totalCaixa, jogadores)
        return result

    def get_matriz(self, matriz):
        for i in range (1, len(matriz)):
            print(matriz[i])#, j[i][0])

    def melhorCombo(self, tJ, tC, j):
        matriz = [[0]*(tC+1)]
        for i in range(tJ):
            linhaTemp = [0]*(tC+1)
            matriz.append(linhaTemp)
        iLinha = 1
        while iLinha <= tJ:
            iColuna = 0
            for coluna in matriz[iLinha]:
                if iColuna >= j[iLinha][1]:
                    v1 = matriz[iLinha-1][iColuna]
                    v2 = j[iLinha][2] + matriz[iLinha-1][iColuna - j[iLinha][1]] 
                    matriz[iLinha][iColuna] = max(v1, v2)
                else:
                    matriz[iLinha][iColuna] = matriz[iLinha-1][iColuna]
                iColuna += 1
            iLinha += 1
        #self.get_matriz(matriz)

        melhorPontuacao = 0
        melhorValor = 0
        melhoresJogadores = []
        iColunaTemp = -1
        for linha in range(tJ, 0, -1):
             if matriz[linha][iColunaTemp] != matriz[linha-1][iColunaTemp]:
                 melhoresJogadores.append(j[linha][0])
                 melhorValor += j[linha][1]
                 melhorPontuacao += j[linha][2]
                 iColunaTemp -= j[linha][1]
        
        #print(melhorPontuacao)
        #print(melhorValor)
        #print(melhoresJogadores)
        return melhoresJogadores
class Dataframe():
    def __init__(self, json):
        self.metodo = json['metodo_pesquisa']['metodo']
        self.valor = json['metodo_pesquisa']['valor']
        self.posicao = json['posicao']
        self.idade = json['idade']
        self.nacionalidade = json['nacionalidade']
        self.reputacao_internacional = json['reputacao_internacional']
        self.ligas = json['ligas']
        self.qtd_combo = json['combo']
        
        self.df_filter = self.exec_filter()
        
        self.exec_combo()
        '''
        {'metodo_pesquisa': {'metodo': 1, 'valor': 151000}, 
        'posicao': {'GK': 0, 'CB': 0, 'RB': 0, 'LB': 0, 'CDM': 0, 'CM': 1, 'RM': 1, 'LM': 0, 'CAM': 0, 'RW': 0, 'LW': 0, 'CF': 0, 'ST': 0},
        'idade': 'Todos', 'nacionalidade': 'Burundi', 'reputacao_internacional': 'Muito alta',
        'ligas': ['English Premier League', 'Italian Serie A'], 'combo': 1}
        '''
    
    def get_df(self):
        return Mdl.df()

    def exec_filter(self):
        df = self.get_df()
        df = self.filtrar_posicao()
        df = self.filtrar_idade()
        df = self.filtrar_nacionalidade()
        df = self.filtrar_reputacao()
        df = self.filtrar_ligas()
        return df
        
    def filtrar_posicao(self):
        pass

    def filtrar_idade(self):
        pass

    def filtrar_nacionalidade(self):
        pass

    def filtrar_reputacao(self):
        pass

    def filtrar_ligas(self):
        pass

    def filtrar_result_jogadores(self, result):
        #após sabermos a melhor combinação, devemos filtrar os jogadores retornados pelo ID dele
        pass

    def jogadores_to_csv(self):
        # saida deve ser ['13052000;8;57', 'id_jogador;valor;pontuacao']
        if self.metodo == 1:
            pass
        elif self.metodo == 2:
            pass
        elif self.metodo == 3:
            pass

    def exec_combo(self):
        jogadores = self.jogadores_to_csv()
        algorithm = Knapsack_Problem(self.valor)
        result    = algorithm.run(jogadores)
        self.export_excel(result)
    
    def export_excel(self, result):
        pass