#!/usr/bin/env python3
"""
Polhamus Lift-Coefficient Calculator
====================================
Implements the Polhamus lift-curve slope formula (semi-empirical, subsonic)
to compute the wing lift coefficient CL at a user-specified angle of attack.

Reference:
  "Polhamus Formula" as provided – estimates c_L_alpha for swept wings
  with AR between 3 and 7, Lambda_LE < 30-32°, M < M_crit.

Restrictions:
  - The formula is derived from linear subsonic theory. It is valid only
    for Mach numbers well below 1.0 (typically M < 0.8).  At M = 1 the
    denominator becomes zero, and the physics changes completely.
    For safety, this script rejects M >= 0.9.

Usage:
  Run in terminal, answer the prompts.
  All angles in degrees.
  Assumes a rectangular wing (for area, AR, and sweep inputs).
"""

import math

def main():
    print("=== Polhamus Lift-Curve Slope & CL Calculator ===\n")

    # ----- Geometry inputs -----
    span_mm = float(input("Wing span (mm): "))
    chord_mm = float(input("Wing chord (mm): "))
    span = span_mm / 1000.0   # m
    chord = chord_mm / 1000.0 # m
    S = span * chord           # wing area (m^2)
    AR = span**2 / S

    print(f"-> Wing area = {S:.4f} m²,  Aspect Ratio = {AR:.3f}")

    # ----- Sweep angles -----
    Lambda_LE_deg = float(input("Leading-edge sweep angle (deg): "))
    Lambda_05_deg = float(input("Half-chord sweep angle (deg): "))

    # ----- Mach number with guard -----
    M = float(input("Mach number (0 for low-speed RC): "))
    if M >= 0.9:
        print("\nERROR: Polhamus formula is only valid for subsonic Mach numbers.")
        print("       The denominator (1 - M²) becomes zero or negative at M ≥ 1.")
        print("       Please enter a Mach number less than 0.9 (typical RC: 0).")
        return  # exit the script

    # ----- Polhamus k factor -----
    if AR < 4:
        k = 1.0 + AR * (1.87 - 0.000233 * Lambda_LE_deg) / 100.0
    else:
        k = 1.0 + ((8.2 - 2.3 * Lambda_LE_deg) - AR * (0.22 - 0.153 * Lambda_LE_deg)) / 100.0

    # ----- Lift-curve slope (per radian) -----
    Lambda_05_rad = math.radians(Lambda_05_deg)

    term1 = (AR**2 * (1 - M**2)) / (k**2)
    term2 = 1.0 + (math.tan(Lambda_05_rad)**2) / (1 - M**2)
    sqrt_term = math.sqrt(term1 * term2 + 4.0)

    CL_alpha_rad = (2.0 * math.pi * AR) / sqrt_term   # per radian
    CL_alpha_deg = CL_alpha_rad / (180.0 / math.pi)   # per degree

    print(f"\n--- Results ---")
    print(f"Polhamus k factor = {k:.4f}")
    print(f"Lift-curve slope (c_L_alpha):")
    print(f"  {CL_alpha_rad:.4f} per radian")
    print(f"  {CL_alpha_deg:.4f} per degree")

    # ----- Lift coefficient at a given AoA -----
    alpha_0_deg = float(input("\nZero-lift angle of attack (deg, e.g. -3.5 for Clark Y): "))
    alpha_deg = float(input("Angle of attack to evaluate (deg): "))

    CL = CL_alpha_deg * (alpha_deg - alpha_0_deg)

    print(f"\nCoefficient of Lift CL at α = {alpha_deg}°:")
    print(f"  CL = {CL:.4f}")
    print(f"  (Effective α = {alpha_deg - alpha_0_deg:.1f}° above zero-lift)")

if __name__ == "__main__":
    main()