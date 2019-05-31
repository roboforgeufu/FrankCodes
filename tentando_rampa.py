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
def cor(cor_lida):
    if cor_lida[0] < 10:
        #NoColor
        return 0
    elif cor_lida[0] < 140:
        #Verde, Preto Azul
        if cor_lida[2] < 30:
            #Verde ou Preto
            if cor_lida[1] < 60:
                #PRETO
                return 1
            else:
                #Verde
                return 3
        else:
            #Azul
            return 2
    elif cor_lida[0] < 300:
        #Vermelho ou Amarelo
        if cor_lida[1] < 90:
            return 5
        else:
            return 4
    else:
        #Branco
        return 6
def eh_rampa(posicao, velocidade):
    cores_lidas = []
    motorA.reset()
    motorB.reset()
    while motorA.position < posicao:
        motorA.run_forever(speed_sp = velocidade)
        motorB.run_forever(speed_sp = velocidade)
        cor_r = cor(sensor1.raw)
        if cor_r not in cores_lidas:
            print(cor_r)
            cores_lidas.append(cor_r)
    motorA.stop()
    motorB.stop()
    print(cores_lidas)
    if len(cores_lidas) > 1:
        print("RAMPA!")
        return True
    else:
        print("nao eh rampa..")
        return False

""" EXECUCAO """
velocidade = 500

print(eh_rampa(600, velocidade))
time.sleep(10)
