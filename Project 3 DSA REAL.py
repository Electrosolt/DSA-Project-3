import pygame, sys
from collections import deque
from collections import defaultdict
import requests

pygame.init()

apiKey = "69769964D41B7AAA6C41B8C8D98538B2"

class SteamAccount:

    maxIndex = 0

    def __init__(self, ID):
        self.ID = ID
        self.index = SteamAccount.maxIndex
        SteamAccount.maxIndex += 1

    def __eq__(self, other):
        return self.ID == other.ID

    def __hash__(self):
        return hash((self.ID, self.index))
    
    # Returns a list of the steam IDs of the SteamAccount's friends
    def getFriendList(self):
        req = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apiKey}&steamid={self.ID}&relationship=friend")

        ids = []
        numIDs = 0

        #print(f"Request Result: {req.json()}")
        if len(req.json()) == 0:
            return []
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

    def __init__(self, source = None):
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

    def __init__(self, source = None):
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
        
        for i in range(target.index - len(self.graph)+ 1):
            self.graph.append([])

        if len(self.graph[source.index]) - 1 < target.index:
            self.graph[source.index].extend([False] * (target.index - len(self.graph[source.index]) + 1))
 
        #print(f"Adding Edge. Source Index: {source.index}, Target Index: {target.index}")

        self.graph[source.index][target.index] = True

        
        if len(self.graph[target.index]) - 1 < source.index:
            self.graph[target.index].extend([False] * (target.index - len(self.graph[target.index]) + 1))
        
        self.graph[target.index][source.index] = True

        self.indexToID[source.index] = source.ID
        self.indexToID[target.index] = target.ID

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

adjacencyListGraph = AdjListGraph()
adjacencyMatrixGraph = AdjMatrixGraph()

def buildGraphs(sourceID):
    sourceID = 76561197960435530
    source = SteamAccount(sourceID)
    queue = deque([source])
    visited = set()
    visited.add(source)
    depth = 0

    adjacencyListGraph.source = sourceID
    adjacencyMatrixGraph.source = sourceID

    while queue and not depth > 3:
        depth += 1
        for i in range(len(queue)):
            current = queue.popleft()
            print(f"Current: {current} with ID {current.ID}")
            friendList = current.getFriendList()
            #print(friendList)
            for friend in friendList:
                if friend not in visited:
                    friendAcc = SteamAccount(friend)
                    queue.append(friendAcc)
                    visited.add(friendAcc)
                    adjacencyListGraph.insertEdge(current, friendAcc)
                    adjacencyMatrixGraph.insertEdge(current, friendAcc)

# UI
# Create colors
size = width, height = 1280, 720
white = 255, 255, 255
black = 0, 0, 0
activeColor = pygame.Color('lightskyblue2')
passiveColor = pygame.Color('gray30')
pretty = pygame.Color('cadetblue4')
background = pygame.Color('grey8')
sourceColor = passiveColor
searchColor = passiveColor
searchBoxColor = passiveColor

# Set values of UI variables
sourceActive = False
searchActive = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Six Degrees of Steam Separation')
base_font = pygame.font.SysFont('monospace', 32, True)
title_font = pygame.font.Font(None, 70)
user_text = ''
search_text = ''
textWidth, textHeight = base_font.size("a")
moveLeft1 = 0
moveLeft2 = 0
running = True
graphCreated = False

# Create text boxes and buttons
inputBox = pygame.Rect(250, 250, 400, 40)
searchBox = pygame.Rect(250, 400, 400, 40)
blackBox = pygame.Rect(-140, 250, 400, 40)
blackBox2 = pygame.Rect(-140, 400, 400, 40)
toSearch = pygame.Rect(740, 400, 21 *  textWidth + 22, 40)
printBox = pygame.Rect(300, 550, 11 * textWidth + 22, 40)
createBox = pygame.Rect(740, 250, 24 * textWidth + 22, 40)

# Render permanent text
box1 = base_font.render('Search from:', True, white) 
box2 = base_font.render('Search to:', True, white) 
printHere = base_font.render('Print graph', True, white) 
searchText = base_font.render('Search for connection', True, white) 
createText = base_font.render('Create graph with source', True, white) 
title = title_font.render('Six Degrees of Steam Separation', True, white) 

# Search for connection when enter is pressed or search button is clicked
def Search(source, search):

    print(adjacencyListGraph.findConnection(search, 3))
    adjacencyMatrixGraph.findConnection(search, 3)

def CreateGraph(source):

    buildGraphs(source)
    

# Program loop
while running:

    backTouched = False

    # Deal with any events
    for event in pygame.event.get():

        # If the program is quit
        if event.type == pygame.QUIT: 

            running = False
            pygame.quit()
            sys.exit()

        # IF the user clicks...
        if event.type == pygame.MOUSEBUTTONDOWN:

            # ...on the source text box
            if inputBox.collidepoint(event.pos):

                # Activate source box
                sourceActive = True
                sourceColor = activeColor
                searchActive = False
                searchColor = passiveColor

            # ...on the search text box
            elif searchBox.collidepoint(event.pos):

                # Activate search box
                sourceActive = False
                sourceColor = passiveColor
                searchActive = True
                searchColor = activeColor

            # ...on the search button
            elif toSearch.collidepoint(event.pos):

                # Reset text boxes and search for connection, if a graph is created
                if graphCreated:

                    Search(user_text, search_text)
                    user_text = ''
                    search_text = ''

                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor

            # ...on the print button
            elif printBox.collidepoint(event.pos):

                # Print the graph
                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor

            # ...on the create button
            elif createBox.collidepoint(event.pos):

                # Create a graph using the source
                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor
                CreateGraph(user_text)
                graphCreated = True

            # ...on anything else
            else:

                # Deactivate the text boxes
                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor

        # If a key is pressed when source text box is active
        if event.type == pygame.KEYDOWN and (sourceActive == True):

            # If backspace is hit
            if event.key == pygame.K_BACKSPACE:

                # Reset text
                backTouched = True
                user_text = user_text[0:-1]

                # Move text right if beyond bounds of box
                if len(user_text) > 20:

                    moveLeft1 -= textWidth

                else:

                    moveLeft1 = 0

                clock.tick(7)
              
            # If enter is hit
            elif event.key == pygame.K_RETURN:

                # Reset text boxes and search for connection
                Search(user_text, search_text)
                user_text = ''
                search_text = ''

            # If any other character, up to max length, is hit
            elif len(user_text) < 64:

                # Add to text
                user_text += event.unicode

                # Move text left if beyond bounds of box, hidden behind blackBox
                if len(user_text) > 20:

                    moveLeft1 += textWidth

                else:

                    moveLeft1 = 0

        # If a key is pressed when source text box is active
        elif event.type == pygame.KEYDOWN and searchActive == True:

            # If backspace is hit
            if event.key == pygame.K_BACKSPACE:

                # Reset text
                backTouched = True
                search_text = search_text[0:-1]

                # Move text right if beyond bounds of box
                if len(search_text) > 20:

                    moveLeft2 -= textWidth

                else:

                    moveLeft2 = 0

                clock.tick(7)

            # If enter is hit
            elif event.key == pygame.K_RETURN:

                # Reset text boxes and search for connection
                Search(user_text, search_text)
                user_text = ''
                search_text = ''

            # If any other character, up to max length, is hit
            elif len(search_text) < 64:

                # Add to text
                search_text += event.unicode

                # Move text left if beyond bounds of box, hidden behind blackBox
                if len(search_text) > 20:

                    moveLeft2 += textWidth

                else:

                    moveLeft2 = 0        
    
    keys = pygame.key.get_pressed()

    # Add holding support for backspace, to continously remove text
    if keys[pygame.K_BACKSPACE] and backTouched == False:

        # Source text box
        if sourceActive:

            user_text = user_text[0:-1]

            if len(user_text) > 20:

                moveLeft1 -= textWidth

            else:

                moveLeft1 = 0

            clock.tick(7)

        # Search text box
        elif searchActive:

            search_text = search_text[0:-1]

            if len(search_text) > 20:

                moveLeft2 -= textWidth

            else:

                moveLeft2 = 0

            clock.tick(7)

    # Screen and text
    screen.fill(background)
    text_surface = base_font.render(user_text, True, white)
    search_surface = base_font.render(search_text, True, white)

    # Draw user text
    screen.blit(text_surface, (inputBox.x + 11 - moveLeft1, inputBox.y + 2))
    screen.blit(search_surface, (searchBox.x + 11 - moveLeft2, searchBox.y + 2))
 
    if graphCreated:

        searchBoxColor = pretty

    # Draw all rectangles
    pygame.draw.rect(screen, background, blackBox)
    pygame.draw.rect(screen, sourceColor, inputBox, 2)
    pygame.draw.rect(screen, background, blackBox2)
    pygame.draw.rect(screen, searchColor, searchBox, 2)
    pygame.draw.rect(screen, searchBoxColor, toSearch)
    pygame.draw.rect(screen, pretty, printBox)
    pygame.draw.rect(screen, pretty, createBox)

    # Draw all permanent text
    screen.blit(box1, (inputBox.x - 235, inputBox.y + 2))
    screen.blit(box2, (searchBox.x - 235 + 2 * textWidth, searchBox.y + 2))
    screen.blit(printHere, (printBox.x + 11, printBox.y + 2))
    screen.blit(title, (240, 40))
    screen.blit(searchText, (toSearch.x + 11, toSearch.y + 2))
    screen.blit(createText, (createBox.x + 11, createBox.y + 2))

    # Complete the program loop
    pygame.display.flip()
    clock.tick(60)
