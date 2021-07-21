'''
Created on Feb 19, 2021

@author: mark_kwong
'''

#===========================================================================
# Description: a single card in the game Set
#
# State Attributes
#   Each of the card attributes are numbers 0, 1, or 2 that can be displayed textually
#   or graphically 
#   - value
#   - color
#   - count
#   - shape
# Methods
#   getValueOf(attr) - returns the value of one of the four attributes
#      attr is a String that is either 'VALUE', 'COLOR', 'COUNT', or 'SHAPE'
#   __str__() - returns a string for the card
#===========================================================================
class Card:
    
    ATTRIBUTES = ['VALUE', 'COLOR', 'COUNT', 'SHAPE']

    # value, color, count, shape must be a number 0, 1 or 2
    def __init__(self, value, color, count, shape):
        self.value = value
        self.color = color
        self.count = count
        self.shape = shape
        
    # what - String that should be one of the four ATTRIBUTES
    def getValueOf(self, what):
        assert what in self.ATTRIBUTES, "input needs to be 'VALUE', 'COLOR', 'COUNT' or 'SHAPE'"
        if what == 'VALUE':
            return self.value
        elif what == 'COLOR':
            return self.color
        elif what == 'COUNT':
            return self.count
        elif what == 'SHAPE':
            return self.shape
    
    # VALUE: 0 == x     1 == y      2 == z
    # COLOR: 0 == red   1 == green  2 == magenta
    # COUNT: 0 == 1     1 == 2      2 == 3
    # SHAPE: 0 == lower 1 == upper  2 == upper/underline
    def __str__(self):
        if self.value == 0:
            ch = 'X'
        elif self.value == 1:
            ch = 'Y'
        elif self.value == 2:
            ch = 'Z'
            
        if self.color == 0:
            fmt = '\033[31'  # red
        elif self.color == 1:
            fmt = '\033[32'  # green
        elif self.color == 2:
            fmt = '\033[35'  # magenta
            
        if self.shape == 0:
            fmt += 'm'       # plain
            ch = ch.lower()  # lower case
        elif self.shape == 1:
            fmt += ';3m'       # italic 
            #fmt += ';1;3m'     # bold
        elif self.shape == 2:
            fmt += ';4m'     # underline
            
        if self.count == 0:
            letters = '  {}{}\033[0m  '.format(fmt, ch)
        elif self.count == 1:
            letters = ' {}{} {}\033[0m '.format(fmt, ch, ch)
        elif self.count == 2:
            letters = '{}{} {} {}\033[0m'.format(fmt, ch, ch, ch)
            
        return(letters)
