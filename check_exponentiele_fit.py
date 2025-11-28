import csv
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

# --------------------------------------------
# 1. Data inlezen
# --------------------------------------------

force_list = []
displacement_list = []
time_list = []

with open("tetrahede_eerste_meting.csv", "r") as file:
    my_reader = csv.reader(file, delimiter=",")
    next(my_reader)
    for row in my_reader:
        time_list.append(row[0])
        displacement_list.append(float(row[1]))
        force_list.append(float(row[2]) / -1000)   # jouw scaling behouden

# --------------------------------------------
# 2. Filteren vanaf 40 mm + drempel-stop
# --------------------------------------------

new_force = []
new_disp = []

i = 0
breek_drempel = 1       # als kracht >1 N omlaag valt → stoppen
was_prev = None
stoppen = False

while i < len(displacement_list) and stoppen == False:

    if displacement_list[i] > 38:
        if was_prev is None:
            was_prev = force_list[i]

        # stoppen wanneer er in 1 stap meer dan 1 N omlaag valt
        if force_list[i] < was_prev - breek_drempel:
            stoppen = True
        else:
            new_disp.append(displacement_list[i])
            new_force.append(force_list[i])
            was_prev = force_list[i]

    i = i + 1

# --------------------------------------------
# 3. Exponentiële fit: F(x) = A * exp(B*x)
# --------------------------------------------

def expo(x, A, B):
    return A * np.exp(B * x)

mod_exp = Model(expo)

y_err = np.array(np.zeros(len(new_force)) + 0.003)
y_inv_err = 1 / y_err

fit_result = mod_exp.fit(new_force, x=new_disp, weights=y_inv_err,
                         A=0.001, B=0.1)   # startwaarden

print(fit_result.fit_report())

# --------------------------------------------
# 4. Plotten
# --------------------------------------------

plt.figure()
plt.xlabel("Displacement (mm)")
plt.ylabel("Force (N)")

plt.errorbar(new_disp, new_force, yerr=0.003,
             fmt='o', markersize=2, label="Data")

plt.plot(new_disp, fit_result.best_fit, 'r-', linewidth=2,
         label="Exponentiële fit")

plt.legend()
plt.show()
