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
    while cor(sensor1.raw) != cor:
        motorA.run_forever(speed_sp = 100 * direcao)
    motorA.stop(stop_action = 'hold')
    while cor(sensor1.raw) != cor:
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
def anda_enquanto_cor(cor_, velocidade):
    while cor_ == cor(sensor1.raw) and cor_ == cor(sensor2.raw):
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
    #time.sleep(1)
    x = cor(sensor1.raw)
    #time.sleep(1)
    while True:
        if cor(sensor1.raw) == x:
            motorA.run_forever(speed_sp = 200 * direcao)
        else:
            motorA.stop(stop_action = 'hold')

        if cor(sensor2.raw) == x:
            motorB.run_forever(speed_sp = 200 * direcao)
        else:
            motorB.stop(stop_action = 'hold')

        if cor(sensor1.raw) != x and cor(sensor2.raw) != x:
            motorA.stop(stop_action = 'hold')
            motorB.stop(stop_action = 'hold')
            break

#Funcao que recebe um valor entre 0 e 2 e realiza a curva com dois motores p/ aquela direcao, sendo 0 -> direita; 1 -> em frente; 2 -> esquerda
def curva_direcao(x, tamanho_curva, velocidade):
    if x == 0:
        curva_direitacom2(tamanho_curva, velocidade)
    elif x == 2:
        curva_esquerdacom2(tamanho_curva, velocidade)

#funcao que gera os intervalos de cor lidas em rgb, continuar para maior precisao na leitura de cores
def cor_intervalo():
    cores_lista0=[]
    cores_lista1=[]
    cores_lista2=[]
    for i in range(5):
        time.sleep(1)
        cor = list(sensor1.rgb)
        cores_lista0.append(cor[0])
        cores_lista1.append(cor[1])
        cores_lista2.append(cor[2])
    intervalomaior = (max(cores_lista0)+(max(cores_lista0) - min(cores_lista0)) ,max(cores_lista1)+(max(cores_lista1) - min(cores_lista1)) , max(cores_lista2)+(max(cores_lista2) - min(cores_lista2)))
    intervalomenor = (min(cores_lista0)+(max(cores_lista0) - min(cores_lista0)) ,min(cores_lista1)+(max(cores_lista1) - min(cores_lista1)) , min(cores_lista2)+(max(cores_lista2) - min(cores_lista2)))
    intervaloamplitude = (max(cores_lista0) - min(cores_lista0), max(cores_lista1) - min(cores_lista1) , max(cores_lista2) - min(cores_lista2))
    print(intervalomaior)
    print(intervalomenor)
    print(intervaloamplitude)
    #criar modulo de comparacao entre intervalos obtidos e cores

def teste_garra():
    #motorC.on_for_rotations(SpeedPercent(40), -2.5)
    #time.sleep(5)
    motorC.on_for_rotations(SpeedPercent(40), 3.5)
    motorC.stop(stop_action = 'hold')
    time.sleep(5)
    motorC.on_for_rotations(SpeedPercent(40), -3.5)


""" EXECUCAO """


velocidade = 500
tamanho_curva_2m = 450

cores_circuito = []
#variavel criada para receber a associacao entre cores e direcoes
cor_direcao = {}
direcoes_disponiveis = [0, 1, 2]

sensor1.calibrate_white()
sensor2.calibrate_white()
cor_atual = cor(sensor1.raw)
anda_enquanto_cor(cor_atual, velocidade)
frente_por_rotacoes(70, velocidade)
ajuste_direto(-1)
#time.sleep(0.5)
frente_por_rotacoes(600, velocidade)

#time.sleep(1)
cor_atual = cor(sensor1.raw)
print("LEU", cor_atual)
#time.sleep(1)

cores_circuito.append(cor_atual)

""" CODIGO QUE DEVE SER SEMPRE EXECUTADO, PARA CADA COR DE CRUZAMENTO"""

if cor_atual in cor_direcao.keys():
    print("JA APRENDEU")
    curva_direcao(cor_direcao[cor_atual], tamanho_curva_2m, velocidade)
    #vai pra proxima cor
elif len(direcoes_disponiveis) == 1:
    cor_direcao[cor_atual] = direcoes_disponiveis[0]
    direcoes_disponiveis.pop(0)
    curva_direcao(cor_direcao[cor_atual], tamanho_curva_2m, velocidade)
    #vai pra proxima cor
else:
    print("APRENDE A DIRECAO DE", cor_atual)
    for direcao in direcoes_disponiveis:
        print("ENTROU NO LOOP =", direcao)
        #Realiza esse laco p/ cada direcao, de 0 a 2
        curva_direcao(direcao, tamanho_curva_2m, velocidade)
        ajuste_direto(1)

        frente_por_rotacoes(70, velocidade)
        cor_atual = cor(sensor1.raw)
        print("LEU", cor_atual)
        #time.sleep(1)

        anda_enquanto_cor(cor_atual, velocidade)
        frente_por_rotacoes(130, velocidade)

        #time.sleep(1)
        cor_lida = cor(sensor1.raw)
        print("LEU", cor_lida)
        ajuste_direto(-1)


        if cor_lida == 1: #se a cor lida for preto
            print("ENTRA EM PRETO")
            re_por_rotacoes(-70, velocidade)

            ajuste_direto(-1)

            re_por_rotacoes(-400, velocidade)
            if direcao == 0:
                print("FAZ A CURVA DE VOLTA")
                curva_direcao(2, tamanho_curva_2m, velocidade)
            print("PROXIMA DIRECAO")
            continue
        else: #se ler qualquer outra cor
            print("APRENDE")
            #associa a direcao a cor atual
            cor_direcao[cor_atual] = direcao
            #remove das direcoes possiveis a direcao atual
            direcoes_disponiveis.remove(direcao)

            break
        #continuar a andar
time.sleep(100)



'''
se a cor ja existir na cor_direcao: adotar a direcao como a associada previamente, caso nao, testar.
if cor_atual in cor_direcao:
    direcao = cor_direcao[cor_atual]
else
    teste
    '''
