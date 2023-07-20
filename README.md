SMITE is a toolbox for using eye trackers from SMI GmbH with Python,
specifically offering integration with PsychoPy. A Matlab version
that integrates with Psychtoolbox is also available from https://github.com/dcnieho/SMITE

Cite as:
[Niehorster, D.C., & Nyström, M., (2019). SMITE: A
toolbox for creating Psychtoolbox and Psychopy experiments with SMI eye
trackers. doi: 10.3758/s13428-019-01226-0.](https://doi.org/10.3758/s13428-019-01226-0)

For questions, bug reports or to check for updates, please visit
www.github.com/marcus-nystrom/SMITE. 

SMITE is licensed under the Creative Commons Attribution 4.0 (CC BY 4.0) license.

`demos/read_me.py` shows a minimal example of using the toolbox's
functionality.

To run the toolbox, it is required to  PsychoPy 1.90.1 standalone is recommended. 

Tested on Windows PsychoPy using Python 2.7. Also tested with PsychoPy3 (Python 3.6, but see issues below)

## To get started (Windows)


1. Install the SMI iViewX SDK version 4.4.26.
1. Download [PsychoPy (e.g., StandalonePsychoPy3_PY2-3.2.3-win32.exe
)](https://www.psychopy.org)
1. Download and install [git](https://www.git-scm.com/downloads)
1. Open the command window
	1. Go the the PsychoPy folder (e.g., C:\Program Files (x86)\PsychoPy)
	1. type 'python -m pip install git+https://github.com/marcus-nystrom/SMITE.git#egg=SMITE' 
1. Download the 'examples' folder and run read_me.py (first change the monitor settings and the eye tracker name in read_me.py).
	
Alternatively:
1. Install the SMI iViewX SDK version 4.4.26.
1. Download [PsychoPy (e.g., StandalonePsychoPy3_PY2-3.2.3-win32.exe
)](https://www.psychopy.org)
1. Download or clone the SMITE folder
1. Add the downloaded SMITE-folder to path in PsychoPy (under file->preferences)
1. Run read_me.py (first change the monitor settings and the eye tracker name in read_me.py).

## Usage
As demonstrated in the demo scripts, the toolbox is configured through
the following interface:
1. retrieve (default) settings for eye tracker of interest: `settings =
SMITE.get_defaults('trackerName');` Supported tracker Names are `HiSpeed`,
`RED`, `REDm`, `RED250mobile`, `REDn_Scientific`, and `REDn_Professional`.
2. edit settings if wanted
3. initialize SMITE using this settings struct: `EThndl = SMITE(settings)

## API
#### Methods
The following method calls are available on a SMITE instance

|Call|inputs|outputs|description|
| --- | --- | --- | --- |
|`get_options()`||<ol><li>`settings`: module with current settings</li></ol>|Get settings|
|`init()`|||Connect to the SMI eye tracker and initialize it according to the requested settings|
|`is_connected()`||<ol><li>`status`: SMI status code (int). For its meaning, see the iView API documentation.|Report status of the connection to the eye tracker|
|`calibrate()`|<ol><li>`win`: window pointer to PsychoPy screen where the calibration stimulus should be shown. See visual.Window()||Do participant setup, calibration and validation|
|`start_recording()`|<ol><li>`clear_buffer`: optional. Boolean indicating whether the IDF file buffer should be cleared before recording starts or not. This clears all already recorded data from the idf file, so set to `true` with caution</li></ol>||Start recording eye-movement data to idf file|
|`start_buffer()`|<ol><li>`sample_buffer_length`: optional. Size in number of samples of recording buffer.||Start recording eye-movement data into buffer for online use|
|`send_message()`|<ol><li>`msg`: Message to be written into idf file</li></ol>||Insert message into idf file|
|`get_latest_sample()`||`sample`:struct array|Get most recent data sample|
|`consume_buffer_data()`||list of samples|Get data from the online buffer. The returned samples are removed from the buffer|
|`peek_buffer_data()`||list of samples|Get data from the online buffer. The returned samples remain in the buffer|
|`stop_buffer()`|<ol><li>`clear_buffer`: optional. Boolean indicating whether the online buffer should be cleared</li></ol>||Stop recording data into buffer|
|`stop_recording()`|||Stop recording data into idf file|
|`save_data()`|<ol><li>`filename`: filename (including path) where idf file will be stored</li><li>`user`: optional. Indentifier that gets placed in idf file header</li><li>`description`: optional. Description that gets placed in idf file header</li><li>`append_version`: optional. Boolean indicating whether version numbers (`_1`, `_2`, etc) will automatically get appended to the filename if the destination file already exists</li></ol>||Save idf file to specified location|
|`de_init()`|<ol><li>`close`: optional. Boolean indicating whether the iView eye tracker server should be shut down</li></ol>||Close connection to the eye tracker and clean up|
|`set_begaze_trial_image()`|<ol><li>`filename`: filename of stimulus that is shown on this trial. Must have one of the following extentions: `.png`, `.jpg`, `.jpeg`, `.bmp`, or `.avi`</li></ol>||Put specially prepared message in idf file to notify BeGaze what stimulus image/video belongs to a trial|
|`set_begaze_key_press()`|<ol><li>`string`: string that will show up on BeGaze's event timeline. Can be name of a key, but also other arbitrary string</li></ol>||Put specially prepared message in idf file that shows up as keypress in BeGaze|
|`set_begaze_mouse_click()`|<ol><li>`which`: string indicating which mouse button, `left` or `right`</li><li>`x`: horizontal pixel coordinate of mouse click</li><li>`y`: vertical coordinate of mouse click</li></ol>||Put specially prepared message in idf file that shows up as mouse click in BeGaze|
|`start_eye_image_recording()`|<ol><li>`filename`: filename where recorded eye images will be saved</li><li>`format`: format to store eye images in, must be one of: `jpg`, `bmp`, `xvid`, `huffyuv`, `alpary`, `xmp4`</li><li>`duration`: optional. If provided, runs eye image recording for this many seconds</li></ol>||Start recording eye images to file. Not supported on `RED250mobile`, `REDn Scientific`, and `REDn Professional`|
|`stop_eye_image_recording()`|||Stop recording eye images to file|
|`set_dummy_mode()`|||Enable dummy mode, which allows running the program without an eye tracker connected|

ToDos (current discrepancies between the paper and the toolbox):
1. File transfer in two computer setups not implemented
2. do_flip_eye not implemented (fixes a bug in older versions of iViewX, e.g., v. 2.7.13, where left and right eyes are flipped)
3. get_options returns all settings. set_options does nothing. This means that it's currently up to the user not to use functionally that is not available during recording (for instance changing the sampling frequency of the eye tracker).
4. Images returned from the API look strange when using PsychoPy3. Affects validation screen and eye images.


