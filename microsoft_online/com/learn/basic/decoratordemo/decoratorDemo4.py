#coding=utf-8
'''
Created on Sep 1, 2015

@author: imad
'''
def salesgirl(discount):#第一层的参数是修饰符的值
    def expense(method):#第二次的参数是被装饰的函数
        def serve(*args):#第三层的参数的是被装饰函数的参数
            print "Salesgirl:Hello, what do you want?", method.__name__
            result = method(*args)
            if result:
                print "Salesgirl: This shirt is 50$.As an old user, we promised to discount at %d%%" %(discount)
            else:
                print "Salesgirl: Well, how about trying another style?"
            return result
        return serve
    return expense
   
@salesgirl(50)
def try_this_shirt(size):
    if size < 35:   
        print "I: %d inches is to small to me" %(size)
        return False
    else:
        print "I:%d inches is just enough" %(size)
        return True
result = try_this_shirt(38)
print "Mum:do you want to buy this?", result

try_this_shirt(20)



