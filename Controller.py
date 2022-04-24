import Model as Mdl
import pandas as pd
import time

class Knapsack_Problem():
    def __init__(self, totalCaixa):
        self.totalCaixa = totalCaixa
    
    def run(self, csvJogadores):
        jogadores      = {}
        for i in range(1, len(csvJogadores)+1):
            jogador = csvJogadores[i-1]
            jogador = jogador.split(';')
            jogador = (jogador[0], int(float(jogador[1])), int(float(jogador[2])))
            jogadores[i] = jogador

        result = self.melhorCombo(len(csvJogadores), self.totalCaixa, jogadores)
        return result

    def get_matriz(self, matriz):
        for i in range (1, len(matriz)):
            print(matriz[i])#, j[i][0])

    def melhorCombo(self, tJ, tC, j):
        inicio = time.time()
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
                 melhoresJogadores.append(int(j[linha][0].replace('.0', '')))
                 melhorValor += j[linha][1]
                 melhorPontuacao += j[linha][2]
                 iColunaTemp -= j[linha][1]
        fim = time.time()
        print(fim - inicio)
        return melhoresJogadores
    
class Dataframe():
    def __init__(self, json):
        self.df_results = []
        self.df  = self.get_df_input()

        self.metodo  = json['metodo_pesquisa']['metodo']
        self.posicao = json['posicao']
        self.idade   = json['idade']
        self.nacionalidade           = json['nacionalidade']
        self.reputacao_internacional = json['reputacao_internacional']
        self.ligas                   = json['ligas']
        self.qtd_combo               = json['combo']

        self.optimized, self.div, self.value_filter_points = self.set_valor_optimized(json)

        self.valor           = json['metodo_pesquisa']['valor']//self.div
        self.df['value_eur'] = self.df['value_eur']//self.div
        self.df['wage_eur']  = self.df['wage_eur']//self.div
        self.df['release_clause_eur'] = self.df['release_clause_eur']//self.div
            
        self.main()
    
    def set_valor_optimized(self, json):
        '''return necessita_otimização | dividendo p/ diminuir tam da matriz | filtro points'''
        if self.metodo == 1:
            if json['metodo_pesquisa']['valor'] >= 10**7:
                return True, 1000, 80
            elif json['metodo_pesquisa']['valor'] >= 10*(10**6):
                return True, 100, 75
            elif json['metodo_pesquisa']['valor'] >= 10**6:
                return True, 100, 72
            elif json['metodo_pesquisa']['valor'] >= 10**5:
                return False, 10, 70
            else:
                return False, 1, 70
        elif self.metodo == 2:
            if json['metodo_pesquisa']['valor'] >= 10**6:
                return True, 100, 80
            elif json['metodo_pesquisa']['valor'] >= 10**5:
                return True, 10, 75
            elif json['metodo_pesquisa']['valor'] >= 10**4:
                return True, 1, 72
            else:
                return False, 1, 70
        elif self.metodo == 3:
            if json['metodo_pesquisa']['valor'] >= 10**9:
                return True, 1000000, 80
            elif json['metodo_pesquisa']['valor'] >= 10**8:
                return True, 100000, 80
            elif json['metodo_pesquisa']['valor'] >= 10**7:
                return False, 1000, 75
            elif json['metodo_pesquisa']['valor'] >= 10**6:
                return False, 100, 72
            elif json['metodo_pesquisa']['valor'] >= 10**5:
                return False, 10, 70
            else:
                return False, 1, 70
    
    def main(self):
        self.exec_filter()
        self.calculate_points()
        if self.optimized:
            self.exec_filter('best')
        for i in range(self.qtd_combo):        
            if i >= self.qtd_combo/2:
                self.exec_filter('best')
            self.exec_combo()
        self.export_excel()
    
    def get_df_input(self):
        return Mdl.df_input()
    
    def get_df_output(self):
        return Mdl.df_output()

    def exec_filter(self, metodo = 'auto'):
        if metodo == 'best':
            self.filtrar_points()
            return
        self.filtrar_posicao()
        self.filtrar_idade()
        self.filtrar_nacionalidade()
        self.filtrar_reputacao()
        self.filtrar_ligas()
        
    def filtrar_points(self):
        if self.df[self.df['points'] >= self.value_filter_points].shape[0] > 20:
            self.df = self.df[self.df['points'] >= self.value_filter_points]
    
    def filtrar_posicao(self):
        self.df = self.df[self.df['player_positions'].str.contains(self.posicao, na=False)]

    def filtrar_idade(self):
        if self.idade == '<= 21':
            self.df = self.df[self.df['age'] <= 21 ]
        elif self.idade == '22 - 27':
            self.df = self.df[(self.df['age'] >= 22) & (self.df['age'] <= 27)]
        elif self.idade == '28 - 33':
            self.df = self.df[(self.df['age'] >= 28) & (self.df['age'] <= 33)]
        elif self.idade == '34 - 39':
            self.df = self.df[(self.df['age'] >= 34) & (self.df['age'] <= 39)]
        elif self.idade == '>= 40':
            self.df = self.df[self.df['age'] >= 40 ]

    def filtrar_nacionalidade(self):
        if self.nacionalidade != 'Todos':
            self.df = self.df[self.df['nationality_name'] == self.nacionalidade]

    def filtrar_reputacao(self):
        if self.reputacao_internacional == 'Muito alta':
            self.df = self.df[self.df['international_reputation'] == 5]
        elif self.reputacao_internacional == 'Alta':
            self.df = self.df[self.df['international_reputation'] == 4]
        elif self.reputacao_internacional == 'Média':
            self.df = self.df[self.df['international_reputation'] == 3]
        elif self.reputacao_internacional == 'Baixa':
            self.df = self.df[self.df['international_reputation'] == 2]
        elif self.reputacao_internacional == 'Muito baixa':
            self.df = self.df[self.df['international_reputation'] == 1]

    def filtrar_ligas(self):
        if 'Todos' not in self.ligas and len(self.ligas) != 0:
            df_temp = self.df[self.df['league_name'] == 'XXX']
            for liga in self.ligas:
                df_temp = pd.concat([self.df[self.df['league_name'] == liga], df_temp])
            self.df = df_temp
    
    def calculate_points(self):
        if self.posicao == 'GK':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['movement_agility']*4)+(self.df['movement_reactions']*6)+
                    (self.df['movement_balance']*4)+(self.df['power_shot_power']*5)+(self.df['power_jumping']*6)+(self.df['power_strength']*6)+
                    (self.df['mentality_vision']*4)+(self.df['mentality_composure']*5)+(self.df['goalkeeping_diving']*7)+(self.df['goalkeeping_handling']*6)+
                    (self.df['goalkeeping_kicking']*6)+(self.df['goalkeeping_positioning']*6)+(self.df['goalkeeping_reflexes']*7)+(self.df['goalkeeping_speed']*4)+
                    (self.df['gk']*7))/102, 5)
        
        elif self.posicao == 'CB':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.3)+(self.df['skill_moves']*0.2)+(self.df['pace']*6)+
                    (self.df['shooting']*4)+(self.df['passing']*5)+(self.df['dribbling']*6)+(self.df['defending']*7)+(self.df['physic']*7)+
                    (self.df['skill_ball_control']*6)+(self.df['movement_acceleration']*6)+(self.df['movement_sprint_speed']*6)+(self.df['movement_agility']*6)+(self.df['movement_reactions']*6)+
                    (self.df['movement_balance']*6)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*8)+(self.df['mentality_aggression']*7)+
                    (self.df['mentality_interceptions']*7)+(self.df['mentality_positioning']*4)+(self.df['mentality_vision']*5)+(self.df['mentality_composure']*6)+(self.df['defending_marking_awareness']*7)+
                    (self.df['defending_standing_tackle']*7)+(self.df['defending_sliding_tackle']*6)+(self.df['lcb']*7)+(self.df['cb']*7)+(self.df['rcb']*7)
                    )/182.5, 5)
            
        elif self.posicao == 'RB':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.3)+(self.df['skill_moves']*0.3)+(self.df['pace']*7)+
                    (self.df['shooting']*5)+(self.df['passing']*6)+(self.df['dribbling']*6)+(self.df['defending']*6)+(self.df['physic']*7)+
                    (self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*5)+(self.df['attacking_heading_accuracy']*6)+(self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*4)+
                    (self.df['skill_dribbling']*6)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*4)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*6)+
                    (self.df['movement_acceleration']*7)+(self.df['movement_sprint_speed']*7)+(self.df['movement_agility']*7)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*6)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*7)+(self.df['power_long_shots']*5)+
                    (self.df['mentality_aggression']*7)+(self.df['mentality_interceptions']*6)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*5)+
                    (self.df['mentality_composure']*6)+(self.df['defending_marking_awareness']*6)+(self.df['defending_standing_tackle']*6)+(self.df['defending_sliding_tackle']*6)+(self.df['rwb']*7)+
                    (self.df['rb']*7)
                    )/245.6, 5)

        elif self.posicao == 'LB':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.3)+(self.df['skill_moves']*0.3)+(self.df['pace']*7)+
                    (self.df['shooting']*5)+(self.df['passing']*6)+(self.df['dribbling']*6)+(self.df['defending']*6)+(self.df['physic']*7)+
                    (self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*5)+(self.df['attacking_heading_accuracy']*6)+(self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*4)+
                    (self.df['skill_dribbling']*6)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*5)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*6)+
                    (self.df['movement_acceleration']*7)+(self.df['movement_sprint_speed']*7)+(self.df['movement_agility']*7)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*6)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*7)+(self.df['power_long_shots']*5)+
                    (self.df['mentality_aggression']*7)+(self.df['mentality_interceptions']*6)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*5)+
                    (self.df['mentality_composure']*6)+(self.df['defending_marking_awareness']*6)+(self.df['defending_standing_tackle']*6)+(self.df['defending_sliding_tackle']*6)+(self.df['rwb']*7)+
                    (self.df['rb']*7)
                    )/246.6, 5)
            
        elif self.posicao == 'CDM':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.3)+(self.df['skill_moves']*0.3)+(self.df['pace']*6)+
                    (self.df['shooting']*6)+(self.df['passing']*6)+(self.df['dribbling']*6)+(self.df['defending']*6)+(self.df['physic']*7)+
                    (self.df['skill_dribbling']*6)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*7)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*6)+(self.df['movement_sprint_speed']*6)+(self.df['movement_agility']*7)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*7)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*7)+(self.df['mentality_interceptions']*6)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*5)+
                    (self.df['mentality_composure']*6)+(self.df['defending_marking_awareness']*6)+(self.df['defending_standing_tackle']*7)+(self.df['defending_marking_awareness']*6)+
                    (self.df['cdm']*7)+(self.df['ldm']*7)+(self.df['rdm']*7)
                    )/230.6, 5)

        elif self.posicao == 'CM':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.3)+(self.df['skill_moves']*0.3)+(self.df['pace']*7)+
                    (self.df['shooting']*6)+(self.df['passing']*6)+(self.df['dribbling']*7)+(self.df['defending']*6)+(self.df['physic']*7)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*7)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*7)+(self.df['movement_sprint_speed']*7)+(self.df['movement_agility']*7)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*7)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*7)+(self.df['mentality_interceptions']*6)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*7)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*7)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*6)+(self.df['attacking_heading_accuracy']*6)+
                    (self.df['attacking_short_passing']*7)+(self.df['attacking_volleys']*5)+(self.df['cm']*7)+(self.df['lcm']*7)+(self.df['rcm']*7)
                    )/249.6, 5)

        elif self.posicao == 'RM':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.4)+(self.df['skill_moves']*0.3)+(self.df['pace']*8)+
                    (self.df['shooting']*6)+(self.df['passing']*6)+(self.df['dribbling']*7)+(self.df['defending']*5)+(self.df['physic']*6)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*8)+(self.df['movement_sprint_speed']*8)+(self.df['movement_agility']*8)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*8)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*6)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*5)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*6)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*6)+(self.df['attacking_heading_accuracy']*5)+
                    (self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*6)+(self.df['rm']*7)
                    )/231.7, 5)

        elif self.posicao == 'LM':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.4)+(self.df['skill_moves']*0.3)+(self.df['pace']*8)+
                    (self.df['shooting']*6)+(self.df['passing']*6)+(self.df['dribbling']*7)+(self.df['defending']*5)+(self.df['physic']*6)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*8)+(self.df['movement_sprint_speed']*8)+(self.df['movement_agility']*8)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*8)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*6)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*5)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*6)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*6)+(self.df['attacking_heading_accuracy']*5)+
                    (self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*6)+(self.df['lm']*7)
                    )/232.7, 5)
            
        elif self.posicao == 'CAM':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.4)+(self.df['skill_moves']*0.4)+(self.df['pace']*7)+
                    (self.df['shooting']*5)+(self.df['passing']*7)+(self.df['dribbling']*7)+(self.df['defending']*5)+(self.df['physic']*6)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*7)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*7)+(self.df['movement_sprint_speed']*7)+(self.df['movement_agility']*8)+(self.df['movement_reactions']*7)+(self.df['movement_balance']*8)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*6)+(self.df['power_stamina']*7)+(self.df['power_strength']*6)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*5)+(self.df['mentality_positioning']*7)+(self.df['mentality_vision']*7)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*7)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*6)+(self.df['attacking_heading_accuracy']*5)+
                    (self.df['attacking_short_passing']*7)+(self.df['attacking_volleys']*6)+(self.df['cam']*7)+(self.df['lam']*7)+(self.df['ram']*7)
                    )/248.8, 5)
            
        elif self.posicao == 'RW':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.4)+(self.df['skill_moves']*0.3)+(self.df['pace']*8)+
                    (self.df['shooting']*6)+(self.df['passing']*6)+(self.df['dribbling']*6)+(self.df['physic']*6)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*5)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*8)+(self.df['movement_sprint_speed']*8)+(self.df['movement_agility']*8)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*6)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*5)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*6)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*6)+(self.df['attacking_heading_accuracy']*5)+
                    (self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*6)+(self.df['rw']*6)
                    )/222.7, 5)
            
        elif self.posicao == 'LW':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.3)+(self.df['skill_moves']*0.3)+(self.df['pace']*8)+
                    (self.df['shooting']*6)+(self.df['passing']*6)+(self.df['dribbling']*7)+(self.df['physic']*6)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*8)+(self.df['movement_sprint_speed']*8)+(self.df['movement_agility']*8)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*6)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*5)+(self.df['mentality_positioning']*6)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*6)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*6)+(self.df['attacking_heading_accuracy']*6)+
                    (self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*6)+(self.df['lw']*6)
                    )/225.6, 5)

        elif self.posicao == 'CF':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.4)+(self.df['skill_moves']*0.4)+(self.df['pace']*8)+
                    (self.df['shooting']*7)+(self.df['passing']*7)+(self.df['dribbling']*7)+(self.df['physic']*6)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*7)+(self.df['skill_fk_accuracy']*6)+(self.df['skill_long_passing']*6)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*8)+(self.df['movement_sprint_speed']*8)+(self.df['movement_agility']*8)+(self.df['movement_reactions']*7)+(self.df['movement_balance']*8)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*6)+(self.df['power_long_shots']*7)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*4)+(self.df['mentality_positioning']*7)+(self.df['mentality_vision']*7)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*7)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*7)+(self.df['attacking_heading_accuracy']*6)+
                    (self.df['attacking_short_passing']*7)+(self.df['attacking_volleys']*6)+(self.df['lf']*7)+(self.df['cf']*7)+(self.df['rf']*7)
                    )/250.8, 5)
            
        elif self.posicao == 'ST':
            self.df['points'] = round(((self.df['overall']*10)+(self.df['potential']*9)+(self.df['weak_foot']*0.4)+(self.df['skill_moves']*0.3)+(self.df['pace']*7)+
                    (self.df['shooting']*7)+(self.df['passing']*6)+(self.df['dribbling']*7)+(self.df['physic']*7)+
                    (self.df['skill_dribbling']*7)+(self.df['skill_curve']*6)+(self.df['skill_fk_accuracy']*5)+(self.df['skill_long_passing']*5)+(self.df['skill_ball_control']*7)+
                    (self.df['movement_acceleration']*7)+(self.df['movement_sprint_speed']*7)+(self.df['movement_agility']*7)+(self.df['movement_reactions']*6)+(self.df['movement_balance']*7)+
                    (self.df['power_shot_power']*7)+(self.df['power_jumping']*7)+(self.df['power_stamina']*7)+(self.df['power_strength']*7)+(self.df['power_long_shots']*6)+
                    (self.df['mentality_aggression']*6)+(self.df['mentality_interceptions']*3)+(self.df['mentality_positioning']*7)+(self.df['mentality_vision']*6)+(self.df['mentality_penalties']*6)+
                    (self.df['mentality_composure']*6)+(self.df['attacking_crossing']*6)+(self.df['attacking_finishing']*7)+(self.df['attacking_heading_accuracy']*6)+
                    (self.df['attacking_short_passing']*6)+(self.df['attacking_volleys']*6)+(self.df['ls']*7)+(self.df['st']*7)+(self.df['rs']*7)
                    )/237.7, 5)

    def jogadores_to_csv(self):
        # saida deve ser ['13052000;8;57', 'id_jogador;valor;pontuacao']
        output = []
        if self.metodo   == 1:
            self.df = self.df[['sofifa_id', 'value_eur', 'points']]
        elif self.metodo == 2:
            self.df = self.df[['sofifa_id','wage_eur', 'points']]
        elif self.metodo == 3:
            self.df = self.df[['sofifa_id','release_clause_eur', 'points']]
        
        self.df.fillna(0, inplace = True)
        for i, row in self.df.iterrows():
            row = row.tolist()
            output.append(f'{row[0]};{row[1]};{row[2]}')
        return output
        
    def exec_combo(self):
        jogadores = self.jogadores_to_csv()
        algorithm = Knapsack_Problem(self.valor)
        result    = algorithm.run(jogadores)
        
        self.df = self.df[~self.df['sofifa_id'].isin(result)]
        
        df_output = self.get_df_output()
        df_filtered = df_output[df_output['sofifa_id'].isin(result)]
        self.df_results.append(df_filtered)
    
    def export_excel(self):
        with pd.ExcelWriter(f'relatorios/relatorio_{self.posicao}.xlsx') as writer: 
            for idx, df in enumerate(self.df_results):
                df.to_excel(writer, sheet_name=f'Combo-{idx+1}', index = False)
