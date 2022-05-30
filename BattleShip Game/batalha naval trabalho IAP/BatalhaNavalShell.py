# -*- coding:utf-8 -*-
'''
Created on 28/10/2019

@author: valves
'''
from cmd import *
from BatalhaNavalWindow import BatalhaNavalWindow
from BatalhaNavalEngine import BatalhaNavalEngine
import random

class BatalhaNavalShell(Cmd):
    intro = 'Interpretador de comandos para a Batalha Naval adaptada. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'BatalhaNaval> '
    
     
    
                               
    def do_jogar(self, arg):
        " -  comando jogar que leva como parâmetro o nome de um ficheiro e a identificação do jogador e carrega o tabuleiro permitindo jogá-lo..: jogar <nome_ficheiro> <jogador> \n" 
        
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 2:
                eng.ler_tabuleiro_ficheiro(lista_arg[0])
                eng.setjogador(lista_arg[1])
                #eng.print_tab_jogo()
                eng.print_tab_estado()
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao mostrar o puzzle")
            
    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro e permite gravar o estado do jogo atual..: gravar <nome_ficheiro>  \n"
        '''
        Função responsável por gravar o jogo atual de jogo, escrevendo num ficheiro novo,
        onde na primeira linha mete Tabuleiro, depois vai escrever a matriz do tabuleiro de jogo
        linha por linha, e depois vai dar print do Estado do Jogo, de sequida coma matriz do estado jogo,
        e no fim as Jogadas efetuadas, e onúmero de jogadas realizadas.
        
        '''
        def matrix_to_string(matriz):
            '''
            Função responsável por transformar uma matriz em strings por linhas.
            '''
            matriz_string = ''
            for l in matriz:
                matriz_string += ' '.join(l) + '\n'
            return matriz_string
        
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                save = open(arg, 'w') #Função responsável por abrir um ficheiro de escirta onde arg é o nome do ficheiro
                save.writelines('Tabuleiro:\n')
                save.writelines(matrix_to_string(eng.gettab_jogo()))
                save.writelines('Estado do Jogo:\n')
                save.writelines(matrix_to_string(eng.gettab_estado()))
                save.writelines('Jogados efetuadas:\n')
                save.writelines(str(eng.getscore()))
                save.writelines('\nBarcos Afundados: \n')
                save.writelines(str(eng.getafundado()))
                save.close()
                print('Jogo gravado com Sucesso')
                
            else:
                print('Número de argumentos é inválido')
        except:
            print('Erro: ao gravar o ficheiro')
    
    def do_tiro(self, arg):    
        " - comando tiro que leva como parâmetros a linha e a coluna de uma casa onde se pretende jogar..: tiro <l> <c>\n"
        '''
        Função responsável por receber 2 posições, uma linha e uma coluna, com esses dois argumentos vai ver se no
        nosso tabuleiro estado, se a jogada já foi realizada ou não, se não tiver sido realizada vai à função do
        tabuleiro de jogo ver se acertou num barco ou não, se acertar vai fazer as suas substituições, se for fogo,
        o programa vai correr a função check do engine, para ver se o barco em qual acertou está afundado ou não se,
        vai alterar os valores nas matrizes, depois de afundar os barcos vai guardar o nome do jogador e o seu score
        no ficheiro de score.
        '''
        
        try:
            linhas = ['A','B','C','D','E','F','G','H','I','J']
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 2:
                eng.setundo_help() #Explicado em agua
                eng.setundo_helpv2('tiro') #explicadp em agua
                if eng.gettab_estado()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] != '.':
                    print('Comando já realizado tente outra vez!')
                else:
                    if eng.gettab_jogo()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] == '#':
                        print('FOGO!!!!!!!')
                        eng.gettab_estado()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] = 'X'
                        eng.setscore()
                        alvo = eng.check(linhas.index(lista_arg[0]),int(lista_arg[1])-1)
                        if alvo == False:
                            pass
                        else:
                            eng.setafundado()
                            eng.gettab_estado()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] = '*'
                            for i in alvo:
                                (x,y) = i
                                eng.gettab_estado()[x][y] = '*'
                            print('PARABÉNS!! BARCO AFUNDADO!')
                            if eng.getafundado() == 8:
                                print('Todos os barcos afundados! Você venceu!')
                                savescore = open('Scores.txt', 'a')
                                savescore.writelines(eng.getjogador())
                                savescore.writelines(': ')
                                savescore.writelines(str(eng.getscore()))
                                savescore.writelines('\n')
                                savescore.close()
                                print('Para ver o score execute o comando')
                    else:
                        print('Água!')
                        eng.gettab_estado()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] = 'O'
                        eng.setscore()
                    eng.print_tab_estado()
                                
            else:
                print('Número de argumentos inválido')
        except:
            print('Erro: no canhão mande tiro outra vez!')
                 
    def do_agua(self, arg):    
        " - comando que leva como parâmetros a linha e a coluna de uma casa, pertencente a uma embarcação já afundada (totalmente descoberta) que se pretende rodear de “água”..: agua <l> <c> \n"
        '''
        Função que recebe 2 argumentos 1 da posição linha e outro da coluna, para verificar se nessa posição no tabuleiro jogo é água,
        ou não, se for água marca na matriz água, se não for vai indicar que perdeu o jogo, e depois vai pedir, ao
        jogador se quer fazer undo na jogada, ou sair do batalha Naval. Fechando a Batalha Naval se quiser sair, ou
        continuando a jogar se fizer o undo. A função não rodea a embarcação de água, devido ao facto de entrar mos em contacto
        com o professor e este dizer que a função teria de servir como o tiro, mas que não contava como jogadas.
        '''
        try:
            linhas = ['A','B','C','D','E','F','G','H','I','J']
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 2:
                eng.setundo_help() # Função responsável por gravar a matriz anted de realizar a água
                eng.setundo_helpv2('água') # Função responsável por gravar o tipo de jogada que foi realizada
                if eng.gettab_estado()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] != '.':
                    print("Coordenada já foi escolhida, escolha outra")
                elif eng.gettab_jogo()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] == '.':
                    eng.gettab_estado()[linhas.index(lista_arg[0])][int(lista_arg[1])-1] = 'O'
                    print('Água!!')
                    eng.print_tab_estado()
                    
                else:
                    print('Acertou num barco, perdeu o jogo!')
                    while True:
                        x = input('Press 1 se tenciona abandonar a partida, Press 2 se tenciona fazer undo na sua jogada!: ')
                        if x.isdigit(): #decomentado na função linha
                            x = int(x)
                            if x == 1:
                                return True # Se uma função der return True a Shell vai fechar
                                
                            elif x == 2:
                                sh.do_undo('') #Função decomentada na linha!
                            else:
                                print(' Insira o número 1 ou 2')
                        else:
                            print('Insira um Número') 
    
            else:
                print('Número de argumentos inválido')
        except:
            print('Erro: A agua secou!')

    def do_linha(self, arg):    
        " - comando linha que permite colocar o estado de todas as casas da linha l que ainda não estão determinadas como sendo “água”...: linha <l> \n"
        '''
        Função que rece 1 argumento, que é a linha alvo, e vai todas as posições de uma linha em água, se encontrar um
        barco não o vai fazer, se esse barco já tiver sido sofrido dano ('FOGO' ou 'AFUNDADO'), ela simplesmente vai,
        ignorar essa posição, se encontrar um elementento de brago que ainda não tenha sofrido Dano, a pessoa perde o jogo,
        e o jogo vai perguntar a pessoa se ela quer fazer undo da jogada ou se quer sair do jogo.
        '''
        try:
            linhas = ['A','B','C','D','E','F','G','H','I','J']
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                eng.setundo_help()
                eng.setundo_helpv2('água')
                l = False # identificador para dar brake ao ciclo for depois de realizar o undo.
                for i in range(10):
                    if l == True:
                        break
                    else:
                        if eng.gettab_jogo()[linhas.index(lista_arg[0])][i] == '#':
                            if eng.gettab_estado()[linhas.index(lista_arg[0])][i] == '*' or eng.gettab_estado()[linhas.index(lista_arg[0])][i] == 'X' :
                                pass
                            else:
                                print ('You Lose!!!')
                                while True:
                                    x = input('Press 1 se tenciona abandonar a partida, Press 2 se tenciona fazer undo na sua jogada!: ')
                                    if x.isdigit(): #Função responsável para saber se x é uma string numérica ou não. 
                                        x = int(x)
                                        if x == 1:
                                            return True
                                        
                                        elif x == 2:
                                            sh.do_undo('') #Função responsável para fazer o undo da jogada depois de esta dar como jogo perdido.
                                            l = True
                                            break
                                            
                                        else:
                                            print(' Insira o número 1 ou 2')
                                    else:
                                        print('Insira um Número')
                        else:
                            eng.gettab_estado()[linhas.index(lista_arg[0])][i] = 'O'
                eng.print_tab_estado()
            else:
                print('nº de argumentos invalido')
        except:
            print('Erro: Try again')
                    
    def do_coluna(self, arg):    
        " - comando coluna que permite colocar o estado de todas as casas da coluna c que ainda não estão determinadas como sendo “água”...: coluna <c> \n"
        '''
        Função que recebe um argumento que é o número da coluna, e realiza o mesmo  processo que realiza a função linha.
        '''
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                eng.setundo_help()
                eng.setundo_helpv2('água')
                l = False
                for i in range(10):
                    if l == True:
                        break
                    if eng.gettab_jogo()[i][int(lista_arg[0])-1] == '#':
                        if eng.gettab_estado()[i][int(lista_arg[0])-1] == '*':
                            pass
                        else:
                            print ('You lose!!')
                            while True:
                                    x = input('Press 1 se tenciona abandonar a partida, Press 2 se tenciona fazer undo na sua jogada!: ')
                                    if x.isdigit(): #Função responsável para saber se x é uma string numérica ou não. 
                                        x = int(x)
                                        if x == 1:
                                            return True
                                        
                                        elif x == 2:
                                            sh.do_undo('') #Função responsável para fazer o undo da jogada depois de esta dar como jogo perdido.
                                            l = True  
                                            break
                                        else:
                                            print(' Insira o número 1 ou 2')
                                    else:
                                        print('Insira um Número')
                    else:
                        eng.gettab_estado()[i][int(lista_arg[0])-1] = 'O'
                eng.print_tab_estado()
            else:
                print('nº de argumentos invalido')
        except:
            print('Erro: Try again')
            
    def do_ajuda(self, arg):    
        " - comando ajuda que indica por linha e por coluna a quantidade de segmentos de barco existentes nessa linha/coluna..: ajuda  \n"
        '''
        funçaõ que recebe 0 argumentos, esta função vai correr todos os elementos do nosso tabuleiro de jogo,
        e fazer uma contagem de elemtos de barco por linha e por coluna, devolvendo um print em linha das linhas: e o
        numero de elementos dos barcos, e as colunas: e o numero de elementos dos barcos. Se utilizar esta função irá
        aumentaro número de jogada em 2 pois é uma ajuda.
        '''
        try:
            linhas = ['A','B','C','D','E','F','G','H','I','J']
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 0:
                for i in range(10):
                    count = 0 # serve para realizar a contagem de elementos nas linhas
                    for k in range (10):
                        if eng.gettab_jogo()[i][k] == '#':
                            count = count + 1        
                    print(linhas[i],':',count) # dá o print das linhas
                for j in range(10):
                    countc = 0# serve para realizar a contagem de elementos nas colunas
                    for l in range(10):
                        if eng.gettab_jogo()[l][j] == '#':
                            countc = countc + 1
                    print(j+1,':',countc) # dá o print das colunas
                for m in range(2):
                    eng.setscore()
            else:
                print('nº de argumentos invalido')
        except:
            print('Erro: Try again')

    def do_undo(self, arg):    
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        '''
        Função que recebe 0 argumentos, vau usar o getundo_help para ir buscar uma lista de matrizes,
        que vai conter as matrizes anted de ocorrer todas as jogadas realizada no jogo, se resolver uma lista vazia,
        implica que não ouve jogadas realizadas ainda, se devolver algo na lista, vai fazer o undo da ultima jogada
        realizada, buscando o getundohelpv2 que é uma função que tem guatdado o nome das jogadas realizadas, se a jogada
        for um tiro vai retirar um ponto se não for vai fazer undo mas não retira pontos.
        '''
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 0:
                if eng.getundo_help() == []:
                    print('Jogadas ainda não realizadas!')
                else:
                    x = eng.getundo_helpv2() #Buscar a lista de jogadas realizadas
                    y = eng.getundo_help() # Buscar a lista de tabuleiros
                    f = len(y) #Número de jogadas já efetuadas desde o início do jogo
                    if x[f-1] == 'tiro':
                        eng.setscore_un() # retirar uma jogada
                        eng.settab_estado(y[f-1]) #vai meter a matriz de estado de jogo igual á ultima na lista do undo das matrizes
                        y.remove(y[f-1]) # vai remover a nosso ultimo elemento da lista de undo das matrizes
                        x.remove(x[f-1]) # vai remover o nome da ultima jogada efetuada
                        print('Undo Realizado')
                    else:
                        eng.settab_estado(y[f-1])
                        print('Undo Realizado')
                        y.remove(y[f-1])
                        x.remove(x[f-1])
                    eng.print_tab_estado()
            else:
                print('Numero de argumentos invalido')
        except:
            print('Erro: Try again')
        
    def do_bot(self, arg):    
        " - comando bot para apresentar a sequência de jogadas ótimas para terminar o jogo: bot \n"
        '''
        Função que recebe 0 argumentos e vai correr a nossa matriz de jogo e ver se existe um segmento de
        barco que não foi danificado e dá print dessa linha e dessa coluna onde se encontra este segmento,
        esta função aumenta o número de jogadas em 5 devido ao facto de ser uma ajuda
        '''
        try:
            linhas = ['A','B','C','D','E','F','G','H','I','J']
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 0:
                l = False
                for i in range(10):
                    for j in range(10):
                        if eng.gettab_jogo()[i][j] == '#':
                            if eng.gettab_estado()[i][j] != 'X' and eng.gettab_estado()[i][j] != '*':
                                print((linhas[i],j+1))
                                l = True #condição para ver se foi dado print
                                break
                    if eng.gettab_jogo()[i][j] == '#':        
                        if eng.gettab_estado()[i][j] != 'X' and eng.gettab_estado()[i][j] != '*':        
                            break
                if l == False:
                    print('Não existem mais segmentos de barco para afundar')
                for m in range(5):
                    eng.setscore()
            else:
                print('argumentos invalidos')
        
        except:
            print('Erro: Try again')
            
    def do_gerar(self, arg):    
        " - comando gerar que gera tabuleiros validos..: gerar \n"
        '''
        Função que recebe 0 argumentos, e usando funções do engine como porta_aviões e outros_boats e vai gerar um
        tabuleiro de jogo e um taboleiro de estado, e depois irá perguntar qual o nome do jogador, se quiser guardar
        o tabuleiro pressa o comando gravar. O tabuleiro gerado irá ter os barcos posicionados com todas as regras necessárias
        de maneira random!
        '''
  
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 0:
                eng.settab_estado(eng.matriz_jogo()) #vai gerar a mtriz de estado de jogo só com pontos
                eng.settab_jogo(eng.matriz_jogo()) #vai gerar a mtriz de tabuleiro de jogo só com pontos
                eng.porta_avioes() # vai meter o porta aviões na nossa matriz de tabuleiro de jogo
                eng.outros_boats(4)# vai meter o barco de 4 na nossa matriz de tabuleiro de jogo tando este sempre a uma casa de distancia minima dos nossos barcos
                eng.outros_boats(3)# vai meter o barco de 3 na nossa matriz de tabuleiro de jogo tando este sempre a uma casa de distancia minima dos nossos barcos
                for i in range(2):
                    eng.outros_boats(2)# vai meter o barco de 2 na nossa matriz de tabuleiro de jogo tando este sempre a uma casa de distancia minima dos nossos barcos
                for j in range(3):
                    eng.outros_boats(1)# vai meter o barco de 1 na nossa matriz de tabuleiro de jogo tando este sempre a uma casa de distancia minima dos nossos barcos
                x = input('Selecione o seu nome de jogador: ')
                eng.setjogador(x)# vai inserir o nome do jogador
                print('Se quiser guardar o tabuleiro pressione o comando Gravar!')
                #eng.print_tab_jogo()
                eng.print_tab_estado()
            else:
                print('argumentos invalidos')
        except:
                print('Erro: Try again')
                   
    def do_score(self, arg):    
        " - comando score que permite ver o registo ordenado dos scores dos jogadores..: \n"
        '''
        função que recebe 0 argumentos, e que vai ser responável de devolver um top de 10 jogadores,
        onde irá ter a sua posição, e o nome do jogador sequido do seu score, quanto mais baixo o score,
        melhor será o jogador, esta função vai ler o nosso ficheiro score.txt vai adicionar todos os jogadores,
        a um dicionário, sendo o seu nome a key e o score o value, se ouverem jogadores com o mesmo nome do ficheiro este
        irá buscar o score melhor dos jogadores.
        '''
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 0:
                scores = open('Scores.txt','r').readlines() #vai ler todas as linhas do nosso ficheiro
                rank = ' '.join(scores)# vai juntar tudo numa string, separado por espaços
                ranking = rank.split()# vai dividir tudo numa lista
                ranked = {}
                for i in range(0,len(ranking),2):# vai correr o nome dos jogadores
                    if ranking[i] in ranked: #vai ver se eles já se encontram no dicionário
                        x = ranked.get(ranking[i])# vai ver qual é o score do jogador se ele já tiver no dicionário
                        if x > int(ranking[i+1]): #e vai ver se o score é menor do que o do dicionário se for vai acicionar esse novo valor ao dicionário
                            ranked[ranking[i]] = int(ranking[i+1])
                    else:
                        ranked[ranking[i]] = int(ranking[i+1])
                k = len(ranked)
                if k == 0: #se não ouver nada no ficheiro vai indicar que não existem scores guardados ainda
                    print('Erro: Não existem scores')
                else:
                    l = 0               
                    for item in sorted(ranked, key = ranked.get): # vai organizar os scores por value
                        print (l+1,'- ', item, ranked[item]) # e vai dar print dos melhores 10
                        l = l +1
                        if l == 10:
                            break
            else: 
                print('argumentos invalidos')
        except:
                print('Erro: Try again')
                
    def do_ver(self, arg):    
        " - Comando para visualizar o estado atual do tabuleiro em ambiente grafico caso seja válido: VER  \n"
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        janela = BatalhaNavalWindow(40) 
        janela.mostraJanela(eng.gettab_estado())        
        
    def do_sair(self, arg):
        "Sair do programa BatalhaNaval: sair"
        print('Obrigado por ter utilizado o BatalhaNaval, espero que tenha sido divertido!')
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
                    del janela  # invoca o metodo destruidor de instancia __del__()
        return True


if __name__ == '__main__':
    eng = BatalhaNavalEngine()
    janela = None
    sh = BatalhaNavalShell()
    sh.cmdloop()
    
'''


'''

