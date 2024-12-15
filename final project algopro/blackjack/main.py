import copy
import random
import pygame
from button_class import Button

pygame.init()
#game variables
cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Pixel jack")
fps = 60
timer = pygame.time.Clock()

#font
font = pygame.font.Font('font.ttf',44) 
bigger_font = pygame.font.Font('font.ttf',55)
smaller_font = pygame.font.Font('font.ttf',36)
font1 = pygame.font.Font('font1.ttf',40)
smaller_font1 = pygame.font.Font('font1.ttf',24)
active = False
smaller_font_deal = pygame.font.Font('font.ttf',15)
card_font = pygame.font.Font('card_font.ttf',47)
smaller_font_newhand = pygame.font.Font('font.ttf',27)

#colors
brown_color = (210, 180, 140)
blue_color = (255, 210, 220)
green_color = (41, 67, 26)
lightgreen_color = (197, 214, 122, 1)
darkgreen_color = (25, 43, 17, 1)
cream = (254,251,234)
broken_white = (248,247,243)

#win, loss, draw/push
records = [0,0,0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['','PLAYER BUSTED!','  PLAYER WINS!!!','   DEALER WINS...','        TIE GAME']

#initialize logo
logo = pygame.image.load('logo.png')

logo_image = pygame.transform.scale(logo, (470, 205))

logo_button = Button(logo_image, 70, 180)


#music
is_music_playing = False
is_music_paused = False

#initialize music button
music_on_image = pygame.image.load('Sound On JPEG.jpeg')
music_off_image = pygame.image.load('Sound Off JPEG.jpeg')

music_on_image = pygame.transform.scale(music_on_image, (70, 50))
music_off_image = pygame.transform.scale(music_off_image, (70, 50))

music_button = Button(music_off_image, 535, 9)

#initialize quit button
quit_image = pygame.image.load('exit.png')

quit_image = pygame.transform.scale(quit_image, (180, 90))
quit_button = Button(quit_image, 210, 570)


#import new hand sound
new_hand_sound = pygame.mixer.Sound('deal_hand.mp3')

#import default button sound
default_button_sound = pygame.mixer.Sound('defaultclick.mp3')
default1_button_sound = pygame.mixer.Sound('defaultclick1.mp3')

#initialize ?? image
unknown_card = pygame.image.load('card1.png')
unknown_card = pygame.transform.scale(unknown_card, (114, 215))

unknown_button = Button(unknown_card, 73, 11)

#initialize popup image
popup_image = pygame.image.load('popup.png')
popup_image = pygame.transform.scale(popup_image, (500, 180))

popup_button = Button(popup_image, 44, 185)


#deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    try:
        card = random.randint(0, len(current_deck))
        current_hand.append(current_deck[card - 1])
        current_deck.pop(card - 1)
        return current_hand, current_deck
    except IndexError as e:
        print(f'Error: Tried to deal from an empty deck. {e}')
        return current_hand, current_deck # Return hands unchanged if error occurs
    except Exception as e:
        print(f'Unexpected error while dealing cards: {e}')
        return current_hand, current_deck # Return hands unchanged if unexpected error occurs


#draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font1.render(f'[{player}]', True, 'white'), (480, 400))
    if reveal_dealer:
        screen.blit(font1.render(f'[{dealer}]', True, 'white'), (480, 100))


#draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 310 + (5 * i), 120, 220], 0, 5)
        screen.blit(card_font.render(player[i], True,'black'),(80 + 70 * i, 310 + 5 * i))
        screen.blit(card_font.render(player[i], True,'black'),(80 + 70 * i, 475 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 310 + (5 * i), 120, 220], 5, 5)

    #if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70*i), 10 + (5*i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(card_font.render(dealer[i], True,'black'),(80 + 70*i, 15 + 5*i))
            screen.blit(card_font.render(dealer[i], True,'black'),(80 + 70*i, 175 + 5*i))
        else: 
            unknown_button.draw(screen)
        pygame.draw.rect(screen, 'blue', [70 + (70*i), 10 + (5*i), 120, 220], 5, 5)

def calculate_score(hand):
    #calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range (len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int (hand[i])
        #for 10 and face cards, add 10
        if hand [i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        #for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
        #determine how many need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

#draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    #initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, blue_color, [150, 400, 300, 95], 0, 10)
        pygame.draw.rect(screen, 'black', [150, 400, 300, 95], 5, 10)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (190,410))
        deal1_text = smaller_font_deal.render('[ PRESS BUTTON ]', True, 'black')
        screen.blit(deal1_text, (240,465))
        button_list.append(deal)
        
        quit_button.draw(screen)
        logo_button.draw(screen)

#once game started, shot hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(screen, brown_color, [0, 560, 300, 90], 0, 5)
        pygame.draw.rect(screen, 'black', [0, 560, 300, 90], 5, 5)
        hit_text = font.render('HIT', True, 'black')
        screen.blit(hit_text, (110,580))
        button_list.append(hit)
        
        stand = pygame.draw.rect(screen, cream, [300, 560, 300, 90], 0, 5)
        pygame.draw.rect(screen, 'black', [300, 560, 300, 90], 5, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (378, 580))
        button_list.append(stand)
        
        score_text = smaller_font1.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text,(62, 687))

    #if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        
        shadow_offset = (7, 7)  # Offset for shadow
        shadow_rect = pygame.Rect(52 + shadow_offset[0], 194 + shadow_offset[1], 494, 174)  # Shadow behind button
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, 0, 10)  # Draw the shadow (darker color)
        popup_button.draw(screen)
        #pygame.draw.rect(screen, green_color, [42, 180, 505, 190], 9, 12)
        
        shadow_offset = (5, 5)  # Shadow offset for the "NEW HAND" button
        shadow_rect = pygame.Rect(180 + shadow_offset[0], 287 + shadow_offset[1], 225, 45)  # Shadow behind button
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, 0, 5)  # Draw dark shadow
        screen.blit(bigger_font.render(results[result], True, green_color), (95, 213))
        deal = pygame.draw.rect(screen, broken_white, [180, 287, 225, 45], 0, 5)
        pygame.draw.rect(screen, lightgreen_color, [180, 287, 225, 45], 3, 5)
        deal_text = smaller_font_newhand.render('NEW HAND', True, darkgreen_color)
        screen.blit(deal_text, (230,293))
        button_list.append(deal)
    return button_list

#check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    #check end game scenarios if player has stood, busted or blackjacked
    #result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score>21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

#main game loop
run = True
while run:
    #run game at framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('#06402B')
    #initial deal to player and dealer
    if initial_deal:
        for i in range (2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    #once game is activated , and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

    music_button.draw(screen)
    buttons = draw_game(active, records, outcome)
    
    #event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                
                if music_button.checkForInput(mouse_pos):
                    if is_music_playing:
                        if is_music_paused:
                            pygame.mixer.music.unpause()
                            is_music_paused = False  
                            
                        else:
                            pygame.mixer.music.pause()
                            is_music_paused = True
                        music_button.image = music_off_image if is_music_paused else music_on_image     
                    else:
                        pygame.mixer.music.load('music_1.mp3')
                        pygame.mixer.music.play(loops=-1)
                        is_music_playing = True
                        is_music_paused = False
                        music_button.image = music_on_image
                 
                if quit_button.checkForInput(mouse_pos):
                    run = False  # Close the game when Quit button is clicked


            if not active:
                if buttons[0].collidepoint(event.pos):
                    #play the new hand button sound
                    new_hand_sound.play()
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
                    outcome = 0                 
                    
            else:
                #if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    default_button_sound.play()
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    player_score = calculate_score(my_hand)
                
                #allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    default_button_sound.play()
                    reveal_dealer = True
                    hand_active = False
                if quit_button.checkForInput(mouse_pos):
                    run = True
                
                elif len(buttons)== 3:
                    if buttons[2].collidepoint(event.pos):
                        default1_button_sound.play()
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                    if quit_button.checkForInput(mouse_pos):
                        run = True
                

    #if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
            
    pygame.display.flip()
pygame.quit()

