def calibration_factor():
    weight = 1.19/1000 # kg
    F_measured = 11.27/1000 #Newton 
    F_applied = weight * 9.81
    cb_factor = F_applied / F_measured
    print(cb_factor)
calibration_factor()