# -*- coding: utf-8 -*-
'''
Created on Fri Nov 10 21:31:13 2017

@author: marcus
'''

from psychopy import visual
import numpy as np
from psychopy.tools import monitorunittools
from collections import deque
import copy
import sys

if sys.version_info[0] == 3:
    xrange = range

#%%
class MyDot2:
    '''
    Generates the best fixation target according to Thaler et al. (2013)
    '''
    def __init__(self, win, outer_diameter=50, inner_diameter=10,
                 outer_color = 'black', inner_color = 'white',units = 'pix'):
        '''
        Class to generate a stimulus dot with
        units are derived from the window
        '''

        # Set propertis of dot
        outer_dot = visual.Circle(win,fillColor = outer_color, radius = outer_diameter/2,
                                  units = units)
        inner_dot = visual.Circle(win,fillColor = outer_color, radius = inner_diameter/2,
                                  units = units)
        line_vertical = visual.Rect(win, width=inner_diameter, height=outer_diameter,
                                    fillColor=inner_color, units = units)
        line_horizontal = visual.Rect(win, width=outer_diameter, height=inner_diameter,
                                    fillColor=inner_color, units = units)


        self.outer_dot = outer_dot
        self.inner_dot = inner_dot
        self.line_vertical = line_vertical
        self.line_horizontal = line_horizontal


    def set_size(self, size):
        ''' Sets the size of the stimulus.
        '''
        self.outer_dot.radius = size / 2
        self.line_vertical.size = (self.line_vertical.width, size)
        self.line_horizontal.size = (size, self.line_horizontal.height)

    def set_pos(self, pos):
        '''
        sets position of dot
        pos = [x,y]
        '''
        pos = [float(x) for x in pos]
        self.outer_dot.pos = pos
        self.inner_dot.pos = pos
        self.line_vertical.pos = pos
        self.line_horizontal.pos = pos

    def get_pos(self):
        '''
        get position of dot
        '''
        pos = self.outer_dot.pos

        return pos

    def get_size(self):
        '''
        get size of dot
        '''

        return self.outer_dot.radius * 2


    def draw(self):
        '''
        draws the dot
        '''
        self.outer_dot.draw()
        self.line_vertical.draw()
        self.line_horizontal.draw()
        self.inner_dot.draw()

    def invert_color(self):
        '''
        inverts the colors of the dot
        '''
        temp = self.outer_dot.fillColor
        self.outer_dot.fillColor = self.inner_dot.fillColor
        self.inner_dot.fillColor = temp

    def set_color(self, outer_color, inner_color):
        self.outer_dot.lineColor = outer_color
        self.outer_dot.fillColor = outer_color
        self.inner_dot.fillColor = outer_color
        self.inner_dot.lineColor = outer_color
        self.line_vertical.lineColor = inner_color
        self.line_horizontal.fillColor = inner_color
        self.line_vertical.fillColor = inner_color
        self.line_horizontal.lineColor = inner_color
        
def pixels2degrees(pixels,viewing_dist = 0.70,screen_res = [1280,1024],
                   screen_size = [0.38,0.30],dim = 'h',center_coordinate_system = False):
    '''
    Converts from pixels to degrees
    Pixels can be a single value or a 1D array
    to ensure that conversion is correct in vertical and horizontal dimensions
    '''

    # Conversion in horizontal or vertical dimension?
    if dim == 'h':
        res =  screen_res[0]
        size = screen_size[0]
    else:
        res = screen_res[1]
        size = screen_size[1]

    # SMIs coordinate-system starts in the upper left corner and psychopy's in
    # the center of the screen
    if center_coordinate_system:
        pixels = pixels - res/2

    meter_per_pixel = size/res
    meters = pixels*meter_per_pixel

    alpha = 180/np.pi*(2*np.arctan(meters/viewing_dist/2))

    return alpha

def smi2psychopy(pos, mon, units = 'pix'):
    ''' Converts from smi output (pixels, origo in upper left corner, positive y downward) to
    psychopy coordinate system  (origo in center, positive y upware)
    Args:   pos: N x 2 array
            mon: psychopy monitor
    '''
    screen_res = mon.getSizePix()

    # Center coordinate system to center of screen (now in psychopy 'pix')
    pos[:, 0] = pos[:, 0] - screen_res[0]/2.0
    pos[:, 1] = (pos[:, 1] - screen_res[1]/2.0) *-1

    # convert to [-1, 1]
    if 'norm' in units:
        pos[:, 0] = pos[:, 0] / screen_res[0]/2.0
        pos[:, 0] = pos[:, 1] / screen_res[1]/2.0
    elif 'deg' in units:
        pos[:, 0] = monitorunittools.pix2deg(pos[:, 0], mon, correctFlat=False)
        pos[:, 1] = monitorunittools.pix2deg(pos[:, 1], mon, correctFlat=False)
    elif 'pix':
        pass
    else:
        raise IOError ('Unvalid unit')

    return pos

def psychopy2smi(pos, mon, units='norm'):
    ''' Converts from psychopy norm coordinate system to smi coords (pix).
    Args:   pos: N x 2 array
            mon: psychopy monitor
    '''

    screen_res = mon.getSizePix()

    # Change units to pixels and
    if 'norm' in units:
        pos[:, 0] = pos[:, 0] * screen_res[0]/2.0
        pos[:, 1] = pos[:, 1] * screen_res[1]/2.0
    if 'deg' in units:
        pos[:, 0] = monitorunittools.deg2pix(pos[:, 0], mon, correctFlat=False)
        pos[:, 1] = monitorunittools.deg2pix(pos[:, 1], mon, correctFlat=False)

    # Move origo to upper left (y downward)
    pos[:, 0] = pos[:, 0] + screen_res[0]/2.0
    pos[:, 1] = -1 * pos[:, 1] + screen_res[1]/2.0

    return pos


#%%
class RingBuffer(object):
    ''' A simple ring buffer based on the deque class
    Used as online buffer of gaze samples'''
    def __init__(self, maxlen=200):        
        # Create que with maxlen 
        self.maxlen = maxlen
        self._b = deque(maxlen=maxlen)

    def clear(self):
        ''' Clears buffer '''
        return self._b.clear()

    def get_all(self):
        ''' Returns all samples from buffer and empties the buffer'''
        lenb = len(self._b)
        return list([self._b.popleft() for i in range(lenb)])

    def peek(self):
        ''' Returns all samples from buffer without emptying the buffer
        First remove an element, then add it again
        '''
        b_temp = copy.copy(self._b)
        c = []
        if len(b_temp) > 0:
            for i in xrange(len(b_temp)):
                c.append(b_temp.pop())

        return c

    def peek_time_range(self, t0, t1):
        ''' Returns all samples from buffer without emptying the buffer
        First remove an element, then add it again
        '''
        b_temp = copy.copy(self._b)
        c = []
        if len(b_temp) > 0:
            for i in range(len(b_temp)):
                sample = b_temp.pop()
                if (sample.timestamp >= t0) and (sample.timestamp <= t1):
                    c.append(sample)

        return c
        
    def append(self, L):
        self._b.append(L)         
        '''Append buffer with the most recent sample (list L)'''
