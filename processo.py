from time import time, sleep_ms
# Simulador do processo de volume
class Volume(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self._escala = 100.0 # escala de tempo do processo
        self._volume = 750.0  # Valor inicial do volume
        self._bomba = False
        self._vazao = 0
        self._realVazao = 0.0
        self._saida = False
        self._saidaVazao = 500.0 # Vazao de saida (constante)
        self._tant = time()        
        self._status = 'ok'

    def update(self):
        if self._status == 'ok':
            if self._bomba:
                self._volume += self._escala*self._realVazao * (time()-self._tant)/3600.0
                self._realVazao = self._vazao
            else:
                self._realVazao = 0.0
            if self._saida:
                self._volume -= self._escala*self._saidaVazao * (time()-self._tant)/3600.0
        elif self._status == 'reset':
            self.reset()
        self._tant = time()
        sleep_ms(100)  # Pausa para processamento

    def getBomba(self):
        return self._bomba

    def setBomba(self, v):
        self._bomba = v

    def getVolume(self):
        return self._volume

    def getSaida(self):
        return self._saida

    def setSaida(self, v):
        self._saida = v

    def getVazao(self):
        return self._vazao

    def setVazao(self, v):
        self._vazao = v if v < 500 else 500
