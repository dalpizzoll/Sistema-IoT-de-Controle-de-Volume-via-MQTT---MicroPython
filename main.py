from machine import reset, Pin, Timer
from rede import Rede
from time import sleep_ms, time, ticks_ms
from json import load, dumps, loads
from ntptime import settime
from umqtt.robust import MQTTClient
from processo import Volume

topico = b'v1/devices/me/telemetry'
topRPCReq = 'v1/devices/me/rpc/request/'
topRPCResp = 'v1/devices/me/rpc/response/'

def procRPC(t, p):
    global cliente
    
    nroReq = t.decode().replace(topRPCReq,'')
    acao = loads(p.decode())
     
    if acao['method'] == 'setSaida':
        processo.setSaida(acao['params'])
    elif acao['method'] == 'getSaida':
        cliente.publish((topRPCResp+nroReq).encode(), str(bool(processo.getSaida())).lower().encode())
    elif acao['method'] == 'setBomba':
        processo.setBomba(acao['params'])
    elif acao['method'] == 'getBomba':
        cliente.publish((topRPCResp+nroReq).encode(), str(bool(processo.getBomba())).lower().encode())
    elif acao['method'] == 'setVazao':
        vazao = int(acao['params'])
        processo.setVazao(vazao)
    elif acao['method'] == 'getVazao':
        cliente.publish((topRPCResp+nroReq).encode(), str(processo.getVazao()).encode())
    elif acao ['method'] == 'setVolume':
        processo.setVolume(acao['params'])
    elif acao['method'] == 'getVolume':
        cliente.publish((topRPCResp+nroReq).encode(), str(processo.getVolume()).encode())

    else:
        print (p)
    
    print(acao)

with open('config.json', 'r') as arq:
    cfg = load(arq)

def cbTimer(t):
    global taNaHora
    
    taNaHora = True
    
def debug(arg):
    print(arg)

with open('config.json') as arq:
    cfg = load(arq)   

r = Rede(cfg['rede'], cfg['senha'],
         cb=debug)

if r.conectado:
    settime()
    cliente = MQTTClient(cfg["clientId"],
                         cfg["broker"],
                         user= cfg["userbroker"],
                         password='')
    cliente.set_callback(procRPC)
    cliente.connect()
    cliente.subscribe(b'v1/devices/me/rpc/request/+')
else:
    print ('Deu ruim...Reiniciando')
    sleep_ms(2000)
    reset()

taNaHora = False
timm = Timer(0)
timm.init(mode = Timer.PERIODIC,
          period = 500,
          callback = cbTimer)


# Cria e inicializa a simulação
processo = Volume()
dados={'ts':0, 'values':{}}

# valor correto de timestamp -> 'ts':(time()+946684800)*1000
while True:
    cliente.check_msg()
    processo.update()

    # atualização da telemetria
    if taNaHora:    
        dados['ts'] = (time()+946684800)*1000
        dados['values']['volume'] = processo.getVolume()
        dados['values']['vazao'] = processo.getVazao()
        
        payload = dumps(dados).encode()
        
        cliente.publish(topico, payload)
        taNaHora = False