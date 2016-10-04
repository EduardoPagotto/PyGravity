'''
Created on 21 de set de 2016

@author: pagotto
'''

class Color(object):
    def __init__(self,r=1.0, g=1.0, b=1.0, a=1.0):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __str__(self):
        return str('{0},{1},{2},{3}'.format(self.red, self.green, self.blue, self.alpha))
        
    @staticmethod
    def RED():
        return Color(1.0, 0.0, 0.0, 1.0)
    @staticmethod
    def GREEN():
        return Color(0.0, 1.0, 0.0, 1.0)
    @staticmethod
    def BLUE():
        return Color(0.0, 0.0, 1.0, 1.0)
    @staticmethod
    def YELLOW():
        return Color(1.0, 1.0, 0.0, 1.0)

if __name__ == '__main__':
    color = Color()
    print('Cor:{0}'.format(color))