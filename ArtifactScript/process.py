import json
import os
from firstRunFailureExtraction import firstRunFailureExtraction
from finalFailures import finalFailures

class process:
    def __init__(self, parentPath, fileKeysInfo, failingType: int, isStoreFailingScenario: bool) -> None:
        self.parentPath = parentPath
        self.fileKeysInfo = fileKeysInfo
        self.artifacts = {'data': {}}
        self.failingType = failingType
        if failingType==1:
            self.processFailures = firstRunFailureExtraction()
        elif failingType==2:
            self.processFailures = finalFailures()
        self.__isStoreFailingScenario = isStoreFailingScenario
        self.failingScenarioData = {'data': []}

    def processArtifactsDirListData(self, fileName):
        data = self.getJsonData(os.getcwd(), os.path.join('data', fileName))
        data = data['data']
        for artifactInfo in data:
            if artifactInfo[self.fileKeysInfo[0]] not in self.artifacts['data']:
                self.artifacts['data'][artifactInfo[self.fileKeysInfo[0]]] = []
            #TODO: can remove unwanted data in future
            self.artifacts['data'][artifactInfo[self.fileKeysInfo[0]]].append(artifactInfo)
        return {'message': "preprocessing artifact dir successfull", 'data': self.artifacts}
        

    def getJsonData(self, parentFolder, fileName):
        filePath = os.path.join(parentFolder, fileName)
        with open(filePath, 'r') as file:
            data = json.load(file)
        return {'message': "fetch data successfull", 'data': data['data']}

    def processFileData(self, fileName: str):
        try:
            data = self.getJsonData(os.getcwd(), os.path.join('data', fileName))
            data = data['data']
            for artifact in data.keys():
                #TODO: can create multiple threads
                self.processFailures.dirPresentAtLocation = False
                for files in data[artifact]:
                    self.processFailures.failingScenario = []
                    self.processFailures.count = 0
                    filePath = self.parentPath
                    for ele in self.fileKeysInfo:
                        filePath = os.path.join(filePath, files[ele])
                    failingScenarioData = self.processFailures.getFailingScenarios(filePath, self.failingType, self.__isStoreFailingScenario, artifact)
                    if len(failingScenarioData['failing scenario'])>0:
                        self.failingScenarioData['data'].append({
                            'artifact': artifact,
                            'file': filePath,
                            'failingScenariosData': failingScenarioData['failing scenario'],
                            'failureCount': len(failingScenarioData['failing scenario'])
                        })
                    # print(f'Extracted info from file {filePath}')

            self.saveData(self.failingScenarioData, "failures.json")
            return {'message': "preprocessing file data successfull", 'fileName': "failures.json", "keysInfo": list(self.failingScenarioData['data'][0].keys())}

        except Exception as e:
            print(e)
            return {'message': e, 'fileName': ""}

    def saveData(self, data ,fileName):
        filePath = os.path.join(os.getcwd(), "data", fileName)
        with open(filePath, 'w') as file:
            json.dump(data, file, indent=4)
        return {'message': "file saved successfully", "fileName": fileName}
    
    def postFailueExtraction(self, fileName):
        path = os.path.join(os.getcwd(), "data")
        data = self.getJsonData(path, fileName)
        data = data['data']
        differentData = set()
        for key, value in enumerate(data):
            for ele in value['failingScenariosData']:
                pass