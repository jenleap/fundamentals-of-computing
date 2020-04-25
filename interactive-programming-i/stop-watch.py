import simplegui
import math

# define global variables
current_time = 0
stops = 0
wins = 0
is_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    milliseconds = t % 10
    seconds = t / 10
    minutes = int(math.floor(seconds / 60))
    formatted_seconds = seconds % 60
    if (formatted_seconds < 10):
        formatted_seconds = "0" + str(formatted_seconds)
    else:
        formatted_seconds = str(formatted_seconds)
    
    return str(minutes) + ":" + formatted_seconds + ":" + str(milliseconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global timer, is_running
    timer.start()
    is_running = True
    
def stop_timer():
    global timer, is_running, stops, wins, current_time
    timer.stop()
    if is_running:
        is_running = False
        stops += 1
        if (current_time % 10 == 0):
            wins += 1
    
def reset_timer():
    global timer, current_time, is_running, stops, wins
    timer.stop()
    current_time = 0
    wins = 0
    stops = 0
    is_running = False

# define event handler for timer with 0.1 sec interval
def tick():
    global current_time
    current_time += 1

# define draw handler
def draw(canvas):
    global current_time, stops, wins
    timer_text = format(current_time)
    wins_text = str(wins) + "/" + str(stops)
    canvas.draw_text(timer_text, [50, 50], 40, "White")
    canvas.draw_text(wins_text, [200, 50], 24, "Pink")

# create frame
frame = simplegui.create_frame("Timer", 300, 300)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start_timer, 200)
frame.add_button("Stop", stop_timer, 200)
frame.add_button("Reset", reset_timer, 200)
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()
