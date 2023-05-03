#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         start
# Date:         01.04.2023
# Author:       Dr. Pascal A. Schirmer
# Version:      V.0.1
# Copyright:    Pascal Schirmer
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
# Import external libs
#######################################################################################################################
# ==============================================================================
# Internal
# ==============================================================================
from main import main
from src.general.helpFnc import initSetup, initPath

# ==============================================================================
# External
# ==============================================================================
import warnings
import numpy as np

#######################################################################################################################
# Format
#######################################################################################################################
warnings.filterwarnings("ignore")

#######################################################################################################################
# Paths
#######################################################################################################################
setupPath = initPath('PyPowerSim')

#######################################################################################################################
# Inits
#######################################################################################################################
[setupExp, setupData, setupPara, setupTopo] = initSetup()

#######################################################################################################################
# Configuration
#######################################################################################################################
# ==============================================================================
# General Settings
# ==============================================================================
# ------------------------------------------
# Experiment
# ------------------------------------------
setupExp['Name'] = "test"                                                                                               # name of the simulation (str)
setupExp['Author'] = "Pascal Schirmer"                                                                                  # name of the responsible person (str)
setupExp['debug'] = 0                                                                                                   # (0): debug mode de-activated, (1): debug mode activated level-1, (2): debug mode activated level-2

# ------------------------------------------
# Operating Mode
# ------------------------------------------
setupExp['type'] = 0                                                                                                    # (0): sweep analysis, (1): steady-state analysis, (2): transient analysis
setupExp['loop'] = 'CL'                                                                                                 # (CL): closed-loop, (OL): open-loop
setupExp['freqPar'] = 'fs'                                                                                              # (fs): values are updated earliest after switching cycle, (fel): values are updated earliest after fundamental cycle
setupExp['freqAvg'] = 'none'                                                                                            # (none): no averaging is used (fs): values are averaged over switching cycle, (fel): values are averaged over fundamental cycle

# ------------------------------------------
# Numerical
# ------------------------------------------
setupExp['fsim'] = 5e5                                                                                                  # simulation frequency (Hz)
setupExp['tol'] = 1e-6                                                                                                  # tolerance in percent with respect to the previous converged result
setupExp['eps'] = 1e-12                                                                                                 # small numerical tolerance

# ------------------------------------------
# Output
# ------------------------------------------
setupExp['plot'] = 1                                                                                                    # (0): no results are plotted, (1): results are plotted
setupExp['save'] = 0                                                                                                    # (0): no results are saved, (1): results are saved

# ==============================================================================
# Operating Point
# ==============================================================================
# ------------------------------------------
# General
# ------------------------------------------
# Transient
setupData['trans']['tmax'] = 25/50                                                                                       # maximum time for transient analysis (sec)
setupData['trans']['Tc'] = 50.0                                                                                         # reference temperature of all components (°C)
setupData['trans']['Tj'] = 50.0                                                                                         # core temperature at t=0 of all components (°C)

# Stationary
setupData['stat']['cyc'] = 2                                                                                            # number of fundamental cycles used for stationary analysis
setupData['stat']['W'] = 25                                                                                             # number of datapoints for sweep analysis
setupData['stat']['Tj'] = 50.0                                                                                          # core temperature of all components (°C)
setupData['stat']['Tc'] = 50.0                                                                                          # reference temperature of all components (°C)

# ------------------------------------------
# Parameter
# ------------------------------------------
setupData['stat']['Mi'] = 1.00                                                                                          # modulation index (Mi) for distortion analysis                                                                                                # power factor cos_phi
setupData['stat']['Vdc'] = 400                                                                                          # DC-Link voltage (V)
setupData['stat']['phi'] = 0.0                                                                                          # load angle output voltage (deg)

# ==============================================================================
# Topology
# ==============================================================================
# ------------------------------------------
# Hardware
# ------------------------------------------
setupTopo['SwiName'] = "IKQ75N120CS6"                                                                                   # filename of the parameter set
setupTopo['CapName'] = "Elco"                                                                                           # filename of the parameter set

# ------------------------------------------
# Source
# ------------------------------------------
setupTopo['sourceType'] = "B6"                                                                                          # (B2): half bridge, (B4): full bridge, (B6): two-level three phase converter

# ------------------------------------------
# Filter
# ------------------------------------------
# Input
setupTopo['inpFilter'] = 0                                                                                              # 0) input filter is deacitvated, 1) input filter is activated
setupTopo['Rinp'] = 1e-3                                                                                                # input filter resistance (Ohm)
setupTopo['Linp'] = 2e-3                                                                                                # input filter inductance (H)
setupTopo['Cinp'] = 1e-3                                                                                                # input filter capacitance (F)

# Output
setupTopo['outFilter'] = 0                                                                                              # 0) output filter is deacitvated, 1) output filter is activated
setupTopo['Rout'] = 0                                                                                                   # output filter resistance (Ohm)
setupTopo['Lout'] = 1e-3                                                                                                # output filter inductance (H)
setupTopo['Cout'] = 1e-3                                                                                                # output filter capacitance (F)

# ------------------------------------------
# Load
# ------------------------------------------
# Parameters
setupTopo['R'] = 5.0                                                                                                    # resistance in (Ohm)
setupTopo['L'] = 5e-3                                                                                                   # inductance in (H)
setupTopo['E'] = 0                                                                                                      # induced voltage in (V)
setupTopo['phiE'] = 0                                                                                                   # load angle induced voltage (deg)

# Waveform
setupTopo['wave'] = "sin"                                                                                               # (con): constant, (sin): sinusoidal, (tri): triangular                                                                                   
setupTopo['fel'] = 50                                                                                                   # waveform frequency in (Hz)

# ==============================================================================
# Pulse-Width-Modulation (PWM)
# ==============================================================================
# ------------------------------------------
# General
# ------------------------------------------
setupPara['PWM']['type'] = "SV"                                                                                         # (FF): fundamental frequency, (CB): carrier based, (SV): space vector based
setupPara['PWM']['upd'] = "DE"                                                                                          # (SE): single edge, (DE): double edge 
setupPara['PWM']['samp'] = "RS"                                                                                         # (NS): natural sampling, (RS): regular sampling
setupPara['PWM']['tri'] = "SM"                                                                                          # modulation trigger (RE): rising edge, (FE): falling edge, (SM): symmetrical modulation, (AM): asymmetrical modualtion
setupPara['PWM']['int'] = 0                                                                                             # (0): non-interleaved, (1): interleaving (when multiple carriers are used)
setupPara['PWM']['td'] = 0                                                                                              # dead time (sec)
setupPara['PWM']['tmin'] = 0                                                                                            # minimum on/off period (sec)

# ------------------------------------------
# Modelling
# ------------------------------------------
setupPara['PWM']['loss'] = 1                                                                                            # (0): ideal and lossles, (1): linear modelling
setupPara['PWM']['sw'] = 0                                                                                              # (0): hard switching, (1): soft switching (tbi)

# ------------------------------------------
# Switching Sequence
# ------------------------------------------
setupPara['PWM']['fs'] = 1050                                                                                           # PWM switching frequency (Hz)
setupPara['PWM']['seq'] = "0127"                                                                                        # PWM switching sequence B6 bridge
setupPara['PWM']['zero'] = "SVPWM"                                                                                      # PWM method B6 bridge (SPWM, SVPWM, THIPWM4, THIPWM6, DPWM0, DPWM1, DPWM2, DPWM3, DPWMMAX, DPWMMIN)

# ==============================================================================
# Electrical Parameters
# ==============================================================================
# ------------------------------------------
# Switches (Swi)
# ------------------------------------------
setupPara['Elec']['SwiMdl'] = "tab"                                                                                     # modelling of the switch (con): constant parameters, (pwl): piecewise linear, (tab): tabulated parameters
setupPara['Elec']['SwiType'] = "IGBT"                                                                                   # type of the switch (IGBT, MOSFET->tbi) 
setupPara['Elec']['SwiPara'] = 1                                                                                        # number of switches in parallel  
setupPara['Elec']['SwiSeries'] = 1                                                                                      # number of switches in series 

# ------------------------------------------
# Capacitors (Cap)
# ------------------------------------------
setupPara['Elec']['CapMdl'] = "con"                                                                                     # modelling of the capacitor (con): constant parameters, (tab): tabulated parameters
setupPara['Elec']['CapType'] = "Elco"                                                                                   # type of the capacitor (Elco, MLCC->tbi, Film->tbi) 
setupPara['Elec']['CapPara'] = 1                                                                                        # number of capacitors in parallel 
setupPara['Elec']['CapSeries'] = 1                                                                                      # number of capacitors in series  

# ==============================================================================
# Thermal Parameters
# ==============================================================================
setupPara['Ther']['Heatsink'] = 1                                                                                       # 1) using thermal capacities and resistances of heatsink RC model

#######################################################################################################################
# Calculations
#######################################################################################################################
main(setupExp, setupData, setupTopo, setupPara, setupPath)
