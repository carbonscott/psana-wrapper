def wavelength_to_photon_energy(wavelength):
    h = 6.626070e-34  # J.m
    c = 2.99792458e8  # m/s
    joules_per_ev = 1.602176621e-19  # J/eV
    photon_energy = (h / joules_per_ev * c) / (wavelength * 1e-9)

    return photon_energy
