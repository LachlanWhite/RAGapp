import os.path
import requests
import json

class ContentStore:
    entryDB = []

    class Entity:
        courseDescription = ""
        vector = []

        def __init__(self, s: str, v: []):
            self.courseDescription = s
            self.vector = v
        
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys = True, indent = 4)

    #def __init__(self):
        #self.readFile()

    def readFile(self):
        fileName = "vectorDB.json"

        '''
        if not os.path.isfile(fileName):
            print("File not found")
        else:
            with open(fileName) as file:
                content = file.read().splitlines()

                for line in content:
                    entryDB.append(line)
        '''
        with open(fileName, "r") as json_file:
            #tempList = json.load(json_file)

            self.entryDB = []

            while True:
                line = json_file.readline()

                if not line:
                    break

                #Non-Functional, Entity not taking correct parameters in constructor??
                #EntityE = self.Entity(**json.loads(line))

                dataDictionary = json.loads(line)
                
                EntityE = self.Entity(dataDictionary["courseDescription"], dataDictionary["vector"])

                self.entryDB.append(EntityE)

    #Cycle through the CourseCatalog file until all courses are vectorized and stored in vectorDB. 
    def updateVectorDB(self, courseCatalogFileName: str):
        courseDescription = ""

        with open(fileName, "r") as json_file:

            while True:
                line = json_file.readline()

                if not line:
                    break

                courseDescription += line

                if line == "\n":
                    self.addEntry(courseDescription)
                    courseDescription = ""
            
            self.writeFile()


    def writeFile(self):
        fileName = "vectorDB.json"

        '''
        if not os.path.isfile(fileName):
            print("File not found")

        else:
            file1 = open("vectorDB.txt")
            for x in entryDB:
                file1.writelines(x)

            file1.close()
        '''
        
        with open(fileName, "w") as json_file:
            for x in self.entryDB:
                temp = json.dumps(x.__dict__)
                json_file.writelines(temp + "\n")
        
    def getVector(self, userInput):
        modelType = "text-embedding-3-small"
        query = userInput

        url = "https://api.openai.com/v1/embeddings"

        payload = json.dumps({
        "model": modelType,
        "input": query
        })

        #Need to hide Authorization key here \/

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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',
        'Cookie': '__cf_bm=MyXTuajJDs2sfXyQPOsLBrgeUEhYfuD_e9p9eyWCmT8-1707591857-1-AdAv1O+w3r+YesTnNNvqWEPSCbzMSkSUVn/FbneGZgfIRHfRrI/hJOtpFiIQN5NcL7i2UpYL2PRDotczLdF68Ko=; _cfuvid=OnX782w1UPhMSvrliOKLtv5U603FU9F_az9j33S5x7I-1707591545673-0-604800000'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        apiData = response.json()

        return apiData.get("data")[0].get("embedding")
    

    def compareVector(self, vector1, vector2):
        comparisonScore = 0

        minRange = min(len(vector1), len(vector2))

        for i in range(minRange):
            comparisonScore += vector1[i] * vector2[i]
        
        return comparisonScore
    
    def addEntry(self, userInput):
        vector = self.getVector(userInput)

        entityE = self.Entity(userInput, vector)

        self.entryDB.append(entityE)

        #self.writeFile()

        #self.readFile()

C = ContentStore()
#C.addEntry("What color is the sky?")

C.updateVectorDB("courseCatalog.txt")






    


