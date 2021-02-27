import sys
from emulatedDisk import emulatedDisk

inputFile = open("input.txt", "r")
outputFile = open("output.txt", "w")

e = None

for line in inputFile:
    args = line.strip().split(" ")
    if len(args) < 1:
        continue
    if  args[0] == " "  or args[0] == "":
        outputFile.write("\n")
    elif args[0] == "in":
        e = emulatedDisk();
        outputFile.write("system initialized\n")
        
    elif args[0] == "cr":
        
        if e.create(args[1]):
            outputFile.write(args[1]+" created\n")
        else:
            outputFile.write("error\n")
        
    elif args[0] == "de":
        if (e.destroy(args[1])):
            outputFile.write(args[1]+" destroyed\n")
        else:
            outputFile.write("error\n")
        
    elif args[0] == "op":
        index = e.open(args[1])
        if (index == "error"):
            outputFile.write("error/n")
        else:
            outputFile.write(args[1]+" opened "+index+"\n")
        
    elif args[0] == "cl":
        e.close(int(args[1]))
        outputFile.write(args[1]+" closed\n")
        
    elif args[0] == "rd":
        n =  e.read(int(args[1]),int(args[2]),int(args[3]))
        outputFile.write(str(args[3]) +" bytes read from file "+str(args[1])+"\n")
        
    elif args[0] == "wr":
        n = e.write(int(args[1]),int(args[2]),int(args[3]))
        outputFile.write(str(args[3]) +" bytes written to file "+str(args[1])+"\n")
        
    elif args[0] == "sk":
        if (e.seek(int(args[1]),int(args[2]))):
            outputFile.write("position is "+args[2]+"\n")
        else:
            outputFile.write("error\n")
        
    elif args[0] == "dr":
        outputFile.write(e.directory()+"\n")
        
    elif args[0] == "rm":
        outputFile.write(str(e.rm(int(args[1]),int(args[2])))+"\n")
        
    elif args[0] == "wm":
        n = e.wm(int(args[1]),args[2])
        outputFile.write(str(n+1)+" bytes written to M\n")
        
    else:
        outputFile.write("error\n");
        
outputFile.close()
inputFile.close()
        