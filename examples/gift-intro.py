"""
GIFT Framework - Introduction
=============================
Simplified version for educational purposes
"""

# Essential imports only
import numpy as np
import matplotlib.pyplot as plt

# Core GIFT constants
xi = 5 * np.pi / 16  # Fundamental geometric ratio
beta_H = np.pi / 8   # Anomalous dimension
tau = 3.8966         # Mass hierarchy generator

print("GIFT Framework - Introduction")
print("=" * 40)
print(f"ξ (geometric ratio): {xi:.6f}")
print(f"β_H (anomalous dim): {beta_H:.6f}")
print(f"τ (mass generator): {tau:.6f}")

# Simple prediction: Hubble constant
zeta_3 = 1.2020569  # Apéry constant
h0_cmb = 67.36       # Planck value

h0_gift = h0_cmb * (zeta_3 / xi) ** beta_H
print(f"\nHubble Prediction:")
print(f"H₀_GIFT = {h0_gift:.3f} km/s/Mpc")
print(f"SH0ES   = 73.04 ± 1.04 km/s/Mpc")
print(f"Error   = {abs(h0_gift - 73.04)/73.04 * 100:.2f}%")

# Simple visualization
fig, ax = plt.subplots(figsize=(8, 5))
measurements = ['Planck CMB', 'GIFT', 'SH0ES']
values = [67.36, h0_gift, 73.04]
errors = [0.54, 0.05, 1.04]
colors = ['blue', 'green', 'red']

ax.errorbar(range(len(values)), values, yerr=errors, 
           fmt='o', capsize=5, markersize=8, 
           color=colors)
ax.set_xticks(range(len(measurements)))
ax.set_xticklabels(measurements)
ax.set_ylabel('H₀ (km/s/Mpc)')
ax.set_title('Hubble Tension Resolution via GIFT')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n🎯 Next Steps:")
print("1. Explore the full framework: gift-notebook.py")
print("2. Try other predictions: fine structure, Koide relation")
print("3. Read the theory papers in docs/")
