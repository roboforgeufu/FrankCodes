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
motorC = LargeMotor(OUTPUT_C)

#90* p/ esquerda com 1 motor // x e a quantidade de rotacoes do motorB
def curva_esquerda(x, velocidade):
    motorA.stop()
    motorB.on_for_rotations(SpeedPercent(velocidade), x)
    motorB.stop()

#90* p/ direita com 1 motor // x e a quantidade de rotacoes do motorB
def curva_direita(x, velocidade):
    motorB.stop()
    motorA.on_for_rotations(SpeedPercent(velocidade), x)
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


'''while sensor3.distance_centimeters > 20:
    print('dist > 20')
    print()
    motorA.run_forever(speed_sp = 400)
    motorB.run_forever(speed_sp = 400)
while sensor4.distance_centimeters > 8:
    print('dist > 8')
    print()
    motorA.run_forever(speed_sp = -400)
    motorB.run_forever(speed_sp = 400)
motorA.stop()
motorB.stop()
while sensor4.distance_centimeters > 5:
    motorA.run_forever(speed_sp = 400)
    motorB.run_forever(speed_sp = 400)'''

motorC.run_forever(speed_sp = -250)
time.sleep(6)
motorC.stop()
motorC.run_forever(speed_sp = 250)
time.sleep(10)
motorC.stop(stop_action = 'hold')
