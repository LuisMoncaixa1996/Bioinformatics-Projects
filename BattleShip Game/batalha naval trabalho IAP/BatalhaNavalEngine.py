# -*- coding:utf-8 -*-
'''
Created on 28/10/2019

@author: valves
'''

from copy import deepcopy
import random


class BatalhaNavalEngine:
    
    def __init__(self):
        self.tab_jogo = [] #matriz que representa o tabuleiro de jogo original
        self.tab_estado = [] #matriz que representa o tabuleiro com o estado do jogo
        self.jogador= "top_gun"
        self.score=0 # jogadas efetuadas
        self.undotab = [] # Conjunto de tabuleiros já realizados para o undo
        self.mov = [] # Ordem de jogadas realizada undo
        self.afundado = 0 # contagem de barcos afundados
    
    def ler_tabuleiro_ficheiro(self, filename):
        '''
        Cria nova instancia do jogo numa matriz
        :param filename: nome do ficheiro a ler
        como o formato é fixo sabe-se o que contem cada linha
        '''
        try:
            ficheiro = open(filename, "r")
            lines = ficheiro.readlines() #ler as linhas do ficheiro para a lista lines
            self.tab_jogo=[]
            for i in range(1,11): #as linhas 1 a 11 contêm o tabuleiro de jogo
                self.tab_jogo.append(lines[i].split())
            self.tab_estado=[]
            for i in range(12,22):
                self.tab_estado.append(lines[i].split())
            estado=True
            self.score =int(lines[23])
            self.afundado = int(lines[25])
        except:
            print("Erro: na leitura do tabuleiro")
            estado=False
        else:
            ficheiro.close()
        return estado
    
    def print_tab_jogo(self):
        print("  1 2 3 4 5 6 7 8 9 10")
        letras=['A','B','C','D','E','F','G','H','I','J']
        i=0
        for linha in self.tab_jogo:
            print(letras[i],end=" ")
            i+=1
            for simbolo in linha:
                print(simbolo,end=" ")
            print()
        print("[%s] Jogadas efetuadas:%d"%(self.jogador, self.score))
        
    def print_tab_estado(self):
        print("\n  1 2 3 4 5 6 7 8 9 10")
        letras=['A','B','C','D','E','F','G','H','I','J']
        i=0
        for linha in self.tab_estado:
            print(letras[i],end=" ")
            i+=1
            for simbolo in linha:
                print(simbolo,end=" ")
            print()
        print("[%s] Jogadas efetuadas:%d"%(self.jogador, self.score))

    def setjogador(self,jog):
        '''
        Função que muda o nome do jogador.
        '''
        self.jogador=jog
    
    def getjogador(self):
        '''
        função que devolve o nome do jogador
        '''
        return self.jogador
    
    def gettab_jogo(self):
        '''
      Função que devolve o tabuleiro do jogo
        '''
        return self.tab_jogo
    
    def gettab_estado(self):
        '''
        Função que devolve tabuleiro do estado do jogo
        '''
        return self.tab_estado

    def settab_estado(self, t):
        '''
        função que vai alterar o estado do jogo
        '''
        self.tab_estado = deepcopy(t)
        
    def setscore(self):
        '''
        função que vai aumentar o score +1 sendo este o numero de jogadas
        '''
        self.score = self.score + 1
        
    def setundo_help(self):
        '''
        Função que vai adicionar uma matriz de jogo há nossa lista undotab.
        '''
        self.undotab.append(deepcopy(self.tab_estado))
    
    def settab_jogo(self,k):
        '''
        Função que vai alterar o tabuleiro de jogo
        '''
        self.tab_jogo = deepcopy(k)
        
    def getafundado(self):
        '''
        Função que vai devolver o número de barcos que já foram afundados 
        '''
        return self.afundado
    
    def setafundado(self):
        '''
        função que aumenta o número de barcos afundados
        '''
        self.afundado = self.afundado + 1

    def getundo_help(self):
        '''
        função que devolve o undotab que é a nossa lista de matrizes
        '''
        return self.undotab
    
    def setundo_helpv2(self,mov):
        '''
        Função que vai adicionar a nossa list mov, o movimento que vem associado com a matriz
        '''
        self.mov.append(mov)
        
    def getundo_helpv2(self):
        '''
        Função devolve a lista de jogadas efetuadas
        '''
        return self.mov
     
    def setscore_un(self):
        '''
        Função que diminui o numero do score em -1, utilizada quando se faz o undo de um tiro
        '''
        self.score = self.score - 1
        
    def getscore(self):
        '''
        Função que nos devolve um score
        '''
        return self.score
    
    def check_local(self,x,y,d):
        '''
        Função que rece uma linha uma coluna, e a direção que vai à procura de segmentos de barcos, esta função que vai checkar se o barco que selecionamos se encontra ou não afundado, ele vai correr as posições laterais
        ao tiro onde for dado, se encontrar na tab de jogo um cardinal mas não na tab estado um X, este vai retornar falso,
        ao retornar falso, sabemos que o barco ainda não se encontra afundado, se não retornar falso, ele vai adicionar,
        as linhas e as colunas de todas as posições do barco ao locais e vai dar return dessa lista.
        '''
        locais = [] #lista que vai conter todos as posições que contem barcos já danificados
        if d == 'c':
            l = x - 1
            c = y
            if l > - 1:
                if BatalhaNavalEngine.gettab_estado(self)[l][c] == 'X': #se encontrar a um X inplica que faz parte do barco, e vai correr a função again em todas as direções exepto a direção contrária donde veio para não criar um loop infinito
                    locais.append((l,c))
                    OV = BatalhaNavalEngine.check_local(self,l,c,'c')
                    OV1 = BatalhaNavalEngine.check_local(self,l,c,'e')
                    OV2 = BatalhaNavalEngine.check_local(self,l,c,'d')
                    if OV == False or OV1 == False or OV2 == False:
                        return False
                    else:
                        locais.extend(OV)
                        locais.extend(OV1)
                        locais.extend(OV2)
                elif BatalhaNavalEngine.gettab_estado(self)[l][c] == '.' and BatalhaNavalEngine.gettab_jogo(self)[l][c] == '#':
                    return False
                # Se nenhuma destas condições acontecer vai quebrar o ciclo, fazendo com que este vá devolver a nossa lista locais
                
        elif d == 'b':
            l = x +1
            c = y
            if l <= 9:
                if BatalhaNavalEngine.gettab_estado(self)[l][c] == 'X':
                    locais.append((l,c))
                    OV = BatalhaNavalEngine.check_local(self,l,c,'b')
                    OV1 = BatalhaNavalEngine.check_local(self,l,c,'e')
                    OV2 = BatalhaNavalEngine.check_local(self,l,c,'d')
                    if OV == False or OV1 == False or OV2 == False:
                        return False
                    else:
                        locais.extend(OV)
                        locais.extend(OV1)
                        locais.extend(OV2)
                elif BatalhaNavalEngine.gettab_estado(self)[l][c] == '.' and BatalhaNavalEngine.gettab_jogo(self)[l][c] == '#':
                    return False
        elif d == 'e':
            l = x
            c = y - 1
            if c > -1:
                if BatalhaNavalEngine.gettab_estado(self)[l][c] == 'X':
                    locais.append((l,c))
                    OV = BatalhaNavalEngine.check_local(self,l,c,'c')
                    OV1 = BatalhaNavalEngine.check_local(self,l,c,'e')
                    OV2 = BatalhaNavalEngine.check_local(self,l,c,'b')
                    if OV == False or OV1 == False or OV2 == False:
                        return False
                    else:
                        locais.extend(OV)
                        locais.extend(OV1)
                        locais.extend(OV2)
                elif BatalhaNavalEngine.gettab_estado(self)[l][c] == '.' and BatalhaNavalEngine.gettab_jogo(self)[l][c] == '#':
                    return False
        else:
            l = x 
            c = y + 1
            if c <= 9:
                if BatalhaNavalEngine.gettab_estado(self)[l][c] == 'X':
                    locais.append((l,c))
                    OV = BatalhaNavalEngine.check_local(self,l,c,'c')
                    OV1 = BatalhaNavalEngine.check_local(self,l,c,'b')
                    OV2 = BatalhaNavalEngine.check_local(self,l,c,'d')
                    if OV == False or OV1 == False or OV2 == False:
                        return False
                    else:
                        locais.extend(OV)
                        locais.extend(OV1)
                        locais.extend(OV2)
                elif BatalhaNavalEngine.gettab_estado(self)[l][c] == '.' and BatalhaNavalEngine.gettab_jogo(self)[l][c] == '#':
                    return False
                
        return locais

    def check(self,x,y):
        '''
        Função que vai receber uma cordenada x e y que vau ser a nossa linha e a nossa coluna, e vai correr o nosso,
        check local em todas as direções possíveis, se algum dos alvos, for False, significa que o barco ainda não está
        afundado e sendo assim, esta função tb irá devolver falso, se nenhuma devolver falso significa que o barco já foi
        afundado, vamos adicionar então dar extend a todas as nossas listas prevenientes do check_local, e vamos dar um
        um return dessas listas todas.
        '''
        afundar = []
        alvo_c = BatalhaNavalEngine.check_local(self,x, y, 'c')
        alvo_b = BatalhaNavalEngine.check_local(self,x, y, 'b')
        alvo_e = BatalhaNavalEngine.check_local(self,x, y, 'e')
        alvo_d = BatalhaNavalEngine.check_local(self,x, y, 'd')
        if alvo_c == False or alvo_b == False or alvo_e == False or alvo_d == False:
            return False
        else:
            afundar.extend(alvo_c)
            afundar.extend(alvo_b)
            afundar.extend(alvo_e)
            afundar.extend(alvo_d)
        return afundar
    
    def gerar_random(self):
        '''
        Função que vai devolver uma linha aleatória uma coluna aleatória e um posição esquerda, direita, cima, baixo
        aleatória.
        '''
        linhas = [0,1,2,3,4,5,6,7,8,9]
        colunas = [0,1,2,3,4,5,6,7,8,9]
        posicao = ['e','d','c','b']
        return random.choice(linhas), random.choice(colunas), random.choice(posicao)
    
    def porta_avioes(self):
        '''
        Função que vai adicionar o nosso porta aviões á nossa matriz, primeiro vai as nossas condições da função
        gerar_random, depois com essas condições dependendo da direção vai gerar aleatóriamente outra direção,
        se for impossível o nosso barco encaixar na nossa matriz, este vai correr a função do porta_aviões outra vez,
        e o gerer_random outra vez, até este conseguir encontrar uma posição possível para  o nosso porta avoões encaixar,
        e se assim o fizer vai adicionar este barco a nossa matriz.
        '''
        posicao = BatalhaNavalEngine.gerar_random(self) #vai gerar random a linha, coluna e posição
        linha = posicao[0]
        coluna = posicao[1]
        if posicao[2] == 'e' or 'd':
            orientacao = ['c','b'] #vai gerar outra posição, pois o porta aviões como é em T, tem 2 direções possíveis.
            local = random.choice(orientacao)
            if local == 'c':
                if posicao[2] == 'e':
                    if posicao[0] < 2 or posicao[1] < 2: #se esta não caber na matriz, ela irá correr a função de novo
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna-1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna-2] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna-1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-2][coluna-1] = '#'
                else:
                    if posicao[0] < 2 or posicao[1] > 7:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna+1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna+2] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna+1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-2][coluna+1] = '#'
            else:
                if posicao[2] == 'e':
                    if posicao[0] > 7 or posicao[1] < 2:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna-1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna-2] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna-1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+2][coluna-1] = '#'
                else:
                    if posicao[0] > 7 or posicao[1] > 7:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna+1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna+2] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna+1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+2][coluna+1] = '#'
        else:
            ori = ['e','d']
            l = random.choice(ori)
            if l == 'e':
                if posicao[2] == 'c':
                    if posicao[0] < 2 or posicao[1] < 2:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-2][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna-1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna-2] = '#' 
                else:
                    if posicao[0] > 7 or posicao[1] < 2:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+2][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna-1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna-2] = '#' 
            else:
                if posicao[2] == 'c':
                    if posicao[0] < 2 or posicao[1] > 7:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-2][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna+1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha-1][coluna+2] = '#' 
                else:
                    if posicao[0] > 7 or posicao[1] > 7:
                        BatalhaNavalEngine.porta_avioes(self)
                    else:
                        BatalhaNavalEngine.gettab_jogo(self)[linha][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+2][coluna] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna+1] = '#'
                        BatalhaNavalEngine.gettab_jogo(self)[linha+1][coluna+2] = '#'
                        
    def check_boat(self,c,pos):
        '''
        Função que recebe o comprimento do barco, e uma lista que contêm uma linha, uma coluna e a direção,
        esta função vai ver se na posição linha e coluna e movendo na direção c movimentos se este entra em conflico
        com algum barco já presente no nosso tabbuleiro de jogo, se estiver em conflito, ou o barco não couber na nossa matriz vai retornar falso,
        se nenhuma destas condições acontecer vai dar True e indicar que o barco pode ser desenhado a partir da linha coluna
        no sentido daquela direção c movimentos.
        '''
        for x in range(c):
            if pos[2] == 'c':
                if pos[0] < c-1:#vai checkar se o barco vai para fora da matriz
                    return False
                else:
                    if pos[0]-1-x < 0:#vai ver se o barco se encontra nas extremidades da nossa matriz
                        if pos[1]-1 < 0:
                            for k in range(pos[0]-x,pos[0]+2-x):
                                for j in range(pos[1],pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#': #vai checkar se em qualquer formato de quadrado estiver algum elemento de barco vai dar falso
                                        return False
                        elif pos[1]+1 > 9:
                            for k in range(pos[0]-x,pos[0]+2-x):
                                for j in range(pos[1]-1,pos[1]+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-x,pos[0]+2-x):
                                for j in range(pos[1]-1,pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    elif pos[0]+1-x > 9:
                        if pos[1]-1 < 0:
                            for k in range(pos[0]-1-x,pos[0]-x+1):
                                for j in range(pos[1],pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1 > 9:
                            for k in range(pos[0]-1-x,pos[0]-x+1):
                                for j in range(pos[1]-1,pos[1]+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1-x,pos[0]-x+1):
                                for j in range(pos[1]-1,pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    else:
                        if pos[1]-1 < 0:
                            for k in range(pos[0]-1-x,pos[0]+2-x):
                                for j in range(pos[1],pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1 > 9:
                            for k in range(pos[0]-1-x,pos[0]+2-x):
                                for j in range(pos[1]-1,pos[1]+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1-x,pos[0]+2-x):
                                for j in range(pos[1]-1,pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    
            elif pos[2] == 'b':
                if pos[0] > 9-c+1:
                    return False
                else:
                    if pos[0]-1+x < 0:
                        if pos[1]-1 < 0:
                            for k in range(pos[0]+x,pos[0]+2+x):
                                for j in range(pos[1],pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1 > 9:
                            for k in range(pos[0]+x,pos[0]+2+x):
                                for j in range(pos[1]-1,pos[1]+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]+x,pos[0]+2+x):
                                for j in range(pos[1]-1,pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    elif pos[0]+1+x > 9:
                        if pos[1]-1 < 0:
                            for k in range(pos[0]-1+x,pos[0]+x+1):
                                for j in range(pos[1],pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1 > 9:
                            for k in range(pos[0]-1+x,pos[0]+x+1):
                                for j in range(pos[1]-1,pos[1]+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1+x,pos[0]+x+1):
                                for j in range(pos[1]-1,pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    else:
                        if pos[1]-1 < 0:
                            for k in range(pos[0]-1+x,pos[0]+2+x):
                                for j in range(pos[1],pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1 > 9:
                            for k in range(pos[0]-1+x,pos[0]+2+x):
                                for j in range(pos[1]-1,pos[1]+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1+x,pos[0]+2+x):
                                for j in range(pos[1]-1,pos[1]+2):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    
            elif pos[2] == 'e':
                if pos[1] < c-1:
                    return False
                else:
                    if pos[0]-1 < 0:
                        if pos[1]-1-x < 0:
                            for k in range(pos[0],pos[0]+2):
                                for j in range(pos[1]-x,pos[1]+2-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1-x > 9:
                            for k in range(pos[0],pos[0]+2):
                                for j in range(pos[1]-1-x,pos[1]-x+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0],pos[0]+2):
                                for j in range(pos[1]-1-x,pos[1]+2-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    elif pos[0]+1 > 9:
                        if pos[1]-1-x < 0:
                            for k in range(pos[0]-1,pos[0]+1):
                                for j in range(pos[1]-x,pos[1]+2-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1-x > 9:
                            for k in range(pos[0]-1,pos[0]+1):
                                for j in range(pos[1]-1-x,pos[1]-x+1):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1,pos[0]+1):
                                for j in range(pos[1]-1-x,pos[1]+2-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    else:
                        if pos[1]-1-x < 0:
                            for k in range(pos[0]-1,pos[0]+2):
                                for j in range(pos[1]-x,pos[1]+2-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1-x > 9:
                            for k in range(pos[0]-1,pos[0]+2):
                                for j in range(pos[1]-1-x,pos[1]+1-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1,pos[0]+2):
                                for j in range(pos[1]-1-x,pos[1]+2-x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    
            else:
                if pos[1] > 9-c+1:
                    return False
                else:
                    if pos[0]-1 < 0:
                        if pos[1]-1+x < 0:
                            for k in range(pos[0],pos[0]+2):
                                for j in range(pos[1]+x,pos[1]+2+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1+x > 9:
                            for k in range(pos[0],pos[0]+2):
                                for j in range(pos[1]-1+x,pos[1]+1+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0],pos[0]+2):
                                for j in range(pos[1]-1+x,pos[1]+2+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    elif pos[0]+1 > 9:
                        if pos[1]-1+x < 0:
                            for k in range(pos[0]-1,pos[0]+1):
                                for j in range(pos[1]+x,pos[1]+2+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1+x > 9:
                            for k in range(pos[0]-1,pos[0]+1):
                                for j in range(pos[1]-1+x,pos[1]+1+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1,pos[0]+1):
                                for j in range(pos[1]-1+x,pos[1]+2+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                    else:
                        if pos[1]-1+x < 0:
                            for k in range(pos[0]-1,pos[0]+2):
                                for j in range(pos[1]+x,pos[1]+2+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        elif pos[1]+1+x > 9:
                            for k in range(pos[0]-1,pos[0]+2):
                                for j in range(pos[1]-1+x,pos[1]+1+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
                        else:
                            for k in range(pos[0]-1,pos[0]+2):
                                for j in range(pos[1]-1+x,pos[1]+2+x):
                                    if BatalhaNavalEngine.gettab_jogo(self)[k][j] == '#':
                                        return False
    
        return True
        
    def outros_boats(self,c):
        '''
        Função que recebe o comprimento do barco, vai usar a função gerar_random, para dar uma coluna, linha e direção aleatória,
        depois irá correr a função check_boat, para ver se o barco pode ser posicionado na nossa matriz, se esta função devolver
        falso vai voltar a correr a função outros_boats, sabendo que o C é o mesmo, se a função devolver True, vai ver em que
        direção é para desenhar o barco, e vai adiciona-lo a nossa matriz estado do jogo.
        '''
        pos = BatalhaNavalEngine.gerar_random(self)
        valid = BatalhaNavalEngine.check_boat(self,c, pos)
        if valid == False:
            BatalhaNavalEngine.outros_boats(self,c)
        else:
            if pos[2] == 'c':
                for k in range(c):
                    BatalhaNavalEngine.gettab_jogo(self)[pos[0]-k][pos[1]] = '#'
            elif pos[2] == 'b':
                for k in range(c):
                    BatalhaNavalEngine.gettab_jogo(self)[pos[0]+k][pos[1]] = '#'
            elif pos[2] == 'e':
                for k in range(c):
                    BatalhaNavalEngine.gettab_jogo(self)[pos[0]][pos[1]-k] = '#'
            else:
                for k in range(c):
                    BatalhaNavalEngine.gettab_jogo(self)[pos[0]][pos[1]+k] = '#'
                        
    def matriz_jogo(self):
        '''
        Função que vai criar uma matriz e devolver esta mesma.
        '''
        matriz = []
        for i in range(10):
            linha = []
            for j in range(10):
                linha.append('.')
            matriz.append(linha)
        return matriz