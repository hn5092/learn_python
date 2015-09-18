
def roles(func):
    #print "@ starts"
    def return_func(*args):
        func(*args)
    return return_func

def ROLES(param):
    #print "@(param) starts"
    def return_func(func):
        def add_param(*args):
            if param == "root":
                func(*args)
            else:
                print "Permission denied, root only."          
        return add_param
    return return_func
    


@roles
def uninstall(param):
    print "Do you want to uninstall %s?" % param

@ROLES("root")
def UNINSTALL(param):
    print "Do you want to UNINSTALL %s?" % param

@ROLES("r00t")
def UNinstall(param):
    print "Do you want to UNinstall %s?" % param


uninstall("360")

UNINSTALL('baidu')

UNinstall('qq')
