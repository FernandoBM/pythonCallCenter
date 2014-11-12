'''
Created on 6 Nov 2014

@author: f.benavides
'''

class FirstModule():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def suma(self):
        return self.a + self.b
     
ejemplo = FirstModule(10,50)
print ejemplo.suma()

