#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         calcTimeB6
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
from scipy import integrate


#######################################################################################################################
# Function
#######################################################################################################################
def calcTimeB6(t, s, e, Vdc, Mi, mdl, setupTopo, start, ende):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Parameters
    # ==============================================================================
    id = ['A', 'B', 'C']
    fel = setupTopo['fel']
    K = int(np.round((t[-1] - t[0]) * fel))-1

    # ==============================================================================
    # Variables
    # ==============================================================================
    v0 = {}
    v = {}
    v_out = {}
    v_L = {}
    i = {}
    timeAc = {}
    timeDc = {}

    ###################################################################################################################
    # Pre-Processing
    ###################################################################################################################

    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    # ------------------------------------------
    # Inverter Output
    # ------------------------------------------
    for j in range(0, len(id)):
        v0[id[j]] = 0.5 * (s[id[j]] - np.mean(s[id[j]])) * Vdc
    v_n0 = 1 / 3 * (v0['A'] + v0['B'] + v0['C'])

    # ------------------------------------------
    # Phase Voltages
    # ------------------------------------------
    for j in range(0, len(id)):
        v[id[j]] = v0[id[j]] - v_n0

    # ------------------------------------------
    # Filter Output
    # ------------------------------------------
    for j in range(0, len(id)):
        if setupTopo['outFilter'] == 0:
            v_out[id[j]] = v[id[j]]
        else:
            _, v_out[id[j]], _, = sig.lsim(mdl['SS']['Out'], v[id[j]], t, X0=v[id[j]][0])

    # ------------------------------------------
    # Load
    # ------------------------------------------
    # Voltage
    for j in range(0, len(id)):
        v_L[id[j]] = v_out[id[j]] - Mi * e[id[j]]

    # LL Current
    #for j in range(0, len(id)):
    #    _, i[id[j]], _ = sig.lsim(mdl['SS']['Load'], v_L[id[j]], t)
    #    i[id[j]] = i[id[j]][start:ende]
    _, i_ab, _, = sig.lsim(mdl['SS']['Load'], (v0['A'] - Mi * e['A'] - v0['B'] - Mi * e['B']) / np.sqrt(3), t)
    _, i_bc, _, = sig.lsim(mdl['SS']['Load'], (v0['B'] - Mi * e['B'] - v0['C'] - Mi * e['C']) / np.sqrt(3), t)
    _, i_ca, _, = sig.lsim(mdl['SS']['Load'], (v0['C'] - Mi * e['C'] - v0['A'] - Mi * e['A']) / np.sqrt(3), t)
    i['A'] = np.roll(i_ab[start:ende], int(np.floor((30 + 0) / 360 / K * len(s['A'][start:ende]))))
    i['B'] = np.roll(i_bc[start:ende], int(np.floor((30 + 0) / 360 / K * len(s['B'][start:ende]))))
    i['C'] = np.roll(i_ca[start:ende], int(np.floor((30 + 0) / 360 / K * len(s['C'][start:ende]))))

    # LN Current
    if setupTopo['wave'] != 'con':
        for j in range(0, len(id)):
            i[id[j]] = i[id[j]] - np.mean(i[id[j]])

    # ==============================================================================
    # DC-Side
    # ==============================================================================
    # ------------------------------------------
    # Inverter Input
    # ------------------------------------------
    i_dc = 1 / 2 * (s['A'][start:ende] * i['A'] + s['B'][start:ende] * i['B'] + s['C'][start:ende] * i['C'])

    # ------------------------------------------
    # DC-Link
    # ------------------------------------------
    i_cap = np.mean(i_dc) - i_dc
    _, v_dc, _, = sig.lsim(mdl['SS']['DC'], i_cap, t[start:ende])
    v_dc = v_dc - np.mean(v_dc) + Vdc

    # ------------------------------------------
    # Filter Input
    # ------------------------------------------
    if setupTopo['inpFilter'] == 0:
        v_in = v_dc
    else:
        _, v_in, _, = sig.lsim(mdl['SS']['Inp'], (v_dc - Vdc), t[start:ende])
        v_in = v_in + Vdc

    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    timeAc['v_a0'] = v0['A'][start:ende]
    timeAc['v_a'] = v['A'][start:ende]
    timeAc['v_L_a'] = v_L['A'][start:ende]
    timeAc['v_a_out'] = v_out['A'][start:ende]
    timeAc['v_n0'] = v_n0[start:ende]
    timeAc['i_a'] = i['A']
    timeAc['i_b'] = i['B']
    timeAc['i_c'] = i['C']

    # ==============================================================================
    # DC-Side
    # ==============================================================================
    timeDc['v_in'] = v_in
    timeDc['v_dc'] = v_dc
    timeDc['i_dc'] = i_dc
    timeDc['i_c'] = i_cap

    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [timeAc, timeDc]
