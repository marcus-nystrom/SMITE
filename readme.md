SMITE is a toolbox for using eye trackers from SMI GmbH with Python,
specifically offering integration with PsychoPy. A Matlab version
that integrates with PsychoPy is also available from https://github.com/dcnieho/SMITE

Cite as:
Niehorster, D.C., & Nyström, M., (in prep). SMITE: The definitive
toolbox for creating Psychtoolbox and Psychopy experiments with SMI eye
trackers.

For questions, bug reports or to check for updates, please visit
www.github.com/marcus-nystrom/SMITE. 

SMITE is licensed under the Creative Commons Attribution 4.0 (CC BY 4.0) license.

`demos/readme.py` shows a minimal example of using the toolbox's
functionality.

To run the toolbox, it is required to install the SMI iViewX SDK version
4.4.26. PsychoPy 1.90.1 stand alone is recommended. 

Tested on Windows PsychoPy 1.90.1. Also tested with PsychoPy3, Beta 10 (but see issue below).

## Usage
As demonstrated in the demo scripts, the toolbox is configured through
the following interface:
1. retrieve (default) settings for eye tracker of interest: `settings =
SMITE.get_defaults('trackerName');` Supported tracker Names are `HiSpeed`,
`RED`, `REDm`, `RED250mobile`, `REDn_Scientific`, and `REDn_Professional`.
2. edit settings if wanted (see below)
3. initialize SMITE using this settings struct: `EThndl = SMITE(settings)`

ToDos (current discrepancies between the paper and the toolbox):
1. File transfer in two computer setups not implemented
2. do_flip_eye not implemented (fixes a bug in older versions of iViewX, e.g., v. 2.7.13, where left and right eyes are flipped)
3. get_options returns all settings. set_options does nothing. This means that it's currently up to the user not to use functionally that is not available during recording (for instance changing the sampling frequency of the eye tracker).
4. Images returned from the API looks strange when using PsychoPy with Python 3.6. Affects validation screen and eye images.
5. 'pip install smite' not yet available

