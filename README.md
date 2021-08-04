# PEM-TEA-public
Techno-economic analysis of the levelized cost of hydrogen (LCOH) from a proton exchange membrane electrolyzer. 

**Modes 1A-2B**: this code allows the user to input a .csv datasource of one year of historical electricity prices ("locational marginal prices", LMPs), generate mean-varied "modified LMPs" and calculate a LCOH for Modes 1A, 1B, 2A, and 2B for each modified LMP.

In Mode 1A the electrolyzer runs at constant current density (Jop) of 1.7 A cm-2 for its entire lifetime. In Mode 1B, the electrolyzer runs at a constant current density between 0.1 and 6.0 A cm-2, and Jophigh is selected to minimize LCOH. In Mode 2A, “binary” operation, the electrolyzer runs at a "low" state of 0.1 A cm-2 and an "on" state at the rated current density of 1.7 A cm-2. In Mode 2B, the second binary option, the electrolyzer runs at a "low" state of 0.1 A cm-2 and an "on" state, Jop,high. of any one current density between 0.1 and 6.0 A cm-2 that minimizes LCOH. 

**Mode 3 Individual Files**: this code allows the user to input a .csv datasource of one year of historical electricity prices ("locational marginal prices", LMPs), generate mean-varied "modified LMPs" and calculate a LCOH for Mode 3. Since Mode 3 is time-intensive, each of the 8 modified LMPs, ranging from $0.00 per kWh to $0.07 per kWh, have been separated into individual python files with shell scripts to run on a high performance computing infrastructure. The number at the end of the python title indicates the mean price of the LMP dataset (e.g. "caiso2030_0.py" is the code for the CAISO 2030 dataset with a modified LMP mean of $0.00 per kWh.

In Mode 3, the electrolyzer Jop can, at any hour, operate at any current density between 0.1 and 6 A cm-2 that results in the lowest marginal LCOH.

**Boxplots and Histograms**: this code allows the user to generate boxplots and histograms with all five datasets shown in Supplemental Fig. 1 using each of the .csv datasources.
