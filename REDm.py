# -*- coding: utf-8 -*-
"""
Created on Sat Jan 09 19:50:57 2016

@author: marcus

Settings file for the RED-m eye tracker
Here we list parameters that can be sent remotely to iView server to override default parameters
OBS! PsychoPy geometric setup should match that entered in iView
"""

MY_MONITOR = 'default'              # needs to exist in PsychoPy monitor center



#%% CONNECTION AND TRACKER PARAMS

# General things you can set on all supported eye trackers
port_listen=4444
port_send=5555
ip_send = '127.0.0.1'
ip_listen = '127.0.0.1'

track_mode = 'SMART_BINOCULAR'
sampling_freq = 120                 # Sampling rate of eye tracker

geom_profile = 'Desktop 22in Monitor' # 

average_data = False                # Output binocular of monocular data
filtering = False                   # Use filter to smooth data

#%% Files and filepaths
delete_temp_idf_files = False       # 

eye_image_size = (240, 496)


#%% CALIBRATION PARAMETERS 
autoaccept = 0                      # autoaccept (2), semi autoaccept (1, accept first point) 
                                    # of accept with space bar (0)
                                    
n_cal_points = 0                    # number of calibration points supported: [1, 2, 5, 9]

cal_speed = 1                       # pacing of calibration / validation targets [slow: 0, fast: 1]
                                    # 0: slow, 1:fast
select_best_calibration = True      # option to run a few calibration and 
                                    # select the best
                                    
reset_calibration_points = False    # Resets calibration points to default 
                                    # locations before calibration starts
                                    
record_data_during_calibration = True # Record data during calibration to idf-file

animate_calibration = True          # Show static points or animated targets
screen = 1                          # Display stimuli on a second screen attached 
                                    # to your computer (1). Single setup (0).










