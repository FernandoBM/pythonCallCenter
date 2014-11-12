'''
Created on 6 Nov 2014

@author: f.benavides
'''

class Cliente():
    '''
    Cliente representa a una persona llamando
    '''
    def __init__(self, t_entrada, t_servicio):
        self.t_entrada = t_entrada
        self.t_servicio = t_servicio
        self.t_en_sistema = 0
        self.t_restante = t_servicio
        
    def getTEntrada (self):
        return self.t_entrada

    def getTServicio (self):
        return self.t_servicio
    
    def getTEnSistema (self):
        return self.t_en_sistema
    
    def addTEnSistema (self):
        self.t_en_sistema+=1
    
    def setTEntrada (self, t_entrada):
        self.t_entrada = t_entrada

    def setTServicio (self, t_servicio):
        self.t_servicio = t_servicio

    def getTiempoRestanteEnCola (self):
        return None

    def setTiempoRestanteEnServicio (self):
        return None

    def isOkParaCola (self):
        return None

    def isServicioCompletado(self):
        atendido = False
        if self.t_restante == 0:
            atendido = True
        return atendido
    
    def __str__(self):
        return "Cliente " + str(self.getTEntrada()) + " " + str(self.getTServicio())
    
    
        