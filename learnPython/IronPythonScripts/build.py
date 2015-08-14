import sys
reload(sys)
sys.setdefaultencoding('utf-8')

dict={
      "framework1":"./modules/core/framework1_0.py",
      "framework2":"./modules/core/framework.py",
      "meta":"./modules/core/meta.py"     
    }
output = None
file=None
output=None
contents=[]
try:
    for k,v in  dict.items():
        name=k
        path=v
        print k,v
        file = open(path)
        text=file.read()
        if name=="framework1":
            start=text.find("#<body>#")
            end=text.find("#<test>#")
            body=text[start:end]
            print body
            contents.append(body)
        elif name=="framework2":
            place=text.find("#<head>#")
            import_str=text[0:place]
            import_str=import_str.replace("import meta","import copy")            
            print import_str
            contents.insert(0,import_str) 
            place=text.find("#<body>#")
            body=text[place:]  
            print body          
            contents.append(body)
        elif name=="meta":
            start=text.find("#<body>#")
            end=text.find("#<test>#")
            body=text[start:end]
            print body
            contents.insert(2,body) 

    result="\n\r### split line ###\n\r".join(contents)#.encode("utf-8    
    print result

    output = open('./build_result.py', 'w')    
    output.writelines(result)   
    pass          


finally:
    file.close()
    output.close()
    pass
