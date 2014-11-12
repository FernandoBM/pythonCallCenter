'''
Created on 6 Nov 2014

@author: f.benavides
'''
import re
import Cliente
from call_center.Operadora import Operadora
from call_center.Cola import Cola

def ObtenerDatos(fichero, lista_entrada):
    
    #lista_entrada=[]
    try:
        f = open(fichero, 'r')
        fline = f.readline()
        while fline:
            if esLineaCliente(fline):
                fline = f.readline()
                while fline: 
                    [t_entrada, t_salida] = map(int, re.findall('\d+', fline))
                    nuevo_cliente = Cliente.Cliente(t_entrada, t_salida)
                    lista_entrada.append(nuevo_cliente)
                    fline = f.readline()
            elif esLineaOperadora(fline):
                fline = f.readline() 
                n_operadora = map(int, re.findall('\d+', fline))[0]
            elif esLineaCola(fline):
                fline = f.readline() 
                tam_cola = map(int, re.findall('\d+', fline))[0]
            fline = f.readline()
    except IOError:
        print "Check if the file", fichero, "exists or is corrupted"
    return n_operadora, tam_cola

def esLineaCliente(linea):
    '''Tells if the line read of the document contains 'Cliente'''
    esCliente = False
    if linea.find("Cliente") != -1:
        esCliente = True
    return esCliente

def esLineaOperadora(linea):
    '''Tells if the line read of the document contains 'operadora'''
    esOperadora = False
    if linea.find("operadora") != -1:
        esOperadora = True
    return esOperadora

def esLineaCola(linea):
    '''Tells if the line read of the document contains 'cola'''
    esCola = False
    if linea.find("cola") != -1:
        esCola = True
    return esCola

def isOperadorasLibres(equipoOperadoras):
    '''Returns true if every single operadora is idle'''
    operadorasLibres = True
    for elemento in equipoOperadoras:
        if not elemento.isLibre:
            operadorasLibres = False
            break    
    return operadorasLibres

def isColaLlena (cola):
    
    colaLlena = True
    for cliente in cola: 
        if cliente.getTServicio()==0:
            colaLlena = False
            break
    return colaLlena

def encolaClientes(lista_clientes, cola, time):
    '''Adds customers to the queue'''
    global index_cola
    while not isColaLlena(cola):
        if lista_clientes[0].getTEntrada()==time:
            cola[index_cola]=lista_clientes[0]
            index_cola += 1
            del lista_clientes[0]
        else:
            break   

def descartaClientes(lista_clientes, cola, time):
    '''Drops customers off the queue'''
    if isColaLlena(cola):
        while lista_clientes[0].getTEntrada()==time:
            del lista_clientes[0]
            #Cliente tirado archivo de salida

def createCola(tam_lista):
    lista = []
    for i in range(tam_lista):
        cliente = Cliente.Cliente(0,0)
        lista.append(cliente)
    return lista

def createOperadoraCola(tam_lista):
    lista = []
    for i in range(tam_lista):
        operadora_a_insertar = Operadora()
        lista.append(operadora_a_insertar)
    return lista

def despachaClientes(equipoOperadoras):
    for operadora in equipoOperadoras:
        if operadora.isLibre():
            continue
        elif operadora.isOKParaDespachar():
            #Escribe en fichero de salida los tiempos
            operadora.setLibre()
            
def hayOperadoraLibre(equipoOperadoras):
    hayLibre = False
    for operadora in equipoOperadoras:
        if operadora.isLibre():
            hayLibre = True
            break
    return hayLibre

def hayClienteEnCola(cola):
    hayCliente = False
    for cliente in cola:
        if cliente.getTServicio() != 0:
            hayCliente = True
            break
    return hayCliente

def introduceCliente(equipoOperadoras, cola):
    
    global index_cola
    for operadora in equipoOperadoras:
        if operadora.isLibre():
            if cola[0].getTServicio() != 0:
                operadora.setCliente(cola[0])
                if hayClienteEnCola(cola):
                    desplazaCola(cola)
                    index_cola -= 1
                else:
                    break
            else:
                break
        else:
            break
             
def desplazaCola(cola):
    counter = 0
    while counter < len(cola):
        cola[counter] = cola[counter+1]
        counter += 1
    cola[counter].setTEntrada(0)
    cola[counter].setTServicio(0)

def actualizaTiempoEnSistema(cola, equipoOperadoras):
    
    for cliente in cola:
        cliente.addTEnSistema()
    for operadora in equipoOperadoras:
        operadora.getCliente().addTEnSistema()
    
            
    

def pasaClientesACentralita(lista_clientes, cola, equipoOperadoras, time):
    
    procesando = True
    primera_vez = True;
    
    while procesando:
        if hayOperadoraLibre(equipoOperadoras):
            if hayClienteEnCola(cola):
                while hayOperadoraLibre(equipoOperadoras) and hayClienteEnCola(cola):
                    introduceCliente(equipoOperadoras, cola)
                    procesando = False
            else:
                if primera_vez:
                    encolaClientes(lista_clientes, cola, time)
                    descartaClientes(lista_clientes, cola, time)
                    primera_vez = False
                else:
                    procesando = False
        else:
            encolaClientes(lista_clientes, cola, time)
            descartaClientes(lista_clientes, cola, time)
            procesando = False
    
        
         

#******************************************************#
#****************AQUI EMPIEZA EL CODIGO ***************#
#******************************************************#
#******************************************************#

if __name__ == '__main__':
    
    index_cola = 0
    lista_clientes = []
    cola = []
    equipoOperadoras = []
    time = 0;
    
    #Obtengo los clientes del archivo txt adjunto
    
    n_operadoras, tam_cola = ObtenerDatos("clientes.txt", lista_clientes)
     
    for elemento in lista_clientes:
        print elemento
    print str(n_operadoras)
    print str(tam_cola)
    
    cola = createCola(tam_cola)
    equipoOperadoras = createOperadoraCola(n_operadoras)
    
    
    #Abrir fichero de salida
    
    #Simular entorno del CallCenter
    while (len(cola)>0 or isOperadorasLibres(equipoOperadoras)):
        despachaClientes(equipoOperadoras)
        pasaClientesACentralita(lista_clientes, cola, equipoOperadoras, time)
        encolaClientes(lista_clientes, cola, time)
        descartaClientes(lista_clientes, cola, time)
        time+=1
        actualizaTiempoEnSistema(cola, equipoOperadoras)


    