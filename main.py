#Import all important libraries

import sys, getopt
import subprocess

if __name__ == '__main__':
    if(len(sys.argv)<3):
        raise getopt.GetoptError
    else:
        grammar = sys.argv[1]
        test = sys.argv[2]
        
print("\n\n\nRunning the Scanner Generator...")
#Run Scanner Generator
bashCmd = [
        "python", 
        "scannerGenerator.py", 
        grammar]
subprocess.Popen(bashCmd)
p = subprocess.Popen(bashCmd, stdout = subprocess.PIPE)
while True:
    line = p.stdout.readline()
    if not line: break


print("\n\n\nRunning the Scanner ...")
bashCmd = [
        "python", 
        "scanner.py", 
        test]
subprocess.Popen(bashCmd)
p = subprocess.Popen(bashCmd, stdout = subprocess.PIPE)
while True:
    line = p.stdout.readline()
    if not line: break


print("\n\n\nRunning the Parser Generator...")
bashCmd = [
        "python", 
        "parserConstructor.py"]
subprocess.Popen(bashCmd)
p = subprocess.Popen(bashCmd, stdout = subprocess.PIPE)
while True:
    line = p.stdout.readline()
    if not line: break

if('3' not in grammar):
    print("\n\n\nRunning the Parser...")
    bashCmd = [
        "python", 
        "parserProgram.py"]
else:
    print("\n\n\nRunning the Parser...")
    bashCmd = [
        "python", 
        "parser.py"]
    


subprocess.Popen(bashCmd)
p = subprocess.Popen(bashCmd, stdout = subprocess.PIPE)
while True:
    line = p.stdout.readline()
    if not line: break
    

