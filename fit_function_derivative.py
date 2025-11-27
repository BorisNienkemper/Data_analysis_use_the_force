from lmfit import models
import matplotlib.pyplot as plt
import csv

mod_linear = models.LinearModel()

# --- Load data (same as your original) ---
time_list = []
displacement_list = []
force_list = []
with open("tetrahede_eerste_meting.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        time_list.append(float(row[0]))
        displacement_list.append(float(row[1]))
        force_list.append(float(row[2]) / -1000.0)

N = len(force_list)

deriv = []
for i in range(N-1):
    deriv.append(force_list[i+1] - force_list[i])

# --- 3-point smoothing of derivative (neighbor average) ---
smoothed = []
for i in range(len(deriv)):
    s = deriv[i]
    count = 1
    if i > 0:
        s += deriv[i-1]; count += 1
    if i < len(deriv)-1:
        s += deriv[i+1]; count += 1
    smoothed.append(s / count)

# --- mask of where derivative > 0 (increasing) ---
mask = [d > 0 for d in smoothed]   # length N-1

# --- find the longest contiguous True run in mask ---
best_start = best_end = -1
cur_start = None
for i, m in enumerate(mask):
    if m:
        if cur_start is None:
            cur_start = i
        # continue
    else:
        if cur_start is not None:
            # closed run cur_start .. i-1
            if best_start == -1 or (i-1 - cur_start) > (best_end - best_start):
                best_start, best_end = cur_start, i-1
            cur_start = None

# if mask ends with a True run, close it
if cur_start is not None:
    i = len(mask)
    if best_start == -1 or (i-1 - cur_start) > (best_end - best_start):
        best_start, best_end = cur_start, i-1

# require at least 2 derivative-trues -> maps to at least 3 data points
min_deriv_run = 2
if best_start == -1 or (best_end - best_start + 1) < min_deriv_run:
    print("No clear increasing region found; using full data for fit.")
    sel_start, sel_end = 0, N-1
else:
    # map derivative indices (a..b) to data indices (a .. b+1)
    sel_start = best_start
    sel_end = best_end + 1
    print(f"Detected increasing region in data indices: {sel_start} → {sel_end}")

# --- slice selected region ---
new_displacement_list = displacement_list[sel_start:sel_end+1]
new_force_list = force_list[sel_start:sel_end+1]

# --- fit and plot as before ---
y_err = [0.003] * len(new_force_list)
fit_result = mod_linear.fit(new_force_list, x=new_displacement_list, weights=[1.0 / e for e in y_err])

print(fit_result.fit_report())

plt.figure(figsize=(8,4))
plt.plot(new_displacement_list, new_force_list, label="selected increasing region", linewidth=2)
plt.plot(new_displacement_list, fit_result.best_fit, 'r-', label="linear fit")
plt.xlabel("Displacement (mm)")
plt.ylabel("Force (N)")
plt.legend()
plt.show()
