# -*- coding: utf-8 -*-
"""ercot2030_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18GmwYJt0tJEae1LL7Fe6aPXfS5P3SEe9
"""

#GIT - load prices
import pandas as pd
dynamic = pd.read_csv('ERCOT 2030.csv')
dynamic

dfElPrice = dynamic.iloc[:,1]
dfElPrice
Life_1year = len(dfElPrice)
Life_1year

# allows user to input a desired mean
# transforms all values in the data frame to correspond to this new mean
# also checks for negative values and zeroes them out preemptively

def varyMean(desired_mean, df):
    original_mean = df.mean()
    delta = desired_mean - original_mean
    data_list = []
    for i in range(len(df)):
        data = df[i]
        new_data = data + delta
#         if new_data < 0:
#             new_data = 0
        data_list.append(new_data)
    new_df = pd.DataFrame(data_list)[0]
    return new_df

#desired means: 0.00 to 0.07 $/kWh
#GIT - 1.5.21 - CREATE ARRAY OF DFs with different means
import numpy as np
mean_array = np.linspace(0,0.07,num=8)
mean_array
df_array = []
for mean in mean_array:
    df_array.append(varyMean(mean, dfElPrice))
#df_array

#NAME EACH DF
df_array_dict = {}
for i in range(len(mean_array)):
    df_array_dict[str(mean_array[i])]=df_array[i]
df_array_dict.keys()

#find df_mean of any price distribution
Life_1year = len(df_array_dict['0.0'])
df_array_dict['0.04']

#GIT - 1.5.2021 - create 10 years
for mean in df_array_dict:
    df2 = df_array_dict[mean]
    for i in range(9):
        test = df_array_dict[mean].append(df2)
        df_array_dict[mean] = test
    test
    dynamic = test #calls it dynamic again
    dynamic
    Life_hours = len(dynamic)

#4.5.21 - Mode 3 - for each df - updating assumptions
#3.7.21 - Mode 3 - CAPEX varies with current density
#1.8.21 - GIT - DYNAMIC, multiple price distributions, one CAPEX
#12.15.20 - GIT - DYNAMIC, Custom CAPEX
#11.17.20 - GIT - dynamic, baseline IV curve, corrects for efficiency error, new CAPEX amounts
# 11.03.20 - GIT- DYNAMIC
# 10.9.20 - set voltage threshold
# 10.7.20 - set limit on current choices using voltage threshold
# 9.23.20 - increase frequency of negative prices and shift to left (21%, -$0.025 to all prices)
# 9.22.20 - using new price duration curve - more negative values; can't use penalty increased demand because increased negative
# increases value of energy
# 9.9.20
# 9.2.20 - Degr rate (-7)
# 8.27.20: ADDING DYNAMIC DEGRADATION RATE FOR 61 CURRENT DENSITIES
# 8.5.20: ADDING PIECEWISE FUNCTION FOR DEGRADATION RATE (constant of 7)
# 8.4.20: DYNAMIC WITH JOP0 AS LCOH BASELINE AND INTERVALS OF 0.1 FOR JOP

# STEP 1: CALCULATE THE ENERGY CHARGE FOR EACH Jop
# %matplotlib notebook - TO ZOOM IN in external window
import math  # for the exponential function
import numpy as np
import matplotlib.pyplot as plt


f_file = open("ercot2030_1.csv","w")
print("Max Jop", "10 Yr Average Jop", "LCOH","INST_CAPEX", "PV_OPEX","PV_OM","PV_Costs", "PV_KG", file=f_file,sep=",")

df_LCOH_total_list_dict = {} #use to find optimalJop for each df
# print("mean price 0.06")

# January_5_2021 = 0 #counter for testing
#for mean in df_array_dict:
    # January_5_2021 += 1
    # if January_5_2021 == 2: #runs for mean 0 
        # break
    #print("Mean Price:", mean)
    # Technical Variables
Capacity = 1000  # watts
Capacity_kW = 10000   
Jop_rated = 1.7
Vop_rated = 1.743136145279
Stack_cost_1kW = 473.92 #2020 USD 
M_BOP_1kW = 150.10 #2020 USD 
E_BOP_1kW = 130.48 #2020 USD 
CAPEX_per_1kW = Stack_cost_1kW + M_BOP_1kW + E_BOP_1kW #based on 2019 NREL H2A 
Electronics_percentage = 0.26
CAPEX_Electronics = Electronics_percentage*CAPEX_per_1kW
CAPEX_Rest = (1-Electronics_percentage)*CAPEX_per_1kW
A = (Capacity * Capacity_kW) / (Vop_rated * Jop_rated)  # 3,380,663 cm2 electrode area
# print(A)
CAPEX_Rest_Total = CAPEX_Rest*A*Jop_rated*Vop_rated/1000 #constant, 1000 converts to kW



#Eff_rated = 1.23 / Vop_rated
#A = (Capacity * Capacity_kW) / (Vop_rated * Jop_rated)  # 3,380,663 cm2 electrode area
#print("MEA:", A)
n_mol = 2  # constant for H2
F = 96485  # Faraday's constant
#Degradation_Rate = 1.5 * 0.001  # volts for 0 to 2.9v#1.5 mV/1000 hrs, per NREL H2A Current Central PEM Electrolyzer Model
V_threshold = 2.9  # 10.9.20 - voltage at which current removed from options
# do same thing with degradation rate that you did with PWF

# Financial Variables
N_life = 10  # life of electrolyzer
#     Life_1year = 8783
#     Life_hours = Life_1year * 10  # 87,600 hours for 10 years of life
#     CAPEX = (CAPEX_per_1kW * Capacity_kW)  # $1,000 x $10,000 kW (10 MW)
#     Stack_cost = (Stack_cost_1kW * Capacity_kW)
#     M_BOP = (M_BOP_1kW * Capacity_kW)
#     E_BOP = (E_BOP_1kW * Capacity_kW)
#print(CAPEX, Stack_cost, M_BOP, E_BOP)
#print("CAPEX_per_1kW:", CAPEX_per_1kW)
#print("CAPEX:", CAPEX)
#OM = (CAPEX * 0.05)
# print(OM)
DR = 0.10  # discount rate

# CAPEX per hour -- #10.14.20 - CHECK THIS
#M_CAPEX = CAPEX / Life_hours  # from year 0. It is a present value. Over 10 years.
# print(M_CAPEX)

# OM per hour
#M_OM = OM / Life_1year  # Every year from year 1 to 10. It is a future value that must be discounted to year 0.
# print(M_OM)

# check - is the voltage for LHV or HHV??
# 0 to 90 in increments of 0.1


# Jop_range_stop = 61
for Jop_range_stop in range(61,0,-1): #2.26.21 - #middle value is last value, vary range of max Jop so CAPEX varies with range
    Jop = []
    Jop_start = 0.0
    for i in range(Jop_range_stop):  # 10.9.20 - increase to 9A/cm2
        Jop.append(Jop_start)
        Jop_start += 0.1
    # print(Jop)
#         print("Max Jop:", Jop[Jop_range_stop-1], max(Jop))
#         raise Exception
    
    Vop = []
    for i in range(Jop_range_stop):  # increase options to 9A/cm2
        Vop.append(0.156726387554 * (Jop[i]) + 1.47670128643691)

    PReq = []  # kW required per hour
    for i in range(len(Jop)):  # 3 can be changed based on length of Jop
        if Jop[i] != 0:
            PReq.append((A * Jop[i] * Vop[i]) / 1000)  # kW
        else:
            PReq.append(0)

    Degradation_Rate = 0.0015

    def updatePReq(i, Jop_=Jop[i], Vop_=Vop[i]):  # prevents Jop[i] and Vop[i] from being modified
        if Jop[i] != 0:
            PReq[i] = ((A * Jop_ * Vop_) / 1000)  # kW
        else:
            PReq[i] = 0
        # print(i,Vop[i],Eff[i],PReq[i])
        # print(i,Vop[i])
        return PReq[i]

    Vop_copy = Vop[:]  # 10.14.20 STORES DEGRADED VOLTAGE
    Energy_Charge = {}  # 10.9.20 - holds one df
    Degraded_Voltage = {} #10.28.20 - testing
    # print(Jop)
    threshold_list_J = []  # at which current is the threshold reached
    threshold_list_hour = []  # at which hour is threshold reached
    # 10.9.20 - AFTER EVERY 8,760 HOURS COLLECT THE ENERGY CHARGE IN A LIST PER YEAR
    # COLLECT THE 10 DFs INTO A NEW DF FOR DCFA AND APPLY THE DISCOUNT RATE
    Jop_plotting = []  # to graph the chosen current vs fallback current if threshold reached
    Jop_fallback = []
    Vop_plotting = []  # Vop from the IV curve
    Vop_fallback = []  # Vop fallback that has been degraded based on hour
    for i in range(len(Jop)):  # 60 values, increments of 0.1
        temp_EC = []
        temp_degraded_voltage = [] #testing to accumulate degraded voltage
        count = 0
        # 10.7.20 - Where we cycle through hours
        current_index = i
        Jop_temp = Jop[i]
        Vop_temp = Vop[i]
        hour = 0  # first hour is 1
        Degrade_count = 0  # 10.14.20 - counts how many times degradation has been done to apply to the new voltage
        for price in df_array_dict['0.01']:  # 10.9.20 - FUTURE PRICES NEED TO BE DISCOUNTED AS WELL AS THE DISCOUNT RATE FOR THE ENERGY CHARGE?
            count += 1
            hour += 1
            if count == 1000:
                Degrade_count += 1
                # print(count)
                count = 0
                if Jop[i] != 0:
                    current_index = i  # voltage currently operating at
                    Vop_copy[i] += Vop_copy[i] * Degradation_Rate  # 10.14.20 - applies DR every 1k hrs
                    #                 while (Vop[current_index] + (Vop[current_index] * Degradation_Rate)) >= V_threshold:
                    #                     current_index = current_index-1
                    # if (Vop[current_index] + (Vop[current_index] * Degradation_Rate)) >= V_threshold: #10.9.20 - check if voltage is higher than 2.9
                    if Vop_copy[i] >= V_threshold:
                        Vop_temp = Vop_copy[i]  # use the degraded voltage
                        temp_EC.append(np.nan)  # make EC nan
                        temp_degraded_voltage.append(Vop_copy[i])
                    else:  # threshold not reached
                        Vop_temp = Vop_copy[i]  # use the degraded voltage
                        temp_EC.append(
                            price * updatePReq(i, Jop[i], Vop_copy[i]))  # calculate Energy Charge with degraded voltage
                        temp_degraded_voltage.append(Vop_copy[i]) #for printing
                    #                     Jop_temp = Jop[i] #10.17.20 - if threshold not reached, proceed with same current
                    #                     Vop_temp = Vop_copy[i] #already degraded every 1k hrs

                    if Jop[
                        current_index] not in threshold_list_J:  # if the threshold occurred, if I already added the Jop DON'T ADD IT AGAIN
                        threshold_list_J.append(Jop[current_index])
                        threshold_list_hour.append(hour)
                    Vop_plotting.append(Vop[i])
                    Vop_fallback.append(Vop_temp)
                    Jop_plotting.append(Jop[i])
                    Jop_fallback.append(Jop[current_index])
                    # print(price*PReq[i])
                else:
                    temp_EC.append(
                        0)  # EC IS $0 #add degradation rate #Jop0 is a static number for when electrolyzer is off
                    # print(0)
                    temp_degraded_voltage.append(Vop_copy[i])

                Energy_Charge["EC_Jop" + str(round(Jop[i], 2))] = temp_EC  # collects Energy Charges in a dictionary
                Degraded_Voltage["DV_Jop" + str(round(Jop[i], 2))] = temp_degraded_voltage
                #print(Vop_copy[i])
            else:  # anything other than thousands (e.g. 1 to 999 and 1001 to 1999, 2001 t0 2999)
                if Jop[i] != 0:
                    if Vop_copy[i] >= V_threshold:
                        temp_EC.append(np.nan)
                        temp_degraded_voltage.append(Vop_copy[i])
                    else:
                        temp_EC.append(price * updatePReq(i, Jop[i], Vop_copy[i]))
                        temp_degraded_voltage.append(Vop_copy[i])
                else:
                    temp_EC.append(0)  # EC IS $0 for Jop0
                    temp_degraded_voltage.append(Vop_copy[i])
                Energy_Charge["EC_Jop" + str(round(Jop[i], 2))] = temp_EC
                Degraded_Voltage["DV_Jop" + str(round(Jop[i], 2))] = temp_degraded_voltage

    df_LCOH = pd.DataFrame(data=Energy_Charge)  # 10.10.20 - holds all 87,600 ECs
    df_LCOH_total_list = []  # 10.10.20 - holds all of 10 individual df's, 1 for each year
    start = 0
    stop = Life_1year
    for i in range(10):
        # print(start,stop)
        df_LCOH_temp = df_LCOH.iloc[start:stop]
        df_LCOH_total_list.append(df_LCOH_temp)  # 10.10.20 - saves each year in a list so can loop through
        start = stop
        stop = (i + 2) * Life_1year  # 10.10 - cycles though each year

    for df in df_LCOH_total_list:
        df.index = range(Life_1year)

    if Jop[Jop_range_stop-1] > 1.7: 
        CAPEX_Electronics_Total =  CAPEX_Electronics*A*Jop[Jop_range_stop-1]*Vop[Jop_range_stop-1]/1000
        Installation_Factor = 1.19
        Total_CAPEX = (CAPEX_Rest_Total + CAPEX_Electronics_Total)*Installation_Factor
        M_CAPEX = (Total_CAPEX/Life_hours) # hourly kg H2; SAME EVERY YEAR
    elif Jop[Jop_range_stop-1] > 0 and Jop[Jop_range_stop-1] <= 1.7:
        CAPEX_Electronics_Total =  CAPEX_Electronics*A*Jop_rated*Vop_rated/1000
        Installation_Factor = 1.19
        Total_CAPEX = (CAPEX_Rest_Total + CAPEX_Electronics_Total)*Installation_Factor
        M_CAPEX = (Total_CAPEX/Life_hours) # hourly kg H2; SAME EVERY YEAR
    else:
        M_CAPEX = (0)  # 0 kg produced when Jop=0
        
    M_OM = 0.05*10*M_CAPEX #2.18.21 - !!USING *10 to correct because M_OM is taking 5% of M_CAPEX, which is based on 
      #the total capex / 87830. For Year 1 OM we need the sum of 8783 hours M_OM and NOT 87830 hours 
      #varying the CAPEX_E with Jop  
        
    # Rate of fuel production in kg every hour of year 1
    M_kgh2 = []
    for i in range(len(Jop)):
        if Jop[i] != 0:
            M_kgh2.append((Jop[i] * A) / (n_mol * F) * (0.002 * 3600))  # hourly kg H2; SAME EVERY YEAR
        else:
            M_kgh2.append(0)  # 0 kg produced when Jop=0

    for df_LCOH in df_LCOH_total_list:  # 10.10.20 - cycle through and get each year
        for i in range(len(Jop)):
            df_LCOH["kg_Jop" + str(round(Jop[i], 2))] = [np.nan if np.isnan(df_LCOH["EC_Jop" + str(round(Jop[i], 2))][j]) \
                                                          else M_kgh2[i] for j in range(
            Life_1year)]  # 10.27.20 - list, if EC for that hour and current is NaN, make Nan, else use the calc
            df_LCOH["CAP_Jop" + str(round(Jop[i], 2))] = [np.nan if np.isnan(df_LCOH["EC_Jop" + str(round(Jop[i], 2))][j]) \
                                                          else M_CAPEX for j in range(Life_1year)]
            df_LCOH["OM_Jop" + str(round(Jop[i], 2))] = [np.nan if np.isnan(df_LCOH["EC_Jop" + str(round(Jop[i], 2))][j]) \
                                                          else M_OM for j in range(Life_1year)]


    col1 = []
    for df_LCOH in df_LCOH_total_list:
        for i in range(Jop_range_stop):  # 10.9.20 - length now 91
            CAP_name = 'CAP_Jop' + str(round(Jop[i], 2))
            OM_name = 'OM_Jop' + str(round(Jop[i], 2))
            EC_name = 'EC_Jop' + str(round(Jop[i], 2))
            kg_name = 'kg_Jop' + str(round(Jop[i], 2))

            col1.append(CAP_name)
            col1.append(OM_name)
            col1.append(EC_name)
            col1.append(kg_name)

        df_LCOH = df_LCOH[col1]


    # COMPARE ALL COLUMNS AND PICK UP THE MIN mlCOH
    for df_LCOH in df_LCOH_total_list:  # 10.13.20
        for i in range(len(Jop)):
            if i != 0:
                df_LCOH["mLCOH_Jop" + str(round(Jop[i], 2))] = (df_LCOH["CAP_Jop" + str(round(Jop[i], 2))] + df_LCOH[
                "OM_Jop" + str(round(Jop[i], 2))] + df_LCOH["EC_Jop" + str(round(Jop[i], 2))]) / df_LCOH[
                                                                "kg_Jop" + str(round(Jop[i], 2))]
            # 10.27.20 - will return NaN if all values are NaN
            else:
                df_LCOH["mLCOH_Jop" + str(round(Jop[i], 2))] = 10000  # zero never selected

        mLCOH_title_list = []

        for i in range(Jop_range_stop):  # 10.13.20
            mLCOH_title_list.append("mLCOH_Jop" + str(round(Jop[i], 2)))

        df_LCOH["mLCOH_min"] = df_LCOH[mLCOH_title_list].min(axis=1)
        #     print(df_LCOH["mLCOH_min"])

        df_LCOH[mLCOH_title_list].loc[
            0].min()
        df_LCOH

    # WE CANNOT SUM THE mlCOH_min we must sum the EC associated with the mLCOH for the annnual LCOH
    OptimalEC_List_DCFA = []  # 10.13.20 - for all 10 years
    for df_LCOH in df_LCOH_total_list:
        OptimalEC_Year1 = 0  # 10.13.20 - makes for EACH year new columns
        OptimalJop_Year1_List = []
        OptimalEC_Year1_List = []
#"mLCOH_Jop" + str(round(Jop[Jop_range_stop-1], 2))) - 2.28.21
        for i in range(len(df_LCOH["mLCOH_Jop0.0"])):  # we take length of the year; i is along row (60 values of Jop)
            mLCOH_list = []
            # mLCOH_list = [df_LCOH["mLCOH_Jop0"][i], df_LCOH["mLCOH_Jop1"][i], df_LCOH["mLCOH_Jop4"][i]]
            for k in range(Jop_range_stop):  # k collects 91 values into list (instead of 3)
                mLCOH_list.append(df_LCOH["mLCOH_Jop" + str(round(Jop[k], 2))][i])
            temp_mLCOH_min = min(mLCOH_list)
            # print(len(mLCOH_list))

            # then for the minimum LCOH find the location inside the list
            for j in range(len(mLCOH_list)):
                if temp_mLCOH_min == mLCOH_list[j]:  # take the index from the min LCOH
                    index = j  # save the position for which it is associated so it can be used next line
            if i == 0:  # for TESTING
                # print(index)
                pass
            OptimalEC_Year1 += df_LCOH["EC_Jop" + str(round(Jop[index], 2))][i]  # sums the corresponding min EC
            OptimalEC_Year1_List.append(df_LCOH["EC_Jop" + str(round(Jop[index], 2))][i])  # adds all to df
            OptimalJop_Year1_List.append(Jop[index])

        OptimalEC_List_DCFA.append(OptimalEC_Year1)  # 10.13.20

        df_LCOH["m_ECmin"] = OptimalEC_Year1_List  # creates the df column
        df_LCOH["OptimalJop"] = OptimalJop_Year1_List

    # STEP 3: SUM MINIMUM kg H2
    # for the minimum find the corresponding kg, put in a new column and sum
    OptimalKG_List_DCFA = []  # 10.13.20
    for df_LCOH in df_LCOH_total_list:
        OptimalKG_Year1 = 0
        # cycle through each row and find the minimum LCOH
        OptimalKG_Year1_List = []
        for i in range(len(df_LCOH["mLCOH_Jop0.0"])):
            mLCOH_list = []
            # mLCOH_list = [df_LCOH["mLCOH_Jop0"][i], df_LCOH["mLCOH_Jop1"][i], df_LCOH["mLCOH_Jop4"][i]]
            for k in range(Jop_range_stop):  # k collects 91 values into list (instead of 3)
                mLCOH_list.append(df_LCOH["mLCOH_Jop" + str(round(Jop[k], 2))][i])
            temp_mLCOH_min = min(mLCOH_list)

            # then for the minimum LCOH find the location inside the list
            for j in range(len(mLCOH_list)):
                if temp_mLCOH_min == mLCOH_list[j]:  # take the index from the min LCOH
                    index = j  # save the position for which it is associated so it can be used next line
            if i == 0:  # FOR TESTING
                # print(index)
                pass
            OptimalKG_Year1 += df_LCOH["kg_Jop" + str(round(Jop[index], 2))][i]  # sums the corresponding min kg
            OptimalKG_Year1_List.append(df_LCOH["kg_Jop" + str(round(Jop[index], 2))][i])  # adds all to list to check

        OptimalKG_List_DCFA.append(OptimalKG_Year1)  # 10.13.20

        df_LCOH["m_kgmin"] = OptimalKG_Year1_List

    for df_LCOH in df_LCOH_total_list:  # 10.13.20
        # CAPEX YEAR 1
        CAPEX_Year1 = df_LCOH["CAP_Jop0.0"].sum()

        # OM YEAR 1
        OM_Year1 = df_LCOH["OM_Jop"+str(round(Jop[Jop_range_stop-1],2))].sum() #2.26.21 - take max OM in range
            #2.26.21 - gives the last year values but that's OK because OM will not change, as it is 
            #based on CAPEX

        # LCOH MIN for year 1
        LCOHmin_Year1 = (CAPEX_Year1 + OM_Year1 + OptimalEC_Year1) / OptimalKG_Year1
        # LCOHmin_Year1 #2.3395942749618563


    df_DCFA = pd.DataFrame(data={})
    df_DCFA["Year"] = list(range(0, 11))

    df_DCFA["CAPEX"] = [Total_CAPEX if i == 0 else 0 for i in range(11)]
    # df_DCFA

    df_DCFA["PWF"] = [1 / (1 + DR) ** df_DCFA["Year"][i] for i in range(11)]

    # OM
    df_DCFA["PV_OM"] = [0 if i == 0 else (OM_Year1 * df_DCFA["PWF"][i]) for i in range(11)]

    # EC
    OptimalEC_List_DCFA.insert(0, 0)
    df_DCFA["PV_EC"] = [0 if i == 0 else (OptimalEC_List_DCFA[i] * df_DCFA["PWF"][i]) for i in range(11)]

    # kg
    OptimalKG_List_DCFA.insert(0, 0)
    df_DCFA["PV_KG"] = [0 if i == 0 else (OptimalKG_List_DCFA[i] * df_DCFA["PWF"][i]) for i in range(11)]

    # STEP 4: CALCULATE LCOH

    PV_Costs = (df_DCFA["CAPEX"].sum() + df_DCFA["PV_OM"].sum() + df_DCFA[
        "PV_EC"].sum())  # 10.13.20 - use PV_EC not PV_EC_UPDATED

    PV_KG = df_DCFA["PV_KG"].sum()

    # Lifetime LCOH for when Jop0 LCOH is for mean price from dataset of electricity prices


    Lifetime_LCOH_dynamic_Jop0baseline = PV_Costs / PV_KG

    # CONTRIBUTION ANALYSIS
    CAPEX_Cont = df_DCFA["CAPEX"].sum() / PV_Costs * 100

    OM_Cont = df_DCFA["PV_OM"].sum() / PV_Costs * 100

    EC_Cont = df_DCFA["PV_EC"].sum() / PV_Costs * 100

    # FIND KG OF PRODUCTION
    df_DCFA["PV_KG"].sum()

    #1.5.21 - create a dictionary of mean values to find optimal Jop for each distribution

    df_LCOH_total_list_dict[mean] = df_LCOH_total_list

    OptimalJop_mean = []
    for year in range(10):
        OptimalJop_mean.append(df_LCOH_total_list[year]["OptimalJop"].mean())
    Average_Jop_10yr = sum(OptimalJop_mean) / len(OptimalJop_mean) 
    Year1_Jop = OptimalJop_mean[0]
    Year10_Jop = OptimalJop_mean[9]


    #print("MEA:", A)
    # print("Max Jop:", Jop[Jop_range_stop-1])
    # print("10 Yr Average Jop:", Average_Jop_10yr)
    # print("INST_CAP:", df_DCFA["CAPEX"].sum())
    # print("PV_KG:" , df_DCFA["PV_KG"].sum())
    # print("PV_EC:", df_DCFA["PV_EC"].sum())
    # print("PV_OM:", df_DCFA["PV_OM"].sum())
    # print("LCOH:", Lifetime_LCOH_dynamic_Jop0baseline)
    print(mean, Jop[Jop_range_stop-1],Average_Jop_10yr,Lifetime_LCOH_dynamic_Jop0baseline, df_DCFA["CAPEX"].sum(), df_DCFA["PV_EC"].sum(), df_DCFA["PV_OM"].sum(), PV_Costs, PV_KG, file=f_file,sep=",") #1.9.21 - write to csv as 3 columns
    #Jop_ += 0.1 #the step interval for Jop_rated; must be down here or order is wrong
    
#print("Max Jop", "Average Jop", "LCOH","CAPEX", "PV_OPEX","PV_OM","PV_Costs", "PV_KG", file=f_file,sep=",")

f_file.close()
df_csv = pd.read_csv("ercot2030_1.csv") 
df_csv