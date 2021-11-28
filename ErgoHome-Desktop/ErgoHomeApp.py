# -*- coding: utf-8 -*-
''' ErgoHomeApp.PY
    
    Realiza a análise ergonômica do ambiente
    Inputs: argv[1] = name_image.png
            argv[2] = number of frames from the kick until the ball enters the goal
            argv[3] = resolution horizont of screen
            argv[4] = resolution vertical of screen
   
    Na segunda figura clique na diagonal do monitor:
    Referencias monitor ('0 0     ;   0')
                       ('esq-supe       dir-inf')
                                                           horiz  vert
    Exemplo para rodar:  python ErgoHomeApp.py 1389.png 22 2200 1920
'''

#import os
import Corpo
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
def getcoordspix(img, titleinstruc=None):
    if titleinstruc is None:
        titleinstruc = 'Mouse buttom LEFT: mark | RIGHT: stop | MIDDLE: unmark '
    
    plt.imshow(img)
    plt.title(titleinstruc)
    plt.xlabel('Mouse LEFT: mark | RIGHT: stop | MIDDLE: unmark ')
    pxy = plt.ginput(n=50, timeout=0, mouse_stop=3, mouse_pop=2)
    pxy = np.matrix(pxy)
    
    return pxy


#################################################################
############### Function to calc pixel em cm ####################
#################################################################
def valpixelcm(sizemonitor, L):
    '''
    Create DLT2D
    - sizemonitor tamanho do monitor em cm
         
    - L  matrix containing 2d coordinates of calibration 
         points seen in camera 
         e.g.: np.matrix('1200 1040; 1200 1360')
         valores que vem de onde o cara clica da imagem
'''
    F = sizemonitor*2.54
    L = np.matrix(L)
    distempx=math.sqrt(((L[0,0]-L[1,0])**2)+((L[0,1]-L[1,1])**2))
    valorpxcm=F/distempx    
    
    return valorpxcm 

##############################################################
############### Function to calc distance#####################
##############################################################
def calcdist(valpx, cc2d):

    L = np.matrix(cc2d)
    distinpx = math.sqrt(((L[0,0]-L[1,0])**2)+((L[0,1]-L[1,1])**2))
    distincm = distinpx*valpx
    return distincm

#######################################################
############### MAIN FUNCTION #########################
#######################################################
def main():
    
    # Define global (real)  references
    rh = int(sys.argv[3])
    rv = int(sys.argv[4])
    sizemont = float(sys.argv[2]) # size of monitor screen 
    img = imread(sys.argv[1]) # read image png
    title2calib = 'Mark the points:right-up; left-down of the monitor screen'
    pixcal = getcoordspix(img, title2calib)
    plt.close()
    valpxincm = valpixelcm(sizemont, pixcal)#envia tamanho do monitor junto com os pontos pegos na imagem, e retorna o valor de um px em cm
    
    titlefree = 'Please Mark the eyes and the center of the monitor screen'#selecionar os olhos e a parte central do monitor
    cc2d = getcoordspix(img, titlefree) 
    distcabe = calcdist(valpxincm, cc2d)
    distcab= distcabe*(math.sqrt(2)/2)
    
    resolucao = Core.Resolucao(rh, rv)
    monitor = Core.Monitor(sizemont, resolucao)
    
    print("Distância da cabeça: ", distcab)
    monitor.sumario()
    if (distcab < monitor.distanciaMinima()):
        print("O monitor está muito próximo da cabeça")
    elif (distcab >= monitor.distanciaMinima() and distcab <= monitor.distanciaDeAcuidade()):
        print("O monitor está em uma distância ideal")
    else:
        print("O monitor está muito longe")

    titlefree = 'Please Mark the foot and the knee'#selecionar o topo do joelho e a base dos pés
    cc2d = getcoordspix(img, titlefree) 
    distkneefloor=calcdist(valpxincm, cc2d)
    distfloorknee= distkneefloor*(math.sqrt(2)/2)
    Corpo.altjoch(distfloorknee)
    
    return distcab, distfloorknee

#######################################################
#####################  RUN MAIN CODE ##################
#######################################################
if __name__ == '__main__':
    main()
