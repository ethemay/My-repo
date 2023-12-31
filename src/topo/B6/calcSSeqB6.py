#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         calcSSeqB6
# Date:         14.08.2023
# Author:       Dr. Pascal A. Schirmer
# Version:      V.0.2
# Copyright:    Pascal Schirmer
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
# Import libs
#######################################################################################################################
# ==============================================================================
# Internal
# ==============================================================================
from src.general.helpFnc import deadTime
from src.general.helpFnc import cbInter
from src.general.helpFnc import con2dis
from src.general.genSwSeq import genSwSeq
from src.general.svPWM import svPWM

# ==============================================================================
# External
# ==============================================================================
import numpy as np
from scipy import signal


#######################################################################################################################
# Function
#######################################################################################################################
def calcSSeqB6_CB(ref, t, Mi, setupPara, setupTopo):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Init
    # ==============================================================================
    x0 = {}
    x = {}
    s = {}
    xs = {}
    xsh = {}

    # ==============================================================================
    # Parameters
    # ==============================================================================
    fs = setupPara['PWM']['fs']
    Ts = 1 / fs
    fel = setupTopo['fel']
    id = ['A', 'B', 'C']

    # ==============================================================================
    # Variables
    # ==============================================================================
    tmin = int(setupPara['PWM']['tmin'] / (t[1] - t[0]))
    td = int(setupPara['PWM']['td'] / (t[1] - t[0]))

    ###################################################################################################################
    # Pre-Processing
    ###################################################################################################################
    # ==============================================================================
    # Scale reference
    # ==============================================================================
    x0['A'] = Mi * ref['A'] / np.max(ref['A'])
    x0['B'] = Mi * ref['B'] / np.max(ref['B'])
    x0['C'] = Mi * ref['C'] / np.max(ref['C'])
    xN0 = np.zeros(np.size(x0['A']))
    xAll = np.vstack((x0['A'], x0['B'], x0['C'])).transpose()

    # ==============================================================================
    # Clark Transform
    # ==============================================================================
    phi = np.arcsin(ref['A'][0] / np.max(ref['A']))

    # ==============================================================================
    # Zero-Sequence
    # ==============================================================================
    # ------------------------------------------
    # SPWM
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "SPWM":
        xN0 = np.zeros(np.size(x0['A']))

    # ------------------------------------------
    # SVPWM
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "SVPWM":
        xN0 = 1 / 4 * Mi * signal.sawtooth(3 * 2 * np.pi * fel * (t - (0.25 - phi / (2 * np.pi)) / fel), 0.5)

    # ------------------------------------------
    # THIPWM1/4
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "THIPWM4":
        xN0 = 1 / 4 * Mi * np.sin(3 * 2 * np.pi * fel * (t + (phi / (2 * np.pi)) / fel))

    # ------------------------------------------
    # THIPWM1/6
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "THIPWM6":
        xN0 = 1 / 4 * Mi * np.sin(3 * 2 * np.pi * fel * (t + (phi / (2 * np.pi)) / fel))

    # ------------------------------------------
    # DPWM0
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "DPWM0":
        xAll_s = np.roll(xAll, shift=-int(len(xN0) / 12), axis=0)
        id2 = np.argsort(abs(xAll_s), axis=1)
        for i in range(0, len(xN0)):
            xN0[i] = np.sign(xAll[i, id2[i, 2]]) - xAll[i, id2[i, 2]]

    # ------------------------------------------
    # DPWM1
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "DPWM1":
        xAll_s = np.roll(xAll, shift=0, axis=0)
        id2 = np.argsort(abs(xAll_s), axis=1)
        for i in range(0, len(xN0)):
            xN0[i] = np.sign(xAll[i, id2[i, 2]]) - xAll[i, id2[i, 2]]

    # ------------------------------------------
    # DPWM2
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "DPWM2":
        xAll_s = np.roll(xAll, shift=int(len(xN0) / 12), axis=0)
        id2 = np.argsort(abs(xAll_s), axis=1)
        for i in range(0, len(xN0)):
            xN0[i] = np.sign(xAll[i, id2[i, 2]]) - xAll[i, id2[i, 2]]

    # ------------------------------------------
    # DPWM3
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "DPWM3":
        id2 = np.argsort(abs(xAll), axis=1)
        for i in range(0, len(xN0)):
            xN0[i] = np.sign(xAll[i, id2[i, 1]]) - xAll[i, id2[i, 1]]

    # ------------------------------------------
    # DPWMMIN
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "DPWMMIN":
        xN0 = -1 - np.min(xAll, axis=1)

    # ------------------------------------------
    # DPWMMAX
    # ------------------------------------------
    if setupPara['PWM']['zero'] == "DPWMMAX":
        xN0 = 1 - np.max(xAll, axis=1)

    # ==============================================================================
    # Line-to-Line References
    # ==============================================================================
    x['A'] = x0['A'] + xN0
    x['B'] = x0['B'] + xN0
    x['C'] = x0['C'] + xN0

    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # Carrier
    # ==============================================================================
    if setupPara['PWM']['tri'] == "RE":
        c = signal.sawtooth(2 * np.pi * fs * t, 1) * (-1)
    elif setupPara['PWM']['tri'] == "FE":
        c = signal.sawtooth(2 * np.pi * fs * (t - 0.5 / fs), 0) * (-1)
    elif setupPara['PWM']['tri'] == "AM":
        c = signal.sawtooth(2 * np.pi * fs * t, 1 / 3) * (-1)
    else:
        c = signal.sawtooth(2 * np.pi * fs * (t - 0.5 / fs), 0.5)
    c = (2 * (c - min(c)) / (max(c) - min(c))) - 1

    # ==============================================================================
    # Sampling
    # ==============================================================================
    for i in range(0, len(id)):
        if setupPara['PWM']['samp'] == "RS":
            if setupPara['PWM']['upd'] == "SE":
                xs[id[i]] = con2dis(x[id[i]], t, Ts)
                xsh[id[i]] = np.roll(x[id[i]], int(len(xs[id[i]]) * fel / fs))
            else:
                xs[id[i]] = con2dis(x[id[i]], t, Ts / 2)
                xsh[id[i]] = np.roll(x[id[i]], int(len(xs[id[i]]) * fel / fs / 2))
        else:
            xs[id[i]] = x[id[i]]
            xsh[id[i]] = x[id[i]]

    # ==============================================================================
    # Intersections
    # ==============================================================================
    for i in range(0, len(id)):
        s[id[i]] = cbInter(xs[id[i]], c, Mi, tmin)

        ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # Dead-time
    # ==============================================================================
    if setupPara['PWM']['td'] > 0:
        for i in range(0, len(id)):
            s[id[i]] = deadTime(s[id[i]], td)

    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [xs, xsh, s, c, x, xN0]


#######################################################################################################################
# Function
#######################################################################################################################
def calcSSeqB6_FF(ref, t, Mi, _, setupTopo):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Parameters
    # ==============================================================================
    fel = setupTopo['fel']
    id = ['A', 'B', 'C']

    # ==============================================================================
    # Variables
    # ==============================================================================
    x0 = {}
    s = {}
    x = {}

    ###################################################################################################################
    # Pre-Processing
    ###################################################################################################################
    # ==============================================================================
    # Scale reference
    # ==============================================================================
    x0['A'] = Mi * ref['A'] / np.max(ref['A'])
    x0['B'] = Mi * ref['B'] / np.max(ref['B'])
    x0['C'] = Mi * ref['C'] / np.max(ref['C'])

    # ==============================================================================
    # Carrier
    # ==============================================================================
    c = np.zeros(np.size(t))

    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    for i in range(0, len(id)):
        s[id[i]] = signal.square(2 * np.pi * fel * t - i * (np.pi * 2) / 3, duty=Mi / 2)

    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # Neutral Voltage
    # ==============================================================================
    xN0 = 1 / 3 * (s['A'] + s['B'] + s['C'])

    # ==============================================================================
    # Line-to-Line References
    # ==============================================================================
    x['A'] = x0['A'] + xN0
    x['B'] = x0['B'] + xN0
    x['C'] = x0['C'] + xN0

    # ==============================================================================
    # Output
    # ==============================================================================
    xs = x
    xsh = x

    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [xs, xsh, s, c, x, xN0]


#######################################################################################################################
# Function
#######################################################################################################################
def calcSSeqB6_SV(ref, t, Mi, setupPara, setupTopo):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Init
    # ==============================================================================
    x0 = {}
    s = {}
    x = {}
    xs = {}
    xsh = {}
    mS = {}

    # ==============================================================================
    # Parameters
    # ==============================================================================
    # ------------------------------------------
    # General
    # ------------------------------------------
    fs = setupPara['PWM']['fs']
    fel = setupTopo['fel']
    Tel = 1 / fel
    id = ['A', 'B', 'C']

    # ------------------------------------------
    # PWM
    # ------------------------------------------
    q = int(fs / fel)
    N = int((t[-1] - t[0]) / Tel)
    if setupPara['PWM']['upd'] == "SE":
        Ns = q
    else:
        Ns = 2 * q
    K = int(len(t) / (q * N))
    tmin = int(setupPara['PWM']['tmin'] / (t[1] - t[0]))

    # ==============================================================================
    # Variables
    # ==============================================================================
    ts = np.linspace(0, 2, K)
    ss = np.zeros(np.size(t))
    xN0 = np.zeros(np.size(t))
    rr = np.zeros((Ns * N, 1))
    t1 = np.zeros((Ns * N, 1))
    t2 = np.zeros((Ns * N, 1))
    t0 = np.zeros((Ns * N, 1))
    t7 = np.zeros((Ns * N, 1))
    s['A'] = np.zeros(np.size(t))
    s['B'] = np.zeros(np.size(t))
    s['C'] = np.zeros(np.size(t))
    xs['A'] = np.zeros(np.size(t))
    xs['B'] = np.zeros(np.size(t))
    xs['C'] = np.zeros(np.size(t))

    ###################################################################################################################
    # Pre-Processing
    ###################################################################################################################
    # ==============================================================================
    # Scale reference
    # ==============================================================================
    x0['A'] = Mi * ref['A'] / np.max(ref['A'])
    x0['B'] = Mi * ref['B'] / np.max(ref['B'])
    x0['C'] = Mi * ref['C'] / np.max(ref['C'])

    # ==============================================================================
    # Clark Transform
    # ==============================================================================
    ref['alpha'] = ref['A'] - 0.5 * ref['B'] - 0.5 * ref['C']
    ref['beta'] = np.sqrt(3) / 2 * ref['B'] - np.sqrt(3) / 2 * ref['C']
    phi = np.arctan2(ref['beta'], ref['alpha'])

    # ==============================================================================
    # Mapping Functions
    # ==============================================================================
    mS['A'] = [-1, 1, 1, -1, -1, -1, 1, 1]
    mS['B'] = [-1, -1, 1, 1, 1, -1, -1, 1]
    mS['C'] = [-1, -1, -1, -1, 1, 1, 1, 1]

    # ==============================================================================
    # Define Switching Sequence
    # ==============================================================================
    [seq, k] = genSwSeq(setupPara)

    # ==============================================================================
    # Zero-Sequence
    # ==============================================================================
    for i in range(0, len(t)):
        alpha = i * N / len(t) * 2 * np.pi + phi[0] + 2 * np.pi
        [d0, d1, d2, d7, _] = svPWM(k, alpha, Mi)
        xN0[i] = (-d0 - d1 / 3 + d2 / 3 + d7)

    # ==============================================================================
    # Line-to-Line References
    # ==============================================================================
    x['A'] = x0['A'] + xN0
    x['B'] = x0['B'] + xN0
    x['C'] = x0['C'] + xN0

    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # Determine Sector
    # ==============================================================================
    for i in range(0, Ns * N):
        alpha = i / Ns * 2 * np.pi + phi[0] + 2 * np.pi
        [t0[i], t1[i], t2[i], t7[i], rr[i]] = svPWM(k, alpha, Mi)

    # ==============================================================================
    # Switching times
    # ==============================================================================
    if setupPara['PWM']['upd'] == "SE":
        st = np.hstack((t0, t0 + t1, 1 - t7, np.ones((Ns * N, 1)), 1 + t7, 1 + t7 + t2, 2 - t0, 2 * np.ones((Ns * N, 1))))
    else:
        st1 = np.hstack((t0, t0 + t1, 1 - t7, np.ones((Ns * N, 1))))
        st2 = np.roll(np.hstack((1 + t7, 1 + t7 + t2, 2 - t0, 2 * np.ones((Ns * N, 1)))), -1, axis=0)
        st = np.hstack((st1, st2))
        st = st[::2]
        rr = rr[::2]

    # ==============================================================================
    # Switching states
    # ==============================================================================
    for i in range(0, q * N):
        j = 0
        for ii in range(0, K):
            if st[i, j] > ts[ii]:
                ss[ii + K * i] = seq[int(rr[i] - 1)][j]
            else:
                j = j + 1
                ss[ii + K * i] = ss[ii + K * i - 1]

    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # Sampled waveform
    # ==============================================================================
    for i in range(0, len(id)):
        for ii in range(0, len(x[id[i]])):
            if (ii % int(len(t) / (Ns * N))) == 0:
                xs[id[i]][ii] = x[id[i]][ii]
            else:
                xs[id[i]][ii] = xs[id[i]][ii - 1]

    # ==============================================================================
    # Shifted waveform
    # ==============================================================================    
    for i in range(0, len(id)):
        if setupPara['PWM']['upd'] == "SE":
            xsh[id[i]] = np.roll(x0[id[i]], int(len(xs[id[i]]) * fel / fs))
        else:
            xsh[id[i]] = np.roll(x0[id[i]], int(len(xs[id[i]]) * fel / fs / 2))

    # ==============================================================================
    # Switching Function
    # ==============================================================================
    for i in range(0, len(ss)):
        hold = tmin
        for ii in range(0, len(id)):
            if hold >= tmin:
                if Mi != 0:
                    s[id[ii]][i] = mS[id[ii]][int(ss[i])]
                hold = 0
            else:
                s[id[ii]][i] = s[id[ii]][i - 1]
                hold = hold + 1

    # ==============================================================================
    # Outputs
    # ==============================================================================
    c = ss

    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [xs, xsh, s, c, x, xN0]
