import subprocess
import sys
import os

'''
Author: Manas Taunk
Args:
    namespace: namespace of deployment
    microservices: microservice names provided as comma seperated (Ex: microservice1,microservice2,microservice3)
    timeout: duration(in seconds) for which logs has to be collected.

Command: 
    python3 collectAllMicroserviceLogs.py <namesapce> <list-of-microservices> <timeout> <fetchInterval>
Ex: 
    python3 collectAllMicroserviceLogs.py mynamespace ms1,ms2,ms3 100 10
'''
if __name__ == "__main__":
    namespace = str(sys.argv[1])
    microservices = str(sys.argv[2])
    microservices = microservices.split(',')
    tout = int(sys.argv[3])
    subprocesses = []
    commands = []
    currentDirectoryPath = os.getcwd()
    path = os.path.join(currentDirectoryPath, "logsCollection.sh")
    cmd = "sh "+str(path) # ./logsCollection.sh <namespace> <microservice>
    for microservice in microservices:
        commands.append(cmd+" "+namespace+" "+microservice+" "+str(currentDirectoryPath)+" "+str(tout)+"  10")
    # create subprocess and run them in backgroung
    for command in commands:
        subprocesses.append(subprocess.Popen(command, shell=True))
    try:
        while len(subprocesses)>0:
            process = subprocesses.pop(0)
            process.communicate(timeout=tout)
            tout = 5
    except Exception as e:
        print(e.__traceback__)
    finally:
        while len(subprocesses)>0:
            process = subprocesses.pop(0)
            #TODO: kill the above fetch process gracefully/forcefully.
            process.kill()
