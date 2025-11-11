from lmfit import models
import numpy as np
import matplotlib.pyplot as plt
import csv

mod_linear = models.LinearModel()

force_list = []
displacement_list = []
time_list = []
with open("meting_1.csv", "r") as file:
    my_reader = csv.reader(file, delimiter=",")
    next(my_reader)
    for row in my_reader:
        time_list.append(row[0])
        displacement_list.append(float(row[1]))
        force_list.append(float(row[2])/-1000)

i = 0
a = 0
while i < len(force_list) - 1:
    if np.absolute(force_list[i+1]) - np.absolute(force_list[i]) > 0.1:
        a= i
        print(a)
        print(np.absolute(force_list[i]))
        print(np.absolute(force_list[i+1]))
        i = len(force_list)
    i += 1
    
new_force_list = []
new_displacement_list = []
    
b = a
while b < len(force_list) - 1:
    if force_list[b+1] - force_list[b] > -0.05:
        c=b
        b = len(force_list)
    b +=1
    
while a < len(force_list)-c:
    new_force_list.append(force_list[a])
    new_displacement_list.append(displacement_list[a])
    a += 1
# print(c)
print(a)
print(c)
print(len(force_list))
print(new_displacement_list)   

    

y_err = np.array(len(new_force_list) * [0.003])
y_inv_err = 1/y_err

fit_result = mod_linear.fit(new_force_list, x=new_displacement_list, weights=y_inv_err)

print(fit_result.fit_report())

plt.figure()
plt.xlabel("Displacement (mm)")
plt.ylabel("Force (N)")
plt.errorbar(new_displacement_list, new_force_list, yerr=y_err, fmt='o', markersize=2)
plt.plot(new_displacement_list, fit_result.best_fit, 'r-')
plt.show()

