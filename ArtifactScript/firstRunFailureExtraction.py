from artifacts import artifacts

class firstRunFailureExtraction(artifacts):
    
    def __init__(self):
        super().__init__()
        self.filePath = ""
    
    def process(self, line, failingScenariosFlag):
        return super().process(line, failingScenariosFlag, 1)
