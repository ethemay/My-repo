#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         plotTrans_B2
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

# ==============================================================================
# External
# ==============================================================================
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
from scipy.fft import fft


#######################################################################################################################
# Function
#######################################################################################################################
def plotTrans_B2(time, freq, setupPara, setupData, setupTopo, setupExp):
    ###################################################################################################################
    # MSG IN
    ###################################################################################################################
    print("START: Plotting Transient B2")

    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Init
    # ==============================================================================
    # ------------------------------------------
    # Time
    # ------------------------------------------
    timeSw = time['Sw']
    timeAc = time['Ac']
    timeDc = time['Dc']
    timeElec = time['Elec']
    timeLoss = time['Loss']
    timeTher = time['Ther']

    # ------------------------------------------
    # Frequency
    # ------------------------------------------
    freqSw = freq['Sw']

    # ==============================================================================
    # Parameters
    # ==============================================================================
    fel = setupTopo['fel']
    fs = setupPara['PWM']['fs']
    fsim = setupExp['fsim']
    Q = int(fs / fel)
    R = setupTopo['R']
    L = setupTopo['L']
    Mi = setupData['stat']['Mi']
    Vdc = setupData['stat']['Vdc']
    phiE = setupTopo['phiE']
    down = setupData['stat']['cyc'] - 2
    Ta = setupData['trans']['Tc']

    # ==============================================================================
    # Variables
    # ==============================================================================
    t = timeSw['t'].values
    tel = time['t']
    f = fsim * np.linspace(0, 0.5, int(len(t) / 2)) / fel

    ###################################################################################################################
    # Pre-Processing
    ###################################################################################################################
    # ==============================================================================
    # General
    # ==============================================================================
    # ------------------------------------------
    # Limits
    # ------------------------------------------
    K = int(np.round((t[-1] - t[0]) * fel))
    start = 0
    ende = int((len(t) - 1) / K) + 1

    # ------------------------------------------
    # Change time
    # ------------------------------------------
    t = t[start:ende]
    timeSw = timeSw[:][start:ende]
    for c1 in timeAc:
        timeAc[c1] = timeAc[c1][start:ende]
    for c1 in timeDc:
        timeDc[c1] = timeDc[c1][start:ende]

    # ==============================================================================
    # Load angle Total
    # ==============================================================================
    Y = fft(timeAc['v_a'])
    phiV = np.angle(Y)[1]
    Y = fft(timeAc['i_a'])
    phiI = np.angle(Y)[1]
    phi = phiV - phiI + 2 * np.pi
    while phi > 2 * np.pi:
        phi = phi - 2 * np.pi

    # ==============================================================================
    # Load angle RL
    # ==============================================================================
    angZ = math.atan2(2 * np.pi * fel * L, R)

    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # Switching Function
    # ==============================================================================
    gs = gridspec.GridSpec(3, 2)
    pl.figure()
    txt = "Modulation Functions for: " + "$M_{i}$=" + str(Mi) + "$ ,Q$=" + str(Q) + ", Sampling: " + str(
        setupPara['PWM']['samp']) + ", Update: " + str(setupPara['PWM']['upd']) + " and Edge Trigger: " + str(
        setupPara['PWM']['tri'])
    pl.suptitle(txt, size=18)
    pl.subplots_adjust(hspace=0.35, wspace=0.20, left=0.075, right=0.925, top=0.90, bottom=0.075)

    # ------------------------------------------
    # Modulation
    # ------------------------------------------
    ax1 = pl.subplot(gs[0, :])
    ax2 = ax1.twinx()
    ax1.plot(t, timeSw['c'], 'k')
    ax2.plot(t, timeSw['v_ref'] / (Vdc / 2), color='tab:blue')
    pl.title('Carrier and Reference Waveform')
    pl.xlabel('t in (sec)')
    ax1.set_ylabel('c(t)', color='black')
    ax2.set_ylabel('v(t) (p.u)', color='black')
    pl.legend(["$c$", "$v_{a}^{*}$"], loc='upper right')
    pl.grid('on')

    # ------------------------------------------
    # Switching Waveform
    # ------------------------------------------
    # Time-Domain
    pl.subplot(gs[1, 0])
    pl.plot(t, timeSw['s'])
    pl.title('Time-domain Switching Function')
    pl.xlabel('t in (sec)')
    pl.ylabel("$s_{a}(t)$ (p.u)")
    pl.grid('on')

    # Freq-Domain
    pl.subplot(gs[2, 0])
    pl.stem(f[::down], freqSw['Sa'][::down])
    pl.xlim(0, 50)
    pl.title('Frequency-domain Switching Function')
    pl.xlabel("$f/f_{1}$ (Hz/Hz)")
    pl.ylabel("$S_{a}(f)$ (p.u)")
    pl.yscale('log')
    pl.ylim(0.0001, )
    pl.grid('on')

    # ------------------------------------------
    # Reference Waveform
    # ------------------------------------------
    # Time-Domain
    pl.subplot(gs[1, 1])
    pl.plot(t, timeSw['xs'])
    pl.title('Time-domain Sampled Reference')
    pl.xlabel('t in (sec)')
    pl.ylabel("$x_{a}(t)$ (p.u)")
    pl.grid('on')

    # Freq-Domain
    pl.subplot(gs[2, 1])
    pl.stem(f[::down], freqSw['Xas'][::down])
    pl.xlim(0, 50)
    pl.title('Frequency-domain Sampled Reference')
    pl.xlabel("$f/f_{1}$ (Hz/Hz)")
    pl.ylabel("$X_{a}(f)$ (p.u)")
    pl.yscale('log')
    pl.ylim(0.0001, )
    pl.grid('on')

    # ==============================================================================
    # Current/Voltage
    # ==============================================================================
    plt.figure()
    txt = "Currents and Voltages B2 Bridge for PWM Control with: " + "$V_{dc}$=" + str(Vdc) + "V, " + "$M_{i}$=" + str(
        Mi) + "$ ,Q$=" + str(Q) + ", $\phi_{RL}=$" + str(int(math.degrees(angZ))) + "deg" + ", $\phi_{E}=$" + str(
        int(phiE)) + "deg" + ", $\phi_{VI}=$" + str(int(math.degrees(phi))) + "deg"
    plt.suptitle(txt, size=18)
    plt.subplots_adjust(hspace=0.35, wspace=0.35, left=0.075, right=0.925, top=0.90, bottom=0.075)

    # ------------------------------------------
    # Phase
    # ------------------------------------------
    # Current
    plt.subplot(2, 2, 1)
    plt.plot(t, timeAc['i_a'])
    plt.ylabel("$i_{a}(t)$ (A)")
    plt.title('Time-domain Currents AC-Side')
    plt.xlabel('time in (sec)')
    plt.grid('on')

    # Voltage
    plt.subplot(2, 2, 2)
    plt.plot(t, timeAc['v_a0'], t, timeAc['v_a'], t, timeAc['v_L'], t, timeSw['e'])
    plt.ylabel("$v_{a}(t)$ (V)")
    plt.title('Time-domain Voltages AC-Side')
    plt.xlabel('time in (sec)')
    plt.legend(["$v_{a0}(t)$", "$v_{a}(t)$", "$v_{L}(t)$", "$e(t)$"], loc='upper right')
    plt.grid('on')

    # ------------------------------------------
    # DC-Link
    # ------------------------------------------
    # Current
    plt.subplot(2, 2, 3)
    plt.plot(t, timeDc['i_d_p'], t, np.mean(timeDc['i_d_p']) * np.ones(np.size(timeDc['i_d_p'])), '--')
    plt.ylabel("$i_{dc}(t)$ (A)")
    plt.title('Time-domain Currents DC-Side')
    plt.xlabel('time in (sec)')
    plt.legend(["$i_{dc}^{+}$", "$I_{dc,avg}^{+}$"], loc='upper right')
    plt.grid('on')

    # Voltage
    plt.subplot(2, 2, 4)
    plt.plot(t, timeDc['v_in'], t, timeDc['v_dc'], t, np.mean(timeDc['v_dc']) * np.ones(np.size(timeDc['v_dc'])), '--')
    plt.ylabel("$v_{dc}(t)$ (V)")
    plt.title('Time-domain Voltages DC-Side')
    plt.xlabel('time in (sec)')
    plt.legend(["$v_{in}$", "$v_{dc}$", "$V_{dc,avg}$"], loc='upper right')
    plt.grid('on')

    # ==============================================================================
    # Time-domain Transient
    # ==============================================================================
    plt.figure()
    txt = "Time domain switches B2 bridge for PWM control with: " + "$V_{dc}$=" + str(Vdc) + "V, " + "$M_{i}$=" + str(
        Mi) + ", $\phi_{RL}=$" + str(int(math.degrees(angZ))) + "deg" + ", $\phi_{E}=$" + str(
        int(phiE)) + "deg" + ", $\phi_{VI}=$" + str(int(math.degrees(phi))) + "deg"
    plt.suptitle(txt, size=18)
    plt.subplots_adjust(hspace=0.35, wspace=0.35, left=0.075, right=0.925, top=0.90, bottom=0.075)

    # ------------------------------------------
    # Switches
    # ------------------------------------------
    # Bridge-Leg A
    plt.subplot(411)
    plt.plot(tel, timeElec['sw']['S1']['v_T'], 'b', tel, timeElec['sw']['S2']['v_T'], 'r', tel,
             timeElec['sw']['S1']['v_D'], 'b--', tel, timeElec['sw']['S2']['v_D'], 'r--')
    plt.title('Voltages Transistors and Diodes')
    plt.ylabel('Voltage in (V)')
    plt.legend(['T1', 'T2', 'D1', 'D2'])
    plt.grid('on')

    plt.subplot(412)
    plt.plot(tel, timeElec['sw']['S1']['i_T'], 'b', tel, timeElec['sw']['S2']['i_T'], 'r', tel,
             timeElec['sw']['S1']['i_D'], 'b--', tel, timeElec['sw']['S2']['i_D'], 'r--')
    plt.title('Currents Transistors and Diodes')
    plt.ylabel('Current in (A)')
    plt.legend(['T1', 'T2', 'D1', 'D2'])
    plt.grid('on')

    plt.subplot(413)
    plt.plot(tel, timeLoss['sw']['S1']['p_T_c'], 'b', tel, timeLoss['sw']['S2']['p_T_c'], 'r', tel,
             timeLoss['sw']['S1']['p_D_c'], 'b--', tel, timeLoss['sw']['S2']['p_D_c'], 'r--')
    plt.title('Conduction Losses Transistors and Diodes')
    plt.ylabel('Power in (W)')
    plt.legend(['T1', 'T2', 'D1', 'D2'])
    plt.grid('on')

    plt.subplot(414)
    plt.plot(tel, timeLoss['sw']['S1']['p_T_s'], 'b', tel, timeLoss['sw']['S2']['p_T_s'], 'r', tel,
             timeLoss['sw']['S1']['p_D_s'], 'b--', tel, timeLoss['sw']['S2']['p_D_s'], 'r--')
    plt.title('Switching Losses Transistors and Diodes')
    plt.ylabel('Power in (W)')
    plt.legend(['T1', 'T2', 'D1', 'D2'])
    plt.grid('on')

    # Capacitor
    plt.figure()
    txt = "Time domain capacitor B2 bridge for PWM control with: " + "$V_{dc}$=" + str(Vdc) + "V, " + "$M_{i}$=" + str(
        Mi) + ", $\phi_{RL}=$" + str(int(math.degrees(angZ))) + "deg" + ", $\phi_{E}=$" + str(
        int(phiE)) + "deg" + ", $\phi_{VI}=$" + str(int(math.degrees(phi))) + "deg"
    plt.suptitle(txt, size=18)
    plt.subplots_adjust(hspace=0.35, wspace=0.35, left=0.075, right=0.925, top=0.90, bottom=0.075)

    plt.subplot(311)
    plt.plot(tel, timeElec['cap']['C1']['v_c'])
    plt.title('Voltage Capacitor')
    plt.ylabel('Voltage in (V)')
    plt.xlabel('time in (sec)')
    plt.grid('on')

    plt.subplot(312)
    plt.plot(tel, timeElec['cap']['C1']['i_c'])
    plt.title('Current Capacitor')
    plt.ylabel('Current in (A)')
    plt.xlabel('time in (sec)')
    plt.grid('on')

    plt.subplot(313)
    plt.plot(tel, timeLoss['cap']['C1']['p_L'])
    plt.title('Losses Capacitor')
    plt.ylabel('Power in (W)')
    plt.xlabel('time in (sec)')
    plt.grid('on')

    # ------------------------------------------
    # Thermal
    # ------------------------------------------
    # Switches
    plt.figure()
    plt.subplot(221)
    plt.plot(tel, timeLoss['sw']['S1']['p_L'], 'r', tel, timeLoss['sw']['S2']['p_L'], 'b', tel,
             timeLoss['sw']['S2']['p_L'] + timeLoss['sw']['S1']['p_L'], 'black')
    plt.title('Losses Switches')
    plt.ylabel('Power in (W)')
    plt.legend(['S1', 'S2', 'B2'])
    plt.grid('on')

    plt.subplot(222)
    plt.plot(tel, timeTher['sw']['T1'], color='b', linestyle='--')
    plt.plot(tel, timeTher['sw']['D1'], color='b', linestyle=':')
    plt.plot(tel, timeTher['sw']['C1'], color='b', linestyle='-')
    plt.plot(tel, timeTher['sw']['T2'], color='r', linestyle='--')
    plt.plot(tel, timeTher['sw']['D2'], color='r', linestyle=':')
    plt.plot(tel, timeTher['sw']['C2'], color='r', linestyle='-')
    plt.plot(tel, Ta * np.ones(np.size(tel)), color='k', linestyle='-')
    plt.title('Thermal Switches (A)')
    plt.ylabel('Temperature in (°C)')
    plt.xticks([], [])
    plt.legend(['T1_j', 'T1_d', 'T1_c', 'T2_j', 'T2_d', 'T2_c', 'Ta'])
    plt.grid('on')

    # Capacitor
    plt.subplot(223)
    plt.plot(tel, timeLoss['cap']['C1']['p_L'])
    plt.title('Losses Capacitor')
    plt.ylabel('Power in (W)')
    plt.xlabel('time in (sec)')
    plt.grid('on')

    plt.subplot(224)
    plt.plot(tel, timeTher['cap']['C1'])
    plt.title('Thermal Capacitor')
    plt.ylabel('Temperature in (°C)')
    plt.xlabel('time in (sec)')
    plt.grid('on')
    plt.show()

    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################

    ###################################################################################################################
    # MSG OUT
    ###################################################################################################################
    print("END: Plotting Transient B2")

    ###################################################################################################################
    # Return
    ###################################################################################################################
