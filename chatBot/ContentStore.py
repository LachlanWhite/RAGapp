import os.path
import requests
import json

class ContentStore:
    chunkDB = []

    def __init__(self):
        self.populateChunkDB("vectorDB.json")

    class Entity:
        chunk = ""
        vector = []

        def __init__(self, c: str, v: []):
            self.chunk = c
            self.vector = v
        
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys = True, indent = 4)
        
        def getVector(self):
            return self.vector
        
        def getChunk(self):
            return self.chunk

    def populateChunkDB(self, fileName):

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

            self.chunkDB = []

            while True:
                line = json_file.readline()

                if not line:
                    break

                dataDictionary = json.loads(line)
                
                EntityE = self.Entity(dataDictionary["chunk"], dataDictionary["vector"])

                self.chunkDB.append(EntityE)

    #UpdateChunkDB: Wipes chunkDB and rewrites using given file of chunks (no vectors incl). Parameters are String
    def updateChunkDB(self, courseCatalogFileName: str):
        chunk = ""

        with open(courseCatalogFileName, "r") as file:

            line = " "

            while line:
                line = file.readline()
                while line != "\n":
                    
                    if not line:
                        break

                    chunk += line
                    line = file.readline()

                ### UNCOMMENT LINE TO FUNCTION
                if len(chunk) > 0:
                    print(chunk)
                    self.addEntry(chunk)

                chunk = ""
            
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
            for x in self.chunkDB:
                temp = json.dumps(x.__dict__)
                json_file.writelines(temp + "\n")
        
    #GetVector: Vectorizes string, returns list of floats (vector), parameters are STRING
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
        'Authorization': os.getenv('AUTH_TOKEN'),
        'Cookie': os.getenv('COOKIE')
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        apiData = response.json()

        return apiData.get("data")[0].get("embedding")
    
    #CompareVector: Compares 2 vectors by calculating the dot product. Returns float value between -1 to 1. Parameters are List(float), List(float)
    def compareVector(self, vector1, vector2):
        comparisonScore = 0

        minRange = min(len(vector1), len(vector2))

        for i in range(minRange):
            comparisonScore += vector1[i] * vector2[i]
        
        return comparisonScore
    
    #GetRelevantChunks: Compares query to all vectors in global class database using a match score. Returns List(STRING) of relevant chunks. Parameters are List(float), float
    def getRelevantChunks(self, queryVector, matchScore: float):
        relevantChunks = []

        for x in self.chunkDB:
            score = self.compareVector(x.getVector(), queryVector)

            if(score > matchScore):
                relevantChunks.append(x.getChunk())

        return relevantChunks
    
    def addEntry(self, userInput):
        vector = self.getVector(userInput)

        entityE = self.Entity(userInput, vector)

        self.chunkDB.append(entityE)

    #Returns prompt given userQuery, DOES *NOT* INCLUDE THE QUERY!!!!
    def createPrompt(self, userQuery: str, matchScore: float):
        #take user query + temp
        #Compare to DB vectors, using temperature as threshold
        #return relevant chunks + query
        prompt = "Prompt: You are a helpful chatbot that answers questions surrounding different courses offered at the University of Washington. Here are the course descriptions:\n"

        vecQuery = self.getVector(userQuery)

        relChunks = self.getRelevantChunks(vecQuery, matchScore)

        for x in relChunks:
            prompt += x + "\n"

        return prompt
    
C = ContentStore()
#C.addEntry("What color is the sky?")

#C.updateVectorDB("courseCatalog.txt")

myPrompt = C.createPrompt("What prerequisite courses are required to take CSS 350?", 0.66)

