#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2,INPUT_3,INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank,SpeedPercent
import time

# declaracao dos sensores
sensor1 = ColorSensor(INPUT_1)  #sensor da esquerda
sensor2 = ColorSensor(INPUT_2)  #sensor da direita
sensor3 = UltrasonicSensor(INPUT_3) #sensor lateral
sensor4 = UltrasonicSensor(INPUT_4) #sensor frontal

#declaracao dos motores
tank = MoveTank(OUTPUT_A,OUTPUT_B)
motorA = LargeMotor(OUTPUT_A)   #motor da esquerda
motorB = LargeMotor(OUTPUT_B)   #motor da direita
motorC = LargeMotor(OUTPUT_C)   #motor da garra

""" FUNCOES """

#90* p/ esquerda com 1 motor // x e a quantidade de rotacoes do motor B
def curva_esquerda(rotacoes, velocidade):
    motorA.stop()
    motorB.on_for_rotations(SpeedPercent(velocidade), rotacoes)
    motorB.stop()

#90* p/ direita com 1 motor // x e a quantidade de rotacoes do motor A
def curva_direita(rotacoes, velocidade):
    motorB.stop()
    motorA.on_for_rotations(SpeedPercent(velocidade), rotacoes)
    motorA.stop()

#90* p/ esquerda com 2 motores // x é a posicao final intencionada do motorA
def curva_esquerdacom2(x, velocidade):
    motorA.reset()
    motorB.reset()
    while motorA.position < x:
        motorA.run_forever(speed_sp = velocidade)
        motorB.run_forever(speed_sp = -velocidade)
    motorA.stop(stop_action = 'hold')
    motorB.stop(stop_action = 'hold')

#90* p/ direita com 2 motores // x é a posicao final intencionada do motorB
def curva_direitacom2(x, velocidade):
    motorA.reset()
    motorB.reset()
    while motorB.position < x:
        motorA.run_forever(speed_sp = -velocidade)
        motorB.run_forever(speed_sp = velocidade)
    motorA.stop(stop_action = 'hold')
    motorB.stop(stop_action = 'hold')

#ajuste em linha de uma cor especifica, um motor de cada vez
def ajuste(cor, direcao):
    while sensor1.color != cor:
        motorA.run_forever(speed_sp = 100 * direcao)
    motorA.stop(stop_action = 'hold')
    while sensor2.color != cor:
        motorB.run_forever(speed_sp = 100 * direcao)
    motorB.stop(stop_action = 'hold')

def pegapega():
    print("TENTANDO PEGAR")
    motorB.stop()
    motorA.stop()
    while(sensor_frente.distance_centimeters > 7):
        print(sensor_frente.distance_centimeters)
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)
    motorA.stop()
    motorB.stop()
    motorC.run_timed(speed_sp=100, time_sp=100)

 #girar no proprio eixo o suficiente para procuar

def rodaroda(x):
    print(x)
    motorA.stop()
    motorB.stop()
    motorB.run_timed(speed_sp=800, time_sp=x)
    motorA.run_timed(speed_sp=-800, time_sp=x)
    while motorA.is_running and motorB.is_running:
        pass
    motorB.stop()
    motorA.stop()

#Anda a uma dada velocidade enquanto ve uma dada cor >>> os parametros sao a cor e a velocidade dos motores
def anda_enquanto_cor(cor, velocidade):
    while sensor1.color == cor and sensor2.color == cor:
        motorA.run_forever(speed_sp = velocidade)
        motorB.run_forever(speed_sp = velocidade)
    motorA.stop(stop_action = 'hold')
    motorA.reset()
    motorB.stop(stop_action = 'hold')
    motorB.reset()

#Vai pra frente ate uma determinada posicao do motor A >>> os parametros sao a posicao final desejada e a velocidade dos motores
def frente_por_rotacoes(posicao, velocidade):
    motorA.reset()
    motorB.reset()
    while motorA.position < posicao:
        motorA.run_forever(speed_sp = velocidade)
        motorB.run_forever(speed_sp = velocidade)
    motorA.stop(stop_action = 'hold')
    motorB.stop(stop_action = 'hold')

#Vai pra tras ate uma determinada posicao do motor A >>> os parametros sao a posicao final desejada(negativa) e a velocidade dos motores(positiva)
def re_por_rotacoes(posicao, velocidade):
    motorA.reset()
    motorB.reset()
    while motorA.position > posicao:
        motorA.run_forever(speed_sp = -velocidade)
        motorB.run_forever(speed_sp = -velocidade)
    motorA.stop(stop_action = 'hold')
    motorB.stop(stop_action = 'hold')

#Ajuste utilizando os dois motores ao mesmo tempo
def ajuste_direto(direcao):
    time.sleep(1)
    cor = sensor1.color
    time.sleep(1)
    while True:
        if sensor1.color == cor:
            motorA.run_forever(speed_sp = 200 * direcao)
        else:
            motorA.stop(stop_action = 'hold')

        if sensor2.color == cor:
            motorB.run_forever(speed_sp = 200 * direcao)
        else:
            motorB.stop(stop_action = 'hold')

        if sensor1.color != cor and sensor2.color != cor:
            motorA.stop(stop_action = 'hold')
            motorB.stop(stop_action = 'hold')
            break

#Funcao que recebe um valor entre 0 e 2 e realiza a curva com dois motores p/ aquela direcao, sendo 0 -> direita; 1 -> em frente; 2 -> esquerda
def curva_direcao(x, tamanho_curva):
    if x == 0:
        curva_direitacom2(tamanho_curva)
    elif x == 2:
        curva_esquerdacom2(tamanho_curva)

""" EXECUCAO """

velocidade = 900
tamanho_curva_2m = 300

cores_circuito = []
direcoes_disponiveis = [0, 1, 2]

sensor1.calibrate_white()
sensor2.calibrate_white()
cor_atual = sensor1.color
anda_enquanto_cor(cor_atual, velocidade)
frente_por_rotacoes(200, velocidade)
ajuste_direto(-1)

time.sleep(1)
cor_atual = sensor1.color
time.sleep(1)

cores_circuito.append(cor_atual)
for direcao in range(3):
    #Realiza esse laco p/ cada direcao, de 0 a 2
    curva_direcao(direcao, tamanho_curva_2m)
    ajuste_direto(1)
    ajuste_direto(-1)
    frente_por_rotacoes(300, velocidade)
    cor_atual = sensor1.color
    anda_enquanto_cor(cor_atual, velocidade)
    frente_por_rotacoes(200, velocidade)
    time.sleep(1)
    cor_lida = sensor1.color
    time.sleep(1)
    ajuste_direto(-1)
    ajuste_direto(1)

    if cor_lida == 1: #se a cor lida for preto
        re_por_rotacoes(300, velocidade)
        cor_atual = sensor1.color
        anda_enquanto_cor(cor_atual, -velocidade)
        re_por_rotacoes(200, velocidade)
        ajuste_direto(1)
        ajuste_direto(-1)
        re_por_rotacoes(300, velocidade)
        if direcao == 0:
            curva_direcao(1, tamanho_curva_2m)
        elif direcao == 1:
            curva_direcao(0, tamanho_curva_2m)
        ajuste_direto(1)
        ajuste_direto(-1)
        continue
    else: #se ler qualquer outra cor
        
        
