That is implementation of MeanShift algorithm

There are several example in main directory, that can be used for testing. 

In order to launch app just run the *mean_shift.py* with first argument name of directory.

Example: ```python mean_shift.py Dog``` (pure performance due to bad initial setup)
Example: ```python cam_shift.py Dog``` (pure performance due to bad initial setup)

Better parameters for dog tracking: ```python mean_shift.py Dog/ 0 30 30 15 200 200``` When we have more clear distribution, so tracking becomes more precise.

That will show you sequence of images with correct border of object that is desired to track.
 
In order to track the object just press "S" button and select window that will be tracked. Then press Space and observe te results.

There are two frames running simultaneously, one is image with frame and another is distribution of hist projection in order to interpret results.

You can also define that frame one more time during the video. That will overwrite the color histogram of object and can help with tracking in case the object was lost.

Also we can experiment with HSV min max values using app arguments m_h, m_s, m_v, M_h, M_s, M_v that refer to min and max HSV

There are optimal values for different objects tracking. They were picked experimentally using *color_picker.py*. I picked some good threshold for HSV space that dramatic improve tracking.

For example ```python mean_shift.py Tiger2 4 190 190 9 250 250```
For example ```python cam_shift.py Tiger2 4 190 190 9 250 250```

Cases, when results are not so good as the model misunderstend tiger with arm:
For example ```python mean_shift.py Tiger2```
For example ```python cam_shift.py Tiger2```
In that case we make emphasize on orange color. Distribution become more close to that we want to have, so we have better results.


In case of Dog the Mean shift works well befor dog becomes close to bushes, then it start to fail 
In case of Biker mean shift works good with default setup before fast move.
``` python cam_shift.py Biker/ 0 20 20 30 155 150```

Comparing two algorithms CamShift is improved MeanShift as it can dynamically change the window size.  
So it can adapt to the situations when some objects come closer to camera and become bigger for example.

Hoverer in some cases dynamically changing the window size is not so good as we can track only part of object (for example face of surfer)
The classic mean_shift is doing very good with default setup in that specific case. How ever in case of camshift we will start to track the entire surfer instead of only his face:
Example:```python mean_shift.py Surfer/``` (Good performance)
Example:```python cam_shift.py Surfer/``` (Not so good)


This algorithm is highly dependant to the initial setup (HSV mask that is used for filtering)
So as we see in case we use well defined mask in case with tiger the tracker performs very well, however in case there is no initial set up performanse is pure. So we should adapt it to every single condition.
However it should work well in case where the object is well separated from background (Surfer) or when there are always predefined conditions (Tiger).  
