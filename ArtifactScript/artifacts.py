import os
import json

class artifacts:
    def __init__(self):
        self.failingScenario = []
        self.count = 0
        self.scenarioData = ""
        self.currentScenario = ""
        self.scenarioToSave = False
        self.dirPresentAtLocation = False
        self.scenarioFailuresLogger = ">>>>>>>>>>> Scenario : {} Status : FAILED".format(self.currentScenario)

    def process(self, line, failingScenariosFlag, failureType: int):
        if 'Scenario:' in line or line.strip()=="":
            failingScenariosFlag = False

        if 'Failing scenarios:' in line:
            failingScenariosFlag = True
            self.count+=1
            return {'failingScenariosFlag': failingScenariosFlag}
        
        if failingScenariosFlag and '.feature' not in line:
            failingScenariosFlag = False
        
        if failingScenariosFlag and self.count==failureType:
            # print(line)
            lineData = line.strip().split("  ")
            if len(lineData)==2:
                featureFile = lineData[0].strip()
                scenario = lineData[1].strip()
                self.failingScenario.append({
                    'feature': featureFile,
                    'scenario': scenario
                })
            else:
                print(line)
        return {'failingScenariosFlag': failingScenariosFlag}

    def getFailingScenarios(self, filePath, failureType: int, storeFailureLogs: bool, artifact: str):
        with open(filePath, 'r') as file:
            filedata = file.readlines()
            resp = {'failingScenariosFlag': False}
            data = []
            for line in filedata:
                if line.strip():
                    resp = self.process(line, resp['failingScenariosFlag'])
                    if storeFailureLogs:
                        self.__getFailureJenkinsLogs(line, failureType, artifact)
        return {"failing scenario": self.failingScenario}

    def __getFailureJenkinsLogs(self, line, failureType: int, artifact: str):
        if 'Scenario:' in line:
            if self.currentScenario==True:
                print(f'Scenario: {self.currentScenario}, is to save {self.scenarioToSave} for {str(self.count)} and current Failure type is {str(failureType-1)}')
            if self.scenarioToSave and self.count==failureType-1:
                dirPath = os.path.join(os.getcwd(), "data", "JenkinsLogs", artifact)
                self.__saveData(dirPath)
                self.scenarioToSave = False
            self.scenarioData = ""
            self.currentScenario = line.strip().split(':')[1].strip() # contains scenario and feature file name too.
            self.currentScenario = self.currentScenario.split(" ")[0].strip()
            self.scenarioFailuresLogger = ">>>>>>>>>>> Scenario : {} Status : FAILED".format(self.currentScenario)
            # print(self.scenarioFailuresLogger)
        # store data in scenarioData.
        self.scenarioData+=str(line)
        # is failure log is present, then on scenarioToSave flag (to save scenario at the end)
        if self.scenarioFailuresLogger in line:
            self.scenarioToSave = True
        return

    def __saveData(self, dirPath: str):
        if not self.dirPresentAtLocation:
            os.makedirs(dirPath)
            self.dirPresentAtLocation = True
        scenario = self.currentScenario
        scenario = scenario[:20]
        with open(os.path.join(dirPath, str(scenario)+".log"), 'w') as file:
            file.write(self.scenarioData)



