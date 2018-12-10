#!/usr/bin/env python
# coding: utf-8

# # ASP Project: Designing an Auto-Wah for guitar

# Lucie Perrotta and Simon Guilloud, 2018

# Install libraries

import warnings
warnings.filterwarnings('ignore')

# General imports
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import IPython

# Audio imports
import scipy.signal as sgn
from scipy.io import wavfile

# Helpers
from helpers import *


def compute_envelope (data, ma_width = 2000):
    """
    Compute the envelope of the signal for a dynamic filter application. It is just a moving average applied to the absolute value of the signal,
    normalized between 0 and 1 with some flooring/ceiling.
    Parameters:
    data = The audio signal, between -1 and 1
    ma_width = The width of the moving average.
    Return:
    The envelope of the signal, between 0 and 1
    """
    # Compute the envelope
    envelope = np.concatenate((np.zeros(ma_width//2), data, np.zeros(ma_width//2)))
    envelope = moving_average(np.abs(envelope), ma_width)
    # Log based auditory system
    envelope_log = np.exp(envelope)
    # Normalization
    envelope_log -= np.min(envelope_log)
    envelope_log /= np.max(envelope_log)
    # 
    envelopeF = envelope_log-np.percentile(envelope_log, 10)
    envelopeF /= np.percentile(envelope_log, 95)
    envelopeF = np.clip(envelopeF, 0, 1)
    envelopeF /= np.max(envelopeF)
    return envelopeF


def autowah(data, maximum, minimum, order=2, peak= True, Q = 1, p=0.8, delay=0, fs = 44100):
    """
    This function apply a dynamic filter (or autowah) on a given signal.
    Parameters:
    data = A numpy array containg audio values between -1 and 1
    maximum = The maximum value (in herz) the filter will cut too. Everything higher than that will always be cut.
    minimum = The minimum value (in herz) the filter will cut too. Everything lower than that will never be cut.
    order = The order of the IIR filter. 2 is fine. Try higher values if you want some weird techno-ish sounds
    peak = Boolean value. If set to false the filter will only be lowpass without the resonante component.
    Q = Quality factor of the peak.
    p = Height of the peak. It set to zero, equivalent to peak = False. Should be between 0 and 1 (included)
    delay = delay between the filter and the envelope. May give some weird result.
    fs = Sampling rate.
    
    Return :
    A numpy array containing the resulting audio signal, between 0 and 1.
    """
    if (order < 2):
        raise ValueError("order must be at least 2")
    envelope = compute_envelope(data)
    Q = max(Q, 0.5)
    if peak and (p>1 or p < 0):
        raise ValueError("p must be between 0 and 1")
    y = np.zeros(len(data)+ order+1)
    z = np.zeros(len(data)+ order+1)# Create the y (order + 1 zeros at the begining to compute the 1st values...)
    if delay > 0 :
        d = np.concatenate((np.zeros(order+1+int(delay*fs)), data)) # add padded zeros at the beginning
    else:
        d = np.concatenate((np.zeros(order+1), data, np.zeros(int(-delay*fs)))) # add padded zeros at the beginning
    envelope = np.concatenate((np.zeros(order+1), envelope))

    vals_b = np.zeros(order+1)
    vals_a = np.zeros(order+1)

    for i in range(order+1, len(y)): # begin at order+1 since we must use previous values (0)

        if(i%100 == order+1): 
            cutoff = envelope[i]*(maximum-minimum)/fs*2 + minimum/fs*2
            b, a = sgn.iirfilter(
                      N=order,
                      Wn=(cutoff),     
                      rp=30,
                      rs = 60,
                      btype='lowpass',
                      analog = False,
                      ftype='butter', 
                      output='ba')

        for j in range(0, order+1): # Compute X of the tranfer function
            vals_b[j] = b[j] * d[i-j]

        for j in range(1, order+1): # Compute Y of the tranfer function
            vals_a[j] = a[j] * y[i-j]

        y[i] = (1/a[0]) * ( np.sum(vals_b) - np.sum(vals_a) ) # Transfer function
        
    if peak :
        for i in range(3, len(z)): 

            if(i%100 == 3): # sinon trop lent
                cutoff = envelope[i]*(maximum-minimum)/fs*2 + minimum/fs*2
                b2, a2 = sgn.iirpeak(cutoff, Q)

            for j in range(0, 3): # Compute X of the tranfer function
                vals_b[j] = b2[j] * y[i-j]

            for j in range(1, 3): # Compute Y of the tranfer function
                vals_a[j] = a2[j] * z[i-j]

            z[i] = (1/a[0]) * ( np.sum(vals_b) - np.sum(vals_a) ) # Transfer function
        y = p*z+(1-p)*y
    return y/np.max(abs(y))

def renderAutowah (file, maximum = 3000, minimum = 500, peak = True, p = 1, write=False, output = "output.wav"):
    """
    This function apply a dynamic filter (or autowah) on a given wav file.
    Parameters:
    file = The filepath of a wav file.
    maximum = The maximum value (in herz) the filter will cut too. Everything higher than that will always be cut.
    minimum = The minimum value (in herz) the filter will cut too. Everything lower than that will never be cut.
    peak = Boolean value. If set to false the filter will only be lowpass without the resonante component.
    p = Height of the peak. It set to zero, equivalent to peak = False. Should be between 0 and 1 (included).
    write = Boolean value. Set to true if you want the resulting audio saved.
    output = The filepath where you want the result to be saved, if write = True.
    
    Return :
    A numpy array containing the resulting audio signal, between 0 and 1, along with the sampling rate of the file. Two-dimensional
    if stereo.
    """
    
    fs, data = wavfile.read(file) # get data as integers
    stereo = len(np.shape(data)) == 2
    if stereo :
        datar = data[:,1]
        datal = data[:,0]
        MAX_VAL = abs(np.iinfo(datal.dtype).min)
        datal = datal / MAX_VAL 
        MAX_VAL = abs(np.iinfo(datar.dtype).min)
        datar = datar / MAX_VAL # now data is a normalized array of float between -1 and 1
        yl = autowah(datal, maximum, minimum, peak = peak, Q = 0.8, p = p, delay = 0)
        yr = autowah(datar, maximum, minimum, peak = peak, Q = 0.8, p = p, delay = 0)
        y = np.asarray([yl, yr], dtype=np.float32)
        

    else :
        MAX_VAL = abs(np.iinfo(data.dtype).min) # get max integer
        data = data / MAX_VAL # now data is a normalized array of float between -1 and 1

        y = autowah(data, maximum, minimum, peak = peak, Q = 0.8, p = p, delay = 0)
        y = np.asarray(y, dtype=np.float32)
    if write :
        wavfile.write(output, fs, y)
    return y, fs
