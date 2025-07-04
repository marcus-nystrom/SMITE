# -*- coding: utf-8 -*-
'''
Created on Mon Feb 26 14:16:59 2018

@author: Marcus
'''

from psychopy import core

def get_defaults(eye_tracker_name):
    ''' Returns default setting
    '''
    if eye_tracker_name == 'REDm':
        from . import REDm as settings
    elif eye_tracker_name == 'HiSpeed':
        from . import HiSpeed as settings
    elif eye_tracker_name == 'RED':
        from . import RED as settings
    elif eye_tracker_name == 'REDn_Professional':
        from . import REDn_Professional as settings
    elif eye_tracker_name == 'REDn_Scientific':
        from . import REDn_Scientific as settings        
    elif eye_tracker_name == 'RED250mobile':
        from . import RED250mobile as settings             
    else:
        print('Eye tracker not defined')
        core.quit()   
        
    settings.eye_tracker_name = eye_tracker_name
    
    return settings
    
    
class Connect(object):   
    def __init__(self, in_arg='dummy'):
        '''  in_arg can be either string with the eye tracker name
        or 'settings' generated by calling (and optionally modifying)
        the output from get_defaults()
        '''
        
        if isinstance(in_arg, str):
            if 'dummy' in in_arg:
                from . import SMITE_Dummy
                self.__class__ = SMITE_Dummy.Connect
                self.__class__.__init__(self)  
            else:            
                from . import SMITE_ET
                self.__class__ = SMITE_ET.Connect
                self.__class__.__init__(self, in_arg)
        else:
            from . import SMITE_ET
            self.__class__ = SMITE_ET.Connect
            self.__class__.__init__(self, in_arg)
            
            
        

