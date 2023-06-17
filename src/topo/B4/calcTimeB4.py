#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         calcTimeB4
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
import scipy.signal as sig

#######################################################################################################################
# Function
#######################################################################################################################
def calcTimeB4(t, s, e, Vdc, Mi, mdl, setupTopo, start, ende):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    timeAc = {}
    timeDc = {}
    
    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    # ------------------------------------------
    # Inverter Output
    # ------------------------------------------
    v_a0 = 0.5*s['A']*Vdc
    v_b0 = 0.5*s['B']*Vdc
    v_ab = v_a0 - v_b0
    
    # ------------------------------------------
    # Filter Output
    # ------------------------------------------
    if setupTopo['outFilter'] == 0:
        v_out = v_ab
    else:
        _, v_out, _, = sig.lsim(mdl['SS']['Out'], v_ab, t, X0=v_ab[0])
    
    # ------------------------------------------
    # Load 
    # ------------------------------------------
    # Voltage
    v_L = v_out - Mi*e
    
    # Current
    if setupTopo['wave'] == "con":
        _, i_a, _, = sig.lsim(mdl['SS']['Load'], v_L, t)
        i_a = i_a[start:ende]
    else: 
        _, i_a, _, = sig.lsim(mdl['SS']['Load'], (v_L - np.mean(v_L)), t)
        i_a = i_a[start:ende]
        i_a = i_a - np.mean(i_a)

    # ==============================================================================
    # DC-Side
    # ==============================================================================
    # ------------------------------------------
    # Inverter Input
    # ------------------------------------------
    i_dc = i_a/2 * (s['A'][start:ende] - s['B'][start:ende])
    
    # ------------------------------------------
    # DC-Link
    # ------------------------------------------
    i_c = np.mean(i_dc) - i_dc
    _, v_dc, _, = sig.lsim(mdl['SS']['DC'], i_c, t[start:ende])
    
    # ------------------------------------------
    # Filter Input
    # ------------------------------------------
    if setupTopo['inpFilter'] == 0:
        v_in = v_dc
    else:
        _, v_in, _, = sig.lsim(mdl['SS']['Inp'], (v_dc-Vdc), t[start:ende])
        v_in = v_in + Vdc
        
    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    timeAc['v_a0'] = v_a0[start:ende]
    timeAc['v_b0'] = v_a0[start:ende]
    timeAc['v_L'] = v_L[start:ende]
    timeAc['v_out'] = v_out[start:ende]
    timeAc['v_ab'] = v_ab[start:ende]
    timeAc['i_a'] = i_a
    
    # ==============================================================================
    # DC-Side
    # ==============================================================================
    timeDc['v_in'] = v_in
    timeDc['v_dc'] = v_dc
    timeDc['i_dc'] = i_dc
    timeDc['i_c'] = i_c
    
    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [timeAc, timeDc]