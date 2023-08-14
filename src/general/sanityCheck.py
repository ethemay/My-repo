#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         sanityCheck
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
import psutil
import numpy as np


#######################################################################################################################
# Function
#######################################################################################################################
def sanityInput(setupExp, setupData, setupTopo, setupPara):
    ###################################################################################################################
    # MSG IN
    ###################################################################################################################
    print("------------------------------------------")
    print("START: Sanity Checks")
    print("------------------------------------------")

    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    RAM_machine = psutil.virtual_memory().total
    if setupExp['type'] == 2:
        RAM_use = setupExp['fsim']*setupData['stat']['cyc'] * (20 + 24 + 36 + 12) * setupTopo['fel']*setupData['trans']['tmax']
    else:
        RAM_use = setupExp['fsim']*setupData['stat']['cyc'] * (20 + 24 + 36 + 12)

    ###################################################################################################################
    # General Settings
    ###################################################################################################################
    # ==============================================================================
    # RAM (PS 14/01/2023: estimation of RAM based on fsim)
    # ==============================================================================
    if RAM_machine/RAM_use < 5:
        print("WARN: Machine might run out of memory reduce 'setupExp['fsim']', 'setupData['stat']['cyc']' or 'setupData['trans']['tmax']'")
    
    # ==============================================================================
    # Epsilon
    # ==============================================================================
    if setupExp['eps'] * 1e3 > (1/setupExp['fsim']):
        print("WARN: Numerical value 'setupExp['eps']' comparatively large")
    
    ###################################################################################################################
    # Mission Profile
    ###################################################################################################################
    # ==============================================================================
    # Cycles
    # ==============================================================================
    if setupData['stat']['cyc'] < 3:
        print("WARN: To ensure convergence chose 'setupData['stat']['cyc']' >= 3")
    
    # ==============================================================================
    # Cycles
    # ==============================================================================
    if setupTopo['sourceType'] == 'B2' or setupTopo['sourceType'] == 'B4':
        if setupData['stat']['Mi'] > 1.0:
            setupData['stat']['Mi'] = 1.0
            print("WARN: Modulation index Mi too high, limited to 1.000")
    elif setupTopo['sourceType'] == 'B6':
        if setupData['stat']['Mi'] > 4/np.pi:
            setupData['stat']['Mi'] = 1.0
            print("WARN: Modulation index Mi too high, limited to 1.273")

    ###################################################################################################################
    # Parameters
    ###################################################################################################################
    # ==============================================================================
    # PWM
    # ==============================================================================
    # ------------------------------------------
    # Minimum time
    # ------------------------------------------
    if (setupPara['PWM']['tmin'] + setupExp['eps']) < (1/setupExp['fsim']):
        setupPara['PWM']['tmin'] = 0
        print("WARN: Minimum pulse width (tmin) smaller than simulation time (tsim)")
    elif setupPara['PWM']['tmin'] > (1/setupExp['fs']):
        setupPara['PWM']['tmin'] = 0
        print("ERROR: Minimum pulse width (tmin) larger than switching time (ts)")
        
    # ------------------------------------------
    # Dead time
    # ------------------------------------------
    if (setupPara['PWM']['td'] + setupExp['eps']) < (1/setupExp['fsim']):
        setupPara['PWM']['td'] = 0
        print("WARN: Dead-time (td) smaller than simulation time (tsim)")
    elif setupPara['PWM']['td'] > (1/setupExp['fs']):
        setupPara['PWM']['td'] = 0
        print("ERROR: Dead-time (td) larger than switching time (ts)")
    
    # ------------------------------------------
    # Pulse number
    # ------------------------------------------
    if not (setupPara['PWM']['fs'] / setupTopo['fel']).is_integer():
        print("WARN: Pulse-number (q) is not integer, modulation is asynchronous")
    
    # ==============================================================================
    # Electrical
    # ==============================================================================
    
    # ==============================================================================
    # Thermal
    # ==============================================================================
    
    ###################################################################################################################
    # MSG Out
    ###################################################################################################################
    print("------------------------------------------")
    print("END: Sanity Checks")
    print("------------------------------------------")

    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [setupExp, setupData, setupTopo, setupPara]
