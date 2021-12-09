import sys, pygame
pygame.init()

size = width, height = 1280, 720
white = 255, 255, 255
black = 0, 0, 0
activeColor = pygame.Color('lightskyblue2')
passiveColor = pygame.Color('gray30')
pretty = pygame.Color('cadetblue4')
background = pygame.Color('grey8')
sourceColor = passiveColor
searchColor = passiveColor

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

inputBox = pygame.Rect(250, 250, 400, 40)
searchBox = pygame.Rect(250, 400, 400, 40)
blackBox = pygame.Rect(-140, 250, 400, 40)
blackBox2 = pygame.Rect(-140, 400, 400, 40)
toSearch = pygame.Rect(800, 325, 21 *  textWidth + 22, 40)
printBox = pygame.Rect(300, 550, 11 * textWidth + 22, 40)

box1 = base_font.render('Search from:', True, white) 
box2 = base_font.render('Search to:', True, white) 
printHere = base_font.render('Print graph', True, white) 
searchText = base_font.render('Search for connection', True, white) 
title = title_font.render('Six Degrees of Steam Separation', True, white) 

moveLeft1 = 0
moveLeft2 = 0

def Search(source, search):

    print('Source: ', source)
    print('Target: ', search)

while 1:

    backTouched = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT: 

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if inputBox.collidepoint(event.pos):

                sourceActive = True
                sourceColor = activeColor
                searchActive = False
                searchColor = passiveColor

            elif searchBox.collidepoint(event.pos):

                sourceActive = False
                sourceColor = passiveColor
                searchActive = True
                searchColor = activeColor

            elif toSearch.collidepoint(event.pos):

                Search(user_text, search_text)
                user_text = ''
                search_text = ''
                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor

            elif printBox.collidepoint(event.pos):

                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor

            else:

                sourceActive = False
                sourceColor = passiveColor
                searchActive = False
                searchColor = passiveColor

        if event.type == pygame.KEYDOWN and (sourceActive == True):

            if event.key == pygame.K_BACKSPACE:

                backTouched = True
                user_text = user_text[0:-1]

                if len(user_text) > 20:

                    moveLeft1 -= textWidth

                else:

                    moveLeft1 = 0

                clock.tick(7)
                    
            elif event.key == pygame.K_RETURN:

                Search(user_text, search_text)
                user_text = ''
                search_text = ''

            elif len(user_text) < 64:

                user_text += event.unicode

                if len(user_text) > 20:

                    moveLeft1 += textWidth

                else:

                    moveLeft1 = 0

        elif event.type == pygame.KEYDOWN and searchActive == True:

            if event.key == pygame.K_BACKSPACE:

                backTouched = True
                search_text = search_text[0:-1]

                if len(search_text) > 20:

                    moveLeft2 -= textWidth

                else:

                    moveLeft2 = 0

                clock.tick(7)

            elif event.key == pygame.K_RETURN:

                Search(user_text, search_text)
                user_text = ''
                search_text = ''

            elif len(search_text) < 64:

                search_text += event.unicode

                if len(search_text) > 20:

                    moveLeft2 += textWidth

                else:

                    moveLeft2 = 0        
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_BACKSPACE] and backTouched == False:

        if sourceActive:

            user_text = user_text[0:-1]

            if len(user_text) > 20:

                moveLeft1 -= textWidth

            else:

                moveLeft1 = 0

            clock.tick(7)

        elif searchActive:

            search_text = search_text[0:-1]

            if len(search_text) > 20:

                moveLeft2 -= textWidth

            else:

                moveLeft2 = 0

            clock.tick(7)

    screen.fill(background)
    text_surface = base_font.render(user_text, True, white)
    search_surface = base_font.render(search_text, True, white)

    screen.blit(text_surface, (inputBox.x + 11 - moveLeft1, inputBox.y + 2))
    screen.blit(search_surface, (searchBox.x + 11 - moveLeft2, searchBox.y + 2))
 
    pygame.draw.rect(screen, background, blackBox)
    pygame.draw.rect(screen, sourceColor, inputBox, 2)
    pygame.draw.rect(screen, background, blackBox2)
    pygame.draw.rect(screen, searchColor, searchBox, 2)
    pygame.draw.rect(screen, pretty, toSearch)
    pygame.draw.rect(screen, pretty, printBox)

    screen.blit(box1, (inputBox.x - 235, inputBox.y + 2))
    screen.blit(box2, (searchBox.x - 235 + 2 * textWidth, searchBox.y + 2))
    screen.blit(printHere, (printBox.x + 11, printBox.y + 2))
    screen.blit(title, (240, 40))
    screen.blit(searchText, (toSearch.x + 11, toSearch.y + 2))

    pygame.display.flip()
    clock.tick(60)
