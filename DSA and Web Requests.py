from collections import deque
from collections import defaultdict
import requests

apiKey = "69769964D41B7AAA6C41B8C8D98538B2"


class SteamAccount:

    maxIndex = 0

    def __init__(self, ID):
        self.ID = ID
        self.index = SteamAccount.maxIndex
        SteamAccount.maxIndex += 1

    def __eq__(self, other):
        return self.ID == other.ID
    
    # Returns a list of the steam IDs of the SteamAccount's friends
    def getFriendList(self):
        req = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apiKey}&steamid={self.ID}&relationship=friend")

        ids = []
        numIDs = 0
        for user in req.json()['friendslist']['friends']:
            numIDs += 1
            ids.append(user['steamid'])
        print(f"Total IDs: {numIDs}")
        return ids
    
    # Returns a list of usernames corresponding to the input steam ID list. Static Function.
    def getAccountNames(steamIDs):
        # The request can only handle up to 100 IDs at once.
        # Solution: Slice the ID list into blocks of 100 IDs each
        blocks = []
        for i in range(0, len(steamIDs), 100):
            blocks.append(steamIDs[i:i+100])
        
        names = []
        numNames = 0
        for steamIDList in blocks:
            print(f"Block Length: {len(steamIDList)}")
            steamIDstr = ",".join(steamIDList)
            req = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apiKey}&steamids={steamIDstr}")

            for user in req.json()['response']['players']:
                numNames += 1
                names.append(user['personaname'])

        print(f"Total Names: {numNames}")
        return names

class AdjListGraph:

    def __init__(self, source):
        self.source = source
        self.graph = defaultdict(list)

        
    def findConnection(self, target, maxDegrees):
        queue = deque([self.source])
        visited = set((self.source))
        pathLength = 0 # Length of path from source to target, if found.

        while queue and not pathLength > maxDegrees:
            pathLength += 1
            for i in range(len(queue)):
                current = queue.popleft()
                for child in self.graph[current]:
                    if child == target:
                        return pathLength
                    elif child not in visited:
                        queue.append(child)
                        visited.add(child)
        return -1
    
    def insertEdge(self, source, target):
        self.graph[source].append(target)

    def printGraph(self):
        queue = deque([self.source])
        visited = set((self.source))
        
        while queue:
            current = queue.popleft()
            print(f"ID: {current}, # of Friends: {current.numFriends}")

            for child in self.graph[current]:
                if child not in visited:
                    visited.add(child)
                    queue.append(child)


class AdjMatrixGraph:

    def __init__(self, source):
        self.source = source
        self.graph = []
        self.indexToID = {}

    def findConnection(self, target, maxDegrees):
        queue = deque([self.source.index])
        visited = set((self.source.index))
        pathLength = 0 # Length of path from source to target, if found.

        while queue and not pathLength > maxDegrees:
            pathLength += 1
            for i in range(len(queue)):
                current = queue.popleft()
                for index, exists in enumerate(self.graph[current]):
                    if not exists:
                        continue
                    if self.indexToID[index] == target:
                        return pathLength
                    elif index not in visited:
                        queue.append(index)
                        visited.add(index)
        return -1
    
    def insertEdge(self, source, target):
        if len(self.graph) > max(source.index, target.index):
            self.graph.extend([False] * max(source.index, target.index) - len(self.graph))
        

        if len(self.graph[source.index]) > target.index:
            self.graph[source.index].extend([False] * target.index - len(self.graph[source.index]))
        
        self.graph[source.index][target.index] = True
        
        if len(self.graph[target.index]) > source.index:
            self.graph[target.index].extend([False] * source.index - len(self.graph[target.index]))
        
        self.graph[target.index][source.index] = True

        self.indexToID[source.index] = source.id
        self.indexToID[target.index] = target.id

    def printGraph(self):
        queue = deque([self.source])
        visited = set((self.source))
        
        while queue:
            current = queue.popleft()
            print(f"ID: {self.indexToID[current]}, # of Friends: {self.indexToID[current].numFriends}")

            for index, exists in enumerate(self.graph[current]):
                if index not in visited and exists:
                    visited.add(index)
                    queue.append(index)    


def buildGraphs(source):
    queue = deque([source])
    visited = set((source))
    depth = 0

    adjListFriends = AdjListGraph(source)
    adjMatrixFriends = AdjMatrixGraph(source)

    while queue and not depth > 3:
        depth += 1
        for i in range(len(queue)):
            current = queue.popleft()
            for friend in current.getFriendList():
                if friend not in visited:
                    queue.append(friend)
                    visited.add(friend)
                    friendAcc = SteamAccount(friend)
                    adjListFriends.insertEdge(current, friendAcc)
                    adjMatrixFriends.insertEdge(current, friendAcc)

