'''
Created on 6 Nov 2014

@author: f.benavides
'''
import sys, os
import Cliente

class Operadora:

    def __init__(self):
        self.libre = True;
        self.cliente = Cliente.Cliente(0,0)

    def isLibre(self):
        return self.libre
    
    def setLibre(self):
        self.libre = True;
        self.cliente.setTEntrada(0)
        self.cliente.setTSalida(0)
    
    def isOkParaDespachar (self):
        return self.cliente.isServicioCompletado()
    
    def setCliente(self, cliente):
        self.cliente = cliente
    
    def getCliente(self):
        return self.cliente
        
    def getClienteEntrada(self):
        return self.cliente.getTEntrada()
    
    def getClienteSalida(self):
        return self.cliente.getTServicio()
    