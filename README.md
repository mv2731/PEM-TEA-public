# PEM-TEA-public
Techno-economic analysis of the levelized cost of hydrogen (LCOH) from a proton exchange membrane electrolyzer. 

**Directory Structure**: 
The "Code" folder includes a file "modes_1_3_h2_tea_31mar2022", which can run all 5 modes. The "Code" folder includes boxplots and histograms as a .ipynb file. The "Source Data" folder contains the .csv files for each of the five original LMP datasets.

**Modes 1A-2B**: this code allows the user to input a .csv datasource of one year of historical electricity prices ("locational marginal prices", LMPs), generate mean-varied "modified LMPs" and calculate a LCOH for Modes 1A, 1B, 2A, and 2B for each modified LMP.

In Mode 1A the electrolyzer runs at constant current density (Jop) of 1.7 A cm-2 for its entire lifetime. In Mode 1B, the electrolyzer runs at a constant current density between 0.1 and 6.0 A cm-2, and Jophigh is selected to minimize LCOH. In Mode 2A, “binary” operation, the electrolyzer runs at a "low" state of 0.1 A cm-2 and an "on" state at the rated current density of 1.7 A cm-2. In Mode 2B, the second binary option, the electrolyzer runs at a "low" state of 0.1 A cm-2 and an "on" state, Jop,high. of any one current density between 0.1 and 6.0 A cm-2 that minimizes LCOH. 

**Mode 3**: this code allows the user to input a .csv datasource of one year of historical electricity prices ("locational marginal prices", LMPs), generate mean-varied "modified LMPs" and calculate a LCOH for Mode 3. 

In Mode 3, the electrolyzer Jop can, at any hour, operate at any current density between 0.1 and 6 A cm-2 that results in the lowest marginal LCOH.

**Boxplots and Histograms**: this code allows the user to generate boxplots and histograms with all five datasets shown in Supplemental Fig. 1 using each of the .csv datasources.

**Optimal Jop Distribution**: this code allows the user to generate boxplots of the optimal current density for ERCOT 2020 and CAISO 2020 given a .csv with columns of hourly optimal Jop by average electricity price. 
