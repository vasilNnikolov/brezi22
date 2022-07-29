from astropy.io import fits
import numpy as np
import glob
import astroalign as aa
import matplotlib.pyplot as plt
from datetime import datetime

startTime = datetime.now()

all_darks = np.empty((1287, 1792, 0))

#Darks for the light frames
#Заснели сме даркове за кадрите със същата експозиция 
#Стакваме ги като 3д матрица и им вземаме медината,това се нарича мастър дарк кадър

for file in glob.glob('C:/Users/admin/Desktop/Ivan_Kalina/Dark-*_300s_Bin2.fit'):
   
    f = fits.open(file)[0].data
    all_darks = np.dstack((all_darks, f))

master_dark_light = np.median(all_darks, axis = 2)

print("done!")

# Dark for the flat fields
#Заснели сме даркове за флатовете(различни от за реалните кадри, защото имат различни експозиции)
#Стакваме ги като 3д матрица и им вземаме медината,това се нарича мастър дарк

for file in glob.glob('C:/Users/admin/Desktop/Ivan_Kalina/Flat_Dark-*_15s_Bin2.fit'):
   
    f = fits.open(file)[0].data
    all_darks = np.dstack((all_darks, f))

master_dark_flat = np.median(all_darks, axis = 2)

all_flats = np.empty((1287, 1792, 0))

# Flat fields
# Шумът от дарка се появява и при заснемане на флат кадрите, затова за да имаме чист дарк трябва от заснетите файлове да извадим мастър дарка. това се нарича мастър флат
# Също така нормирираме флатовете, за да избехнем ефектите от геометрията

print("done!")

for file in glob.glob(r'C:\Users\admin\Desktop\Ivan_Kalina\Flat-*_R_15s_Bin2.fit'):

    flat = fits.open(file)[0].data
    flat_dark = flat - master_dark_flat
    flat_dark_norm = flat_dark / np.median(flat_dark)
    all_flats = np.dstack((all_flats, flat_dark_norm))

master_flat = np.median(all_flats, axis = 2)
#print(master_flat)
#print(np.count_nonzero(master_flat==0))

print("done!")

#Light frames
# Изчистваме всички заснети кадри, като от тях вадим мастър дарка за кадрите...йей имаме готова за обработка снимка
#lights = np.empty((1287, 1792, 0))

i = 1
for file in glob.glob(r'C:\Users\admin\Desktop\Ivan_Kalina\NGC185-*_R_300s_Bin2.fit'):
    light = fits.open(file)[0].data
    light_dark = light - master_dark_light
    light_processed = light_dark / master_flat
    #lights = np.dstack((lights, light_processed))
    #print(lights.shape)
    #print(light_processed.shape)
    #print(np.stack((lights, light_processed), axis=2).size)
    #print(np.stack((lights, light_processed), axis=1).size)
    #print(np.stack((lights, light_processed), axis=0).size)
    hdu = fits.PrimaryHDU(light_processed)
    hdu.writeto("C:/Users/admin/Desktop/Ivan_Kalina/purvichna_obrabotka-" + str(i) + ".fits")
    print(i)
    i += 1

print("done!")



#Align
# При заснемане имаме малко пресместване, този код ги подрежда така, че при наслагването всичко да е точно



print("done!")
print(datetime.now() - startTime)

