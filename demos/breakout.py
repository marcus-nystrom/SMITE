"""
 Sample Breakout Game
 
 Adapted to PsychoPy from:
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""
 
# --- Import libraries used for this program
 
import math
import numpy as np
import os, sys

from psychopy import core, event, misc, visual, monitors, data, gui, monitors
import pandas as pd

# Insert the parent directory (where SMITE is) to path
curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)
sys.path.insert(0,os.path.dirname(curdir)) 
import SMITE
import helpers

# Get settings
eye_tracker_name = 'REDm'

MY_MONITOR = 'default'
SCREEN_WIDTH = 53
SCREEN_RES = (1920, 1080)
VIEWING_DIST = 65

mon = monitors.Monitor(MY_MONITOR) # Defi ned in defaults file
mon.setWidth(SCREEN_WIDTH)    # Width of screen (cm)
mon.setDistance(VIEWING_DIST) # Distance eye / monitor (cm) 
mon.setSizePix(SCREEN_RES)


# Show dialogue box
info = {'Enter your name':'your name', 'Eye tracking':[False, True]}
dictDlg = gui.DlgFromDict(dictionary=info,
        title='Breakout')
if dictDlg.OK:
    print(info)
else:
    print('User Cancelled')
    core.quit()
    
info['dateStr']= data.getDateStr()    
player_name = '_'.join([info['Enter your name'], info['dateStr']])

# Window set-up (the color will be used for calibration)
win = visual.Window(monitor = mon, screen = 1, 
                    units = 'pix', fullscr = True,
                    allowGUI = False)
                    
print(win.size)

core.wait(1) 
mouse = event.Mouse(win=win)
mouse.setVisible(False)

instruction_text = visual.TextStim(win,text='', wrapWidth = 600, height = 20)  
                    
c = core.Clock()
my_clock = core.Clock()
         
if info['Eye tracking']:
    eye_tracking = True 
else:
    eye_tracking = False

### Setup a PsychoPy window for calibration
if eye_tracking:

    settings = SMITE.get_defaults(eye_tracker_name)
    tracker = SMITE.Connect(settings)
    tracker.init()
    
    tracker.calibrate(win)
        
    # Start eye tracker
    tracker.start_recording()
        
    tracker.start_buffer(sample_buffer_length=10)
    core.wait(1)

# Define some colors
black = (0, 0, 0)
white = (1, 1, 1)
blue = (0, 0, 1)
 

screen_size = SCREEN_RES
game_rect = visual.Rect(win, SCREEN_RES[0], SCREEN_RES[1], units = 'pix')
mouse.setPos((0, -screen_size[1]/2 + 100))

# information about block position
nBlockRows = 3
 
# Number of blocks to create
blockcount = 16.0

block_width = screen_size[0] / blockcount
block_height = screen_size[1] / 20.0


def generate_blocks():
    ''' Generate a bunch of blocks '''
    blocks = []
    top = screen_size[1] / 2.0 - block_height * 2

    for row in range(nBlockRows):
        for column in range(0, int(blockcount-1)):
            block = Block(blue, (column + 1) * (block_width + 2)  - screen_size[0]/2, top)
            blocks.append(block)
            
        # Move the top of the next row down
        top -= block_height - 2
        print(top)
        
    return blocks
 
 
class Block():
    """This class represents each block that will get knocked out by the ball
    """
 
    def __init__(self, color, x, y):
        """ Constructor. Pass in the color of the block,
            and its x and y position. """

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = visual.Rect(win, block_width, block_height)
 
        # Fill the image with the appropriate color
        self.image.fillColor = color
 
        # Fetch the rectangle object that has the dimensions of the image
        self.image.pos = (x, y)
  
 
class Ball():
    """ This class represents the ball
    """
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        
        # Speed in pixels per cycle
        self.speed = 10.0
     
        # Floating point representation of where the ball is
        self.x = 0
        self.y = 0 + screen_size[1] *0.05
     
        # Direction of ball (in degrees)
        self.direction = 200 + 180
     
        self.radius =  screen_size[0] * 0.01
 
        # Create the image of the ball
        self.image = visual.Circle(win, self.radius)
 
        # Color the ball
        self.image.fillColor = white
        self.image.pos = (self.x, self.y)
#        
  
    def bounce(self, diff):
        """ This function will bounce the ball
            off a horizontal surface (not a vertical one) """
 
        self.direction = (180 - self.direction) % 360
        self.direction += diff
 
    def update(self):
        """ Update the position of the ball. """
        
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        # Move the image (ball) to where our x and y are
        self.image.pos = (self.x, self.y)
 
        # Do we bounce off the top of the screen?
        if self.y >= screen_size[1]/2.0:
            self.bounce(0)
 
        # Do we bounce off the left of the screen?
        if self.x <=  -screen_size[0] / 2.0:
            self.direction = (360 - self.direction) % 360
            self.x = -screen_size[0] / 2.0 + self.radius
 
        # Do we bounce of the right side of the screen?
        if self.x >= screen_size[0] / 2.0:
            self.direction = (360 - self.direction) % 360
            self.x =screen_size[0] / 2.0 - self.radius - 1
 
        # Did we fall off the bottom edge of the screen (or below the paddle)?
        if self.y < - (screen_size[1] / 2.0 + self.radius):
            return True
        else:
            return False
 
class Player():
    """ This class represents the bar at the bottom that the
    player controls. """
 
    def __init__(self):
        """ Constructor for Player. """
 
        self.width = 300
        self.height =15
        self.image = visual.Rect(win, self.width, self.height)
  
        # Color the player
        self.image.fillColor = white
        self.fixed_y = -screen_size[1]/2 + 100
        self.image.pos = (0, self.fixed_y)
        
        
  
    def update(self):
        """ Update the player position. """
        
        if eye_tracking:
            
            # Peek in the eye tracker buffer
            data = tracker.peek_buffer_data()
            
            # Convert from Tobii coordinate system to ssv 
            lx = [d.leftEye.gazeX for d in data]
            rx = [d.rightEye.gazeX for d in data]

            # Use the average position (i.e., lowpass filtered)
            pos = (np.mean(rx) + np.mean(lx)) / 2.0 - screen_size[0]/2

        else:
            # Get where the mouse is
            pos = mouse.getPos()[0]

        # Set the left side of the player bar to the mouse/gaze position
        if pos > (screen_size[0] / 2 - self.width/2.0):
            pos = screen_size[0] / 2 - self.width/2.0
            
        if pos < (-screen_size[0] / 2 + self.width/2.0):
            pos = -screen_size[0] / 2 + self.width/2.0
            
        
        # Update position of player
        self.image.pos = (pos, self.fixed_y)

 
# Create the player paddle object
player = Player()
ball = Ball()

player.image.draw()
ball.image.draw()

# --- Create blocks
blocks = generate_blocks()
#blocks_buffered = visual.BufferImageStim(win, stim=blocks)
win.flip()

# Is the game over?
game_over = False

# Exit the program?
exit_program = False
score = 0
score_old = 0

# Main program loop
i = 1
c.reset()
my_clock.reset()
while not exit_program:
 
    k = event.getKeys()
    if 'escape' in k:
        exit_program = True
        
    # Update the ball and player position as long
    # as the game is not over.
    # Update the player and ball positions
    player.update()
    game_over = ball.update()

    # See if the ball hits the player paddle
    wentThrough = ball.image.pos[1] <= player.image.pos[1] and ((player.image.pos[0] - ball.image.pos[0]) / player.width<.5)
    if (player.image.overlaps(ball.image) or wentThrough) and c.getTime() > 0.5:
        
        # The 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff = (player.image.pos[0] - ball.image.pos[0]) / player.width / 2 * 30 
 
        # Set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.bounce(diff)
        c.reset()
        
       
    # See if the ball hits a brick
    overlap = [ball.image.overlaps(b.image) for b in blocks]
    if any(overlap):
        # Delete the brick it hits and bounce
       del blocks[np.where(overlap)[0][0]]
       ball.bounce(0)
       score += 5
       
#       # Re-create blocks_buffered
#       blocks_buffered = visual.BufferImageStim(win, stim=blocks)
       
    # Any bricks left?
    if len(blocks) == 0:
        exit_program = True
        
    # Paddel missed the ball
    if ball.image.pos[1] <= player.image.pos[1] and not ((player.image.pos[0] - ball.image.pos[0]) / player.width<.5):
        exit_program = True

    # Draw all stimuli
    game_rect.draw()
    [b.image.draw() for b in blocks]
    player.image.draw()
    ball.image.draw()
    
    # Draw the score
    if score > score_old:
        instruction_text.text = 'Score: ' + str(score)
    instruction_text.draw()
    win.flip()
    
    # Increase the ball speed at certain intervals
    if my_clock.getTime() > 5 :
        ball.speed *= 1.1
        my_clock.reset()
        
    score_old = score

try:
    
    # Create the file if it doesn't exist
    fname  = 'highscore.csv'
    print(os.path.isfile(fname))
    if not os.path.isfile(fname):
        df = pd.DataFrame({'Name':[player_name], 'Score':[score]})
        df.to_csv(fname, sep='\t')
    else:
        df = pd.read_csv('highscore.csv', sep='\t')
    
    highscore = np.max(np.array(df['Score']))
    
    instruction_text.pos = (0, 0)
    instruction_text.height = 50    
    
    if highscore >= score: 
        # Blink HIGH SCORE
        instruction_text.text = 'HIGH SCORE!'
        for i in range(5):
            instruction_text.draw()
            win.flip()
            core.wait(0.3)
            win.flip()
            core.wait(0.3)             
    else:   
        # Blink GAME OVER 
        instruction_text.text = 'GAME OVER'
        for i in range(5):
            instruction_text.draw()
            win.flip()
            core.wait(0.3)
            win.flip()
            core.wait(0.3)
            
    # Show score    
    instruction_text.draw()
    instruction_text.pos = (0, - 100)
    instruction_text.text = 'Your score: ' + str(score)
    instruction_text.draw()
    instruction_text.pos = (0, - 200)
    instruction_text.text = 'High score: ' + str(highscore)          
    instruction_text.draw()
    win.flip()

    core.wait(3)

    # Stop eye tracker and clean up 
    if eye_tracking:
        tracker.stop_buffer()
        tracker.stop_recording()
        tracker.de_init()

    # Write results to data frame
    df_player = pd.DataFrame({'Name':[player_name], 'Score':[score]})

    # Add players score to highscore sheet
    with open(fname, 'a') as f:
        df_player.to_csv(f, sep='\t', header=False)
            
except Exception as e: 
    mouse.setVisible (True)
    print(e)

win.close()
core.quit()