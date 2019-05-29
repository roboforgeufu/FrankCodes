#Arquivo com todas as funcoes a serem utilizadas na programacao


#90* p/ esquerda com 1 motor // x e a quantidade de rotacoes do motorB
def curva_esquerda(rotacoes, velocidade):
    motorA.stop()
    motorB.on_for_rotations(SpeedPercent(velocidade), rotacoes)
    motorB.stop()

#90* p/ direita com 1 motor // x e a quantidade de rotacoes do motorB
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
        
