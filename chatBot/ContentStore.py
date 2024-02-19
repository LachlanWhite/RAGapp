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
        
        def getVector(self):
            return self.vector
        
        def getCourseDescription(self):
            return self.courseDescription

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

        with open(courseCatalogFileName, "r") as file:

            line = " "

            while line:
                line = file.readline()
                while line != "\n":
                    
                    if not line:
                        break

                    courseDescription += line
                    line = file.readline()

                ### UNCOMMENT LINE TO FUNCTION
                if len(courseDescription) > 0:
                    print(courseDescription)
                    #self.addEntry(courseDescription)

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
    
    #Return a list of chunks that are relevant to the prompt, given a query's vector and the temperature
    def getRelevantChunks(self, queryVector):
        relevantChunks = []

        # THIS IS WHERE TO CHANGE HOW SENSITIVE THE FILTER IS
        temperatureSensitivity = 1

        for x in self.entryDB:
            score = self.compareVector(x.getVector(), queryVector)

            if(score > temperatureSensitivity):
                relevantChunks.append(x.getCourseDescription())

        return relevantChunks
    
    def addEntry(self, userInput):
        vector = self.getVector(userInput)

        entityE = self.Entity(userInput, vector)

        self.entryDB.append(entityE)

    #Returns prompt given userQuery, DOES *NOT* INCLUDE THE QUERY!!!!
    def getPrompt(self, userQuery: str, temperature: float):
        #take user query + temp
        #Compare to DB vectors, using temperature as threshold
        #return relevant chunks + query
        prompt = "Prompt: You are a helpful chatbot that answers questions surrounding different courses offered at the University of Washington. Here are the course descriptions:\n"

        vecQuery = self.getVector(userQuery)

        relChunks = self.getRelevantChunks(vecQuery)

        for x in relChunks:
            prompt += x + "\n"

        return prompt

C = ContentStore()
#C.addEntry("What color is the sky?")

#C.updateVectorDB("courseCatalog.txt")

myPrompt = C.getPrompt("What prerequisite courses are required to take CSS 143?")
