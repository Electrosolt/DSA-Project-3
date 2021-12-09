import sys, pygame
pygame.init()

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

# Create text boxes and buttons
inputBox = pygame.Rect(250, 250, 400, 40)
searchBox = pygame.Rect(250, 400, 400, 40)
blackBox = pygame.Rect(-140, 250, 400, 40)
blackBox2 = pygame.Rect(-140, 400, 400, 40)
toSearch = pygame.Rect(800, 325, 21 *  textWidth + 22, 40)
printBox = pygame.Rect(300, 550, 11 * textWidth + 22, 40)

# Render permanent text
box1 = base_font.render('Search from:', True, white) 
box2 = base_font.render('Search to:', True, white) 
printHere = base_font.render('Print graph', True, white) 
searchText = base_font.render('Search for connection', True, white) 
title = title_font.render('Six Degrees of Steam Separation', True, white) 

# Search for connection when enter is pressed or search button is clicked
def Search(source, search):

    print('Source: ', source)
    print('Target: ', search)

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

                # Reset text boxes and search for connection
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
 
    # Draw all rectangles
    pygame.draw.rect(screen, background, blackBox)
    pygame.draw.rect(screen, sourceColor, inputBox, 2)
    pygame.draw.rect(screen, background, blackBox2)
    pygame.draw.rect(screen, searchColor, searchBox, 2)
    pygame.draw.rect(screen, pretty, toSearch)
    pygame.draw.rect(screen, pretty, printBox)

    # Draw all permanent text
    screen.blit(box1, (inputBox.x - 235, inputBox.y + 2))
    screen.blit(box2, (searchBox.x - 235 + 2 * textWidth, searchBox.y + 2))
    screen.blit(printHere, (printBox.x + 11, printBox.y + 2))
    screen.blit(title, (240, 40))
    screen.blit(searchText, (toSearch.x + 11, toSearch.y + 2))

    # Complete the program loop
    pygame.display.flip()
    clock.tick(60)
