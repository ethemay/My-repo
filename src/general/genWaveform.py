#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         genWave
# Date:         01.14.2023
# Author:       Dr. Pascal A. Schirmer
# Version:      V.0.1
# Copyright:    Pascal Schirmer
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
# Import libs
#######################################################################################################################
# ==============================================================================
# Internal
# ==============================================================================

# ==============================================================================
# External
# ==============================================================================
import numpy as np
from scipy import signal

#######################################################################################################################
# Function
#######################################################################################################################
def genWave(t, fel, phi, phi2, setupTopo):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    Tel = 1/fel
    Nsim = len(t)

    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # Sinusoidal
    # ==============================================================================
    if setupTopo['wave'] == "sin":
        wave = np.sin(2*np.pi*fel*t + phi + phi2)
        print("INFO: Sinusoidale waveform generated")

    # ==============================================================================
    # Constant
    # ==============================================================================
    elif setupTopo['wave'] == "con":
        t = np.linspace(0, Tel, Nsim)
        wave = np.ones((Nsim, ))
        print("INFO: Constant waveform generated")

    # ==============================================================================
    # Triangular
    # ==============================================================================
    elif setupTopo['wave'] == "tri":
        wave = signal.sawtooth(2*np.pi*fel*t + phi + phi2, 0.5)
        print("INFO: Triangular waveform generated")

    # ==============================================================================
    # Rectengular
    # ==============================================================================
    elif setupTopo['wave'] == "rec":
        wave = signal.square(2*np.pi*fel*t + phi + phi2, 0.5)
        print("INFO: Rectangular waveform generated")

    # ==============================================================================
    # Default
    # ==============================================================================
    else:
        wave = np.sin(2*np.pi*fel*t + phi + phi2)
        print("ERROR: Undefined waveform using sinusoidal wave")

    ###################################################################################################################
    # Output
    ###################################################################################################################
    return wave