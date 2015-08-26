#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
def talk():
    def walk():
        return "go"
    print walk()
talk()

def people(type='eat'):
    def eat():
        print "eating"
    def sleep():
        print 'sleep'
    if type == 'eat':
        return eat
    else:
        return sleep
people('sleep')()  
    