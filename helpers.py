import numpy as np
import scipy.signal as sgn

# Do not use this one, it's only used in the next function!!!
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sgn.butter(order, [low, high], btype='band')
    return b, a

# Bandpass filter applied on array "data"
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sgn.lfilter(b, a, data)
    return y

# Moving average to scmooth signal
def smooth(x, window_len=11, window='hanning'):
	if window_len<3:
	    return x
	s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
	if window == 'flat': #moving average
	    w=np.ones(window_len,'d')
	else:
	    w=eval('np.'+window+'(window_len)')
	y=np.convolve(w/w.sum(), s, mode='valid')
	return y