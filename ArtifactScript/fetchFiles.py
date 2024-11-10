import json
import os


class fetchFiles:
    def __init__(self, parent_path) -> None:
        self.parent_path = parent_path
        self.data = {'data': []}

    def fetch(self):
        '''
        1. give downloads path
        2. extract all the artifact folders from downloads.
        3. iterate over the artifacts to extract the files.
        4. store the files in a list.
        '''

        for artifats in os.listdir(os.path.join(self.parent_path)):
            if os.path.isdir(os.path.join(self.parent_path, artifats)):
                for logDirs in os.listdir(os.path.join(self.parent_path, artifats)):
                    if os.path.isdir(os.path.join(self.parent_path, artifats, logDirs)):
                        for files in os.listdir(os.path.join(self.parent_path, artifats, logDirs)):
                            if '.log' in files:
                                self.data['data'].append({ 'artifactFolder': artifats,
                                                    'jenkinsLogs': logDirs, 
                                                    'file': files})

        return {'message': "files fetch successfully.", 'data': self.data}

    def saveData(self, fileName):
        data_file = os.path.join(os.getcwd(), "data", fileName)
        with open(data_file, "w") as f:
            json.dump(self.data, f, indent=4)
        return {'message': f'data saved in file {data_file}', 'fileName': fileName, 'keysInfo': list(self.data['data'][0].keys())}
    

        