import pandas as pd
import os
filename = "isochrones/long_isochrone.dat"
with open(filename, "r") as file:
    lines = file.readlines()

header = lines[0]
dataframes_data = [] # list of list of strings
i = 1
while i < len(lines):
    local_lines = []
    while i < len(lines) and lines[i] != "\n":
        local_lines.append(lines[i])
        i += 1
    i += 1
    dataframes_data.append(local_lines)

times = [6.0 + i*0.1 for i in range(31)] 
for index, df_data in enumerate(dataframes_data):
    filename = f"isochrones/isochrone_{10*times[index]:.0f}.dat"
    # first line is useless
    with open(filename, "w") as file:
        file.write(f"{header}")
        file.writelines(df_data[1:])

