# Import modules
from psychopy import visual, monitors
from psychopy import core, event, gui
import numpy as np
import os, sys


# Insert the parent directory (where SMITE is) to path
curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)
sys.path.insert(0,os.path.dirname(curdir)) 
from smite import SMITE, helpers

MY_MONITOR = 'default'
SCREEN_WIDTH = 53
SCREEN_RES = (1920, 1080)
VIEWING_DIST = 65
dummy_mode = True

mon = monitors.Monitor(MY_MONITOR) # Defi ned in defaults file
mon.setWidth(SCREEN_WIDTH)    # Width of screen (cm)
mon.setDistance(VIEWING_DIST) # Distance eye / monitor (cm) 
mon.setSizePix(SCREEN_RES)

eye_tracker_name = 'REDm'
settings = SMITE.get_defaults(eye_tracker_name) 

# Window set-up (the color will be used for calibration)

win = visual.Window(monitor = mon, screen = settings.screen, size=(1280, 1024),
                    units = 'deg', fullscr = True,
                    allowGUI = False) 
text = visual.TextStim(win, text='')                    
print(win.size)
et_sample = visual.Circle(win, radius  = 20, 
                                 fillColor = 'blue',
                                  units='pix') 
                                  
mouse = event.Mouse(win=win)                                  


tracker = SMITE.Connect(settings)


#tracker.raw.set_RED_geometry()

if dummy_mode:
    tracker.set_dummy_mode()
    
tracker.init()
print(tracker.system_info)

tracker.calibrate(win)

tracker.start_recording()

tracker.start_buffer(sample_buffer_length=10) 
core.wait(0.5)

print('connection status: {}'.format(tracker.is_connected()))

text.text = 'Press Escape to continue'
# Show gaze contingent marker (left eye)
while True:
    
    k = event.getKeys()

    data = tracker.peek_buffer_data() 
   
    
    if len(data) > 0:
        
        # Convert mouse data to smi coordinate system
        pos = np.array([[data[0].leftEye.gazeX, data[0].leftEye.gazeY]])
        pos = helpers.smi2psychopy(pos, mon, units='pix')
        et_sample.pos = pos
        et_sample.draw()
        
    text.draw()
    win.flip()
    
    if 'escape' in k:
        break
        
tracker.stop_buffer()
tracker.stop_recording()

core.wait(1)

# Test setting image name
tracker.start_recording()
core.wait(0.1)

# Flip an image onto the screen here
tracker.set_begaze_trial_image("imname.png")
core.wait(1)
tracker.stop_recording()

# Test setting mouse click in BeGaze
text.text = 'Left click mouse'
core.wait(1)
tracker.start_recording()
text.draw()
win.flip()

pressed = False
while not pressed:
    buttons = mouse.getPressed()
    if np.any(np.array(buttons)):
        b = np.where(buttons)[0][0]
        if b==0:
            which = 'left'
        else:
            which = 'right'
        pos = mouse.getPos()
        pressed = True
        
    text.draw()
    win.flip()
print(which, pos[0], pos[1])
tracker.set_begaze_mouse_click(which, pos[0], pos[1])

# Test setting key press in BeGaze
text.setText('Press a key')
text.draw()
win.flip()
k = event.waitKeys()
print(k[0])
tracker.set_begaze_key_press(k[0])


# Print information about the RED geometry
print(tracker.geom)

# Print the calibration history
print(tracker.calibration_history)
print(tracker.system_info)

# Stop recording, save data, and cleanup
tracker.stop_recording()
win.close()
tracker.save_data('c:\\Marcus\\test.idf') # idf-file saved in default dir on iView comp
tracker.de_init()
core.quit()
