# Alunos:
# João Pedro Pilastri Terruel - 11812584
# Victor Pereira Moura - 11836160

# -*- coding: utf-8 -*-
''' ErgoHomeApp.PY
    
    Realiza a análise ergonômica do ambiente
    Inputs: argv[1] = nome_imagem.png
            argv[2] = tamanho da tela, em polegadas
            argv[3] = resolução horizontal da tela, em pixels
            argv[4] = rresolução vertical da tela, em pixels
   
    Na segunda figura, clique na diagonal do monitor:
    Referencias monitor ('0 0     ;   0')
                       ('esq-supe       dir-inf')
                                                           horiz  vert
    Exemplo para rodar:  python ErgoHomeApp.py teste1.png 22 1920 1080
'''
import Core
import sys
import math
import numpy as np
from numpy import linalg as LA
from numpy.linalg import inv
import matplotlib.pyplot as plt
from matplotlib.image import imread
#######################################################
######### Get image pixel x, y by ginput ##############
#######################################################

#ta pronto
def getCoordenadasPixel(img, titleinstruc=None):
    if titleinstruc is None:
        titleinstruc = 'MOUSE - botão ESQUERDO: marcar | DIREITO: parar | DO MEIO: desmarcar '
    
    plt.imshow(img)
    plt.title(titleinstruc)
    plt.xlabel(
        'MOUSE - botão ESQUERDO: marcar | DIREITO: parar | DO MEIO: desmarcar ')
    pxy = plt.ginput(n=50, timeout=0, mouse_stop=3, mouse_pop=2)
    pxy = np.matrix(pxy)
    
    return pxy

#################################################################
############### Function to calc pixel em cm ####################
#################################################################
def tamanhoPixelEmCentimetros(tamanhoMonitor, L):
    '''
    Create DLT2D
    - tamanhoMonitor tamanho do monitor em cm
         
    - L  matrix containing 2d coordinates of calibration 
         points seen in camera 
         e.g.: np.matrix('1200 1040; 1200 1360')
         valores que vem de onde o cara clica da imagem
'''
    F = tamanhoMonitor*2.54
    L = np.matrix(L)
    distempx=math.sqrt(((L[0,0]-L[1,0])**2)+((L[0,1]-L[1,1])**2))
    valorpxcm=F/distempx    
    
    return valorpxcm 

##############################################################
############### Function to calc distance#####################
##############################################################
def calcdist(valpx, cc2d):

    L = np.matrix(cc2d)
    distanciaEmPixels = math.sqrt(((L[0,0]-L[1,0])**2)+((L[0,1]-L[1,1])**2))
    distanciaEmCentimetros = distanciaEmPixels*valpx
    return distanciaEmCentimetros

#######################################################
############### MAIN FUNCTION #########################
#######################################################
def main():
    if sys.argv[1] == "-h":
        print(''' 
ErgoHomeApp.PY
    Realiza a análise ergonômica do ambiente
    Inputs: argv[1] = nome_imagem.png
        argv[2] = tamanho da tela, em polegadas
        argv[3] = resolução horizontal da tela, em pixels
        argv[4] = rresolução vertical da tela, em pixels
    Na segunda figura, clique na diagonal do monitor:
    Referencias monitor ('0 0     ;   0')
                        ('esq-supe       dir-inf')
                                                             horiz vert
    Exemplo para rodar:  python ErgoHomeApp.py teste1.png 22 1920 1080
        ''')
        return
    
    if len(sys.argv) != 5:
        print('Argumentos inválidos! ')
        print("Como usar: python ErgoHomeApp.py imagem tamanho_monitor resolucao_horizontal resolucao_vertical")
        return

    # Define global (real)  references
    resolucaoHorizontal = int(sys.argv[3])
    resolucaoVertical = int(sys.argv[4])
    tamanhoMonitor = float(sys.argv[2]) # size of monitor screen 
    resolucao = Core.Resolucao(resolucaoHorizontal, resolucaoVertical)
    monitor = Core.Monitor(tamanhoMonitor, resolucao)
    monitor.sumario()

    img = imread(sys.argv[1]) # read image png
    title2calib = 'Marque os pontos: superior-direito; inferior-esquerdo do monitor'
    pixcal = getCoordenadasPixel(img, title2calib)
    plt.close()
    tamanhoPixelEmCm = tamanhoPixelEmCentimetros(tamanhoMonitor, pixcal) # envia tamanho do monitor junto com os pontos pegos na imagem, e retorna o valor de um px em cm
    
    titlefree = 'Por favor selecione a posição dos olhos e a parte central do monitor' # selecionar os olhos e a parte central do monitor
    cc2d = getCoordenadasPixel(img, titlefree) 
    distcabe = calcdist(tamanhoPixelEmCm, cc2d)
    distcab= distcabe*(math.sqrt(2)/2)
    
    
    print("Distância da cabeça: ", distcab)
    Core.Info.distanciaCabecaMonitor(distcab, monitor)
    titlefree = 'Por favor selecione o topo do joelho e a base dos pés'#selecionar o topo do joelho e a base dos pés
    cc2d = getCoordenadasPixel(img, titlefree) 
    distkneefloor=calcdist(tamanhoPixelEmCm, cc2d)
    distfloorknee= distkneefloor*(math.sqrt(2)/2)
    Core.Info.alturaJoelhoChao(distfloorknee)
    
    return distcab, distfloorknee

#######################################################
#####################  RUN MAIN CODE ##################
#######################################################
if __name__ == '__main__':
    main()
