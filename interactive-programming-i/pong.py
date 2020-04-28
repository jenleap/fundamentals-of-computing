# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2] 
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
score1 = 0
score2 = 0
winner = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if direction == "LEFT":
        ball_vel[0] = - random.randrange(120, 240) / 60
    else:
        ball_vel[0] = random.randrange(120, 240) / 60
        
    ball_vel[1] = - random.randrange(60, 180) / 60

# define event handlers
def new_game():    
    if winner == 1:
       spawn_ball("LEFT")
    else:
       spawn_ball("RIGHT")
   
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, winner
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
         
    # collide and reflect off bottom of canvas
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] =  - ball_vel[1]
        
    # collide and reflect off top of canvas
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] =  - ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_vel[1] < 0:
        if (paddle1_pos[1] - HALF_PAD_HEIGHT >= 0):
            paddle1_pos[1] = paddle1_pos[1] + paddle1_vel[1]
    elif paddle1_vel[1] > 0:
        if (paddle1_pos[1] + HALF_PAD_HEIGHT <= HEIGHT):
            paddle1_pos[1] = paddle1_pos[1] + paddle1_vel[1]
    
    if paddle2_vel[1] < 0:
        if (paddle2_pos[1] - HALF_PAD_HEIGHT >= 0):
            paddle2_pos[1] = paddle2_pos[1] + paddle2_vel[1]
    elif paddle2_vel[1] > 0:
        if (paddle2_pos[1] + HALF_PAD_HEIGHT <= HEIGHT):
            paddle2_pos[1] = paddle2_pos[1] + paddle2_vel[1]
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos[1] - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT), (0, paddle1_pos[1] + HALF_PAD_HEIGHT)], 5, "Green")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)], 5, "Green")
    
    # determine whether paddle and ball collide   
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] =  - ball_vel[0]
        else:
            score1 += 1
            winner = 1
            new_game()
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
        else:
            score2 += 1
            winner = 2
            new_game()
    
    # draw scores
    canvas.draw_text(str(score1), (50, 30), 30, "White")
    canvas.draw_text(str(score2), (WIDTH - 50, 30), 30, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if chr(key) == 'W':
        paddle1_vel[1] = -1
    elif chr(key) == 'S':
        paddle1_vel[1] = 1
    elif chr(key) == '&':
        paddle2_vel[1] = -1
    elif chr(key) == '(':
        paddle2_vel[1] = 1
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if chr(key) == 'W' or chr(key) == 'S':
        paddle1_vel[1] = 0
    elif chr(key) == '&' or chr(key) == '(':
        paddle2_vel[1] = 0
        
def reset_game():
    global score1, score2, winner, paddle1_pos, paddle2_pos
    
    winner = 0

    score1 = 0
    score2 = 0
    
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2] 
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]

    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset_game, 200)


# start frame
new_game()
frame.start()
