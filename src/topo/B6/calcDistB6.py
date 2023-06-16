#######################################################################################################################
#######################################################################################################################
# Title:        PWM Distortion Toolkit for Standard Topologies
# Topic:        Power Electronics
# File:         calcDistB6
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
from scipy.fft import fft

#######################################################################################################################
# Function
#######################################################################################################################
def calcDistB6_Num(t, i_a, v_a, i_dc, v_dc, Vdc, setupTopo):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Parameters
    # ==============================================================================
    fel = setupTopo['fel']
    Tel = 1/fel
    dt = t[1] - t[0]
    K = int(np.round((t[-1]-t[0])/Tel))
    N = int(len(v_a)) 

    # ==============================================================================
    # Variables
    # ==============================================================================
    distAc = {}
    distDc = {}
       
    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    V_a_eff = np.sqrt(1/Tel/K * np.sum(v_a**2 * dt))
    V_a_v1_eff = (1/np.sqrt(2))*2*np.abs(fft(v_a)/N)[K]
    V_a_thd = np.sqrt(V_a_eff**2 - V_a_v1_eff**2)/V_a_eff * Vdc/2
    I_a_eff = np.sqrt(1/Tel/K * np.sum(i_a**2 * dt))
    I_a_v1_eff = (1/np.sqrt(2))*2*np.abs(fft(i_a)/N)[K]
    I_a_thd = np.sqrt(I_a_eff**2 - I_a_v1_eff**2) 
    
    # ==============================================================================
    # DC-Side
    # ==============================================================================
    V_dc_eff = np.sqrt(1/Tel/K * np.sum(v_dc**2 * dt))
    V_dc_v1_eff = np.abs(fft(v_dc)/N)[0]
    V_dc_thd = np.sqrt(V_dc_eff**2 - V_dc_v1_eff**2)
    I_dc_eff = np.sqrt(1/Tel/K * np.sum(i_dc**2 * dt))
    I_dc_v1_eff = np.abs(fft(i_dc)/N)[0]
    I_dc_thd = np.sqrt(I_dc_eff**2 - I_dc_v1_eff**2)
        
    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    distAc['V_a_eff'] = V_a_eff
    distAc['V_a_v1_eff'] = V_a_v1_eff
    distAc['V_a_thd'] = V_a_thd
    distAc['I_a_eff'] = I_a_eff
    distAc['I_a_v1_eff'] = I_a_v1_eff
    distAc['I_a_thd'] = I_a_thd
    
    # ==============================================================================
    # DC-Side
    # ==============================================================================
    distDc['V_dc_eff'] = V_dc_eff
    distDc['V_dc_v1_eff'] = V_dc_v1_eff
    distDc['V_dc_thd'] = V_dc_thd
    distDc['I_dc_eff'] = I_dc_eff
    distDc['I_dc_v1_eff'] = I_dc_v1_eff
    distDc['I_dc_thd'] = I_dc_thd
    
    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [distAc, distDc]


#######################################################################################################################
# Function
#######################################################################################################################
def calcDistB6_Ana(t, i_a, v_a, Ia1, Mi, Vdc, setupTopo, setupPara):
    ###################################################################################################################
    # Initialisation
    ###################################################################################################################
    # ==============================================================================
    # Parameters
    # ==============================================================================
    fs = setupPara['PWM']['fs']
    fel = setupTopo['fel']
    Tel = 1/fel
    K = int(np.round((t[-1]-t[0])/Tel))
    L = setupTopo['L']
    R = setupTopo['R']
    Z = np.sqrt(R**2 + (2*np.pi*fel*L)**2)
    
    # ==============================================================================
    # Variables
    # ==============================================================================
    distAc = {}
    distDc = {}
    
    ###################################################################################################################
    # Pre-Processing
    ###################################################################################################################
    # ==============================================================================
    # Load angle
    # ==============================================================================
    Y = fft(v_a)
    phiV1 = np.angle(Y)[K]
    Y = fft(i_a)
    phiI1 = np.angle(Y)[K]
    phi = phiV1 - phiI1
        
    ###################################################################################################################
    # Calculation
    ###################################################################################################################
    # ==============================================================================
    # AC-Side
    # ==============================================================================
    # ------------------------------------------
    # Voltages
    # ------------------------------------------
    V_a_eff = Vdc*np.sqrt(Mi/(np.sqrt(3)*np.pi))
    V_a_v1_eff = 1/np.sqrt(2) * Vdc/2 * Mi
    V_a_thd = Vdc/2 * np.sqrt(1 - Mi * (np.sqrt(3)*np.pi)/8)
    
    # ------------------------------------------
    # Current
    # ------------------------------------------
    # General
    I_a_eff = V_a_eff / Z 
    I_a_v1_eff = V_a_v1_eff / Z 
    
    # Distortion
    if setupPara['PWM']['type'] == "FF":
        I_a_thd = 0.0417 * (Vdc/2) * (1/(2*np.pi*fel*L)) * Mi
    else:
        # 0127 (SPWM)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "SPWM": 
            HDF = 3/2*Mi**2 - 4*np.sqrt(3)/np.pi*Mi**3 + 9/8*Mi**4
        
        # 0127 (SVPWM)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "SVPWM": 
            HDF = 3/2*Mi**2 - 4*np.sqrt(3)/np.pi*Mi**3 + (27/16 - 81*np.sqrt(3)/(64*np.pi))*Mi**4
        
        # 0127 (THIPWM4)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "THIPWM4": 
            HDF = 3/2*Mi**2 - 4*np.sqrt(3)/np.pi*Mi**3 + 63/64*Mi**4
        
        # 0127 (THIPWM6)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "THIPWM4": 
            HDF = 3/2*Mi**2 - 4*np.sqrt(3)/np.pi*Mi**3 + Mi**4
        
        # 0127 (DPWM0)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "DPWM0": 
            HDF_max = 6*Mi**2 - (8*np.sqrt(3) + 45)/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(32*np.pi))*Mi**4
            HDF_min = 6*Mi**2 + (45 - 62*np.sqrt(3))/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(16*np.pi))*Mi**4
            HDF = 0.5*(HDF_max + HDF_min)
            
        # 0127 (DPWM1)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "DPWM1": 
            HDF = 6*Mi**2 - (8*np.sqrt(3) + 45)/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(32*np.pi))*Mi**4
        
        # 0127 (DPWM2)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "DPWM2": 
            HDF_max = 6*Mi**2 - (8*np.sqrt(3) + 45)/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(32*np.pi))*Mi**4
            HDF_min = 6*Mi**2 + (45 - 62*np.sqrt(3))/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(16*np.pi))*Mi**4
            HDF = 0.5*(HDF_max + HDF_min)
            
        # 0127 (DPWM3)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "DPWM3": 
            HDF = 6*Mi**2 + (45 - 62*np.sqrt(3))/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(16*np.pi))*Mi**4
        
        # 0127 (DPWMMAX)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "DPWMMAX": 
            HDF_max = 6*Mi**2 - (8*np.sqrt(3) + 45)/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(32*np.pi))*Mi**4
            HDF_min = 6*Mi**2 + (45 - 62*np.sqrt(3))/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(16*np.pi))*Mi**4
            HDF = 0.5*(HDF_max + HDF_min)
            
        # 0127 (DPWMMIN)
        if setupPara['PWM']['seq'] == "0127" and setupPara['PWM']['zero'] == "DPWMMIN": 
            HDF_max = 6*Mi**2 - (8*np.sqrt(3) + 45)/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(32*np.pi))*Mi**4
            HDF_min = 6*Mi**2 + (45 - 62*np.sqrt(3))/(2*np.pi)*Mi**3 + (27/8 + 27*np.sqrt(3)/(16*np.pi))*Mi**4
            HDF = 0.5*(HDF_max + HDF_min)
        
    # ==============================================================================
    # DC-Side
    # ==============================================================================
    I_dc_eff = Ia1 * np.sqrt(2*np.sqrt(3)/np.pi * Mi*(1/4 + np.cos(phi)**2))
    I_dc_v1_eff = 3/4 * np.sqrt(2) * Ia1 * np.cos(phi)
    I_dc_thd = np.sqrt(2*Mi * (np.sqrt(3)/(4*np.pi) + np.cos(phi)**2 * (np.sqrt(3)/np.pi - 9/16*Mi))) *  Ia1
        
    ###################################################################################################################
    # Post-Processing
    ###################################################################################################################
    # ==============================================================================
    # Denormalization
    # ==============================================================================
    if setupPara['PWM']['type'] == "FF":
        I_a_thd = I_a_thd
    else:
        I_a_thd = Vdc/(24*L*fs) * np.sqrt(HDF)
    
    # ==============================================================================
    # Outputs Distortion
    # ==============================================================================
    # ------------------------------------------
    # AC-Side
    # ------------------------------------------
    distAc['V_a_eff'] = V_a_eff
    distAc['V_a_v1_eff'] = V_a_v1_eff
    distAc['V_a_thd'] = V_a_thd
    distAc['I_a_eff'] = I_a_eff
    distAc['I_a_v1_eff'] = I_a_v1_eff
    distAc['I_a_thd'] = I_a_thd
    
    # ------------------------------------------
    # DC-Side
    # ------------------------------------------
    distDc['V_dc_eff'] = 0
    distDc['V_dc_v1_eff'] = 0
    distDc['V_dc_thd'] = 0
    distDc['I_dc_eff'] = I_dc_eff
    distDc['I_dc_v1_eff'] = I_dc_v1_eff
    distDc['I_dc_thd'] = I_dc_thd
    
    ###################################################################################################################
    # Return
    ###################################################################################################################
    return [distAc, distDc]