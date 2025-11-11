import numpy as np

def Fcr(d, L, E, K=1):
    """Euler critical load for a circular rod"""
    I = np.pi * d**4 / 64
    return np.pi**2 * E * I / (K * L)**2

def Fcr_error(d, L, E, delta_d, delta_L, delta_E, K=1, delta_K=0):
    """Error propagation for Euler load"""
    I = np.pi * d**4 / 64
    F = np.pi**2 * E * I / (K * L)**2

    # partial derivatives
    dF_dd = np.pi**3 * E * d**3 / (16 * (K*L)**2)
    dF_dL = -2 * F / L
    dF_dE = F / E
    dF_dK = -2 * F / K

    # total error
    delta_F = np.sqrt( (dF_dd*delta_d)**2 + (dF_dL*delta_L)**2 +
                       (dF_dE*delta_E)**2 + (dF_dK*delta_K)**2 )
    return delta_F

# Example parameters
d = 0.002      # 2 mm
L = 0.03       # 3 cm
E = 4e9        # 4 GPa
K = 1
delta_d = 0.0001   # 0.1 mm uncertainty
delta_L = 0.001    # 1 mm uncertainty
delta_E = 0.5e9    # 0.5 GPa uncertainty

# Example: Square column, factor 4
factor = 4

F = factor * Fcr(d,L,E,K)
deltaF = factor * Fcr_error(d,L,E,delta_d,delta_L,delta_E,K,0)

print(f"F_max = {F:.2f} N ± {deltaF:.2f} N")
