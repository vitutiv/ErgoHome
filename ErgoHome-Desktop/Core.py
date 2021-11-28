# Alunos: 
# João Pedro Pilastri Terruel - 11812584
# Victor Pereira Moura - 11836160
import math
from enum import Enum

class Medida(Enum):
    CM = 1,
    POL = 2

class Info:

    @staticmethod
    def alturaJoelhoChao(distfloorknee):
        dist = (47-distfloorknee)
        if(dist < 0):
            print("A cadeira esta muito alta. Abaixe-a em:", -1 * dist, "cm.")
        elif(dist == 0):
            print("A cadeira está na altura ideal.")
        else:
            print("A cadeira está muito baixa. Suba-a em:", dist, "cm.")

    @staticmethod
    def distanciaCabecaMonitor(distancia, monitor):
        if (distancia < monitor.distanciaMinima()):
            print("O monitor está muito próximo da cabeça.")
        elif (distancia >= monitor.distanciaMinima() and distancia <= monitor.distanciaDeAcuidade()):
            print("O monitor está em uma distância ideal.")
        else:
            print("O monitor está muito longe.")

class Conversor:
    @staticmethod
    def converter(distancia, de=Medida.POL, para=Medida.CM):
        if de == para:
            return distancia
        return distancia * 2.54

class Resolucao:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical

class Monitor:
    resolucao = Resolucao(0, 0)

    def __init__(self, diagonal, resolucao):
        self.diagonal = diagonal
        self.resolucao = resolucao

    def distanciaMinima(self, medida=Medida.CM):
        proporcaoMonitor = self.resolucao.horizontal / self.resolucao.vertical
        distanciaEmPolegadas = (
            self.diagonal / math.sqrt((proporcaoMonitor**2) + 1)) * 1.4
        return Conversor.converter(distanciaEmPolegadas)

    def distanciaDeAcuidade(self, medida=Medida.CM):
        distanciaEmPolegadas = self.diagonal / (math.sqrt(((self.resolucao.horizontal / self.resolucao.vertical)
                                                ** 2) + 1) * self.resolucao.vertical * math.tan(math.pi / 180 / 60))
        return Conversor.converter(distanciaEmPolegadas)

    def sumario(self):
        print("Informações do monitor \n Tamanho:", self.diagonal, "polegadas \n Resolução:", self.resolucao.horizontal, "x", self.resolucao.vertical)

        distanciaMinima = self.distanciaMinima()
        distanciaDeAcuidade = self.distanciaDeAcuidade()

        print(" Distâncias recomendadas: ")

        if distanciaMinima < 100:
            print("  Distância mínima:", round(distanciaMinima), "cm")
        else:
            print("  Distância mínima:", int(distanciaMinima / 100),
                  "m e ", int(distanciaMinima % 100), "cm")

        if distanciaDeAcuidade < 100:
            print("  Distância de acuidade:", int(
                distanciaDeAcuidade), "cm")
        else:
            print("  Distância de acuidade:", int(distanciaDeAcuidade /
                  100), "m,", int(distanciaDeAcuidade % 100), "cm")