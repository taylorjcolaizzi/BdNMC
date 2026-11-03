# BdNMC

BdNMC is a Monte Carlo event generator for simulating dark matter production and detector interactions in fixed-target and beam-dump experiments.

The code generates dark matter fluxes and detector event predictions using user-supplied physics and detector parameters. Detailed theoretical background and implementation details can be found in the appendix of Dark Matter Production through Proton Bremsstrahlung and Other Processes. 【1-7bf4e6】

---

## Features

- Dark matter production through multiple production channels
- Dark photon and baryonic dark matter models
- Monte Carlo event generation
- Detector acceptance and scattering calculations
- Configurable detector geometries and materials
- Flexible beam and target configurations
- Multiple output modes for event generation and analysis

---

## Installation

### Clone Repository

```bash
git clone --recursive https://github.com/taylorjcolaizzi/BdNMC.git
cd BdNMC
```

If the repository has already been cloned:

```bash
git submodule update --init --recursive
```

### Requirements

- Linux or macOS
- Bash
- GNU Make
- C++ compiler
- Git

---

## Building

The provided launcher script automatically compiles the project before execution.

To build manually:

```bash
cd build
make main
```

The executable is produced as:

```text
build/main
```

---

## Running Simulations

Run with a parameter card:

```bash
./bin/BDNMC parameter.dat
```

If no parameter file is supplied:

```bash
./bin/BDNMC
```

the default `parameter.dat` located in the repository root is used.

Multiple parameter cards may be run sequentially:

```bash
./bin/BDNMC run1.dat run2.dat run3.dat
```

---

## Example Output

For the supplied example parameter card, the simulation should print a result similar to:

```text
Predicted number of signal events = 284.31
Predicted number of signal events from channel 1 pi0_decay = 284.31
```

Small statistical fluctuations are expected due to Monte Carlo sampling.

---

# Parameter Card

Simulation settings are controlled through a plain-text parameter card.

Lines beginning with `#` are ignored.

Units:

- Masses are specified in GeV
- Distances are specified in meters

---

## Random Number Generation

```text
seed 114234
```

Sets the random number generator seed.

If omitted, the seed is generated automatically.

---

## Run Naming

```text
run 14506
```

Optional run identifier.

If not specified, a name is generated automatically.

---

## Physics Model

```text
model Dark_Photon
```

Currently supported models include:

- `Dark_Photon`
- Baryonic dark matter variants

---

## Model Parameters

Example:

```text
epsilon 1e-3
dark_matter_mass 0.005
dark_photon_mass 0.1
alpha_D 0.1
```

### Parameters

| Parameter | Description |
|------------|------------|
| `epsilon` | Kinetic mixing parameter |
| `dark_matter_mass` | Dark matter mass (GeV) |
| `dark_photon_mass` | Dark photon mediator mass (GeV) |
| `alpha_D` | Dark-sector coupling |

---

## Run Parameters

```text
POT 2e20
pi0_per_POT 0.9
samplesize 1000
```

| Parameter | Description |
|------------|------------|
| `POT` | Protons on target |
| `pi0_per_POT` | Average π⁰ production rate per POT |
| `samplesize` | Number of Monte Carlo samples |

Optional:

```text
meson_per_pi0 0.0333
```

---

## Burn-In Configuration

```text
burn_max 1000
burn_timeout 20000
```

The simulation generates dark matter trajectories that intersect the detector and discards events until the burn-in requirement is satisfied.

If the number of attempts exceeds:

```text
burn_max × burn_timeout
```

the burn-in process terminates early and a warning is issued.

---

## Beam Configuration

```text
beam_energy 8.9
```

Beam energy in GeV.

---

# Production Channels

A production channel specifies how dark matter is generated.

Example:

```text
production_channel pi0_decay
```

Supported channels include:

```text
pi0_decay
eta_decay
V_decay
phi_decay
pi0_decay_baryonic
eta_decay_baryonic
V_decay_baryonic
phi_decay_baryonic
piminus_capture
```

---

## Production Distributions

Example:

```text
production_distribution pi0_sanfordwang
```

Supported distributions include:

- `pi0_sanfordwang`
- `k0_sanfordwang`
- `particle_list`
- `proton_brem`

---

### Sanford-Wang Parameterization

Custom fit parameters may be supplied:

```text
sanfordwang_file sanfordwang_parameters.dat
```

---

### Particle List Input

Instead of generating mesons internally, users may provide four-vectors:

```text
production_distribution particle_list
particle_list_file particle_list.dat
```

Format:

```text
px py pz E
```

To specify production positions and times:

```text
particle_list_position true
```

Format:

```text
px py pz E x y z t
```

---

### Proton Bremsstrahlung

Example:

```text
production_channel V_decay
production_distribution proton_brem

ptmax 0.2
zmin 0.3
zmax 0.7
```

These parameters control phase-space generation for proton bremsstrahlung production.

---

# Signal Channels

Signal channels determine how dark matter interacts inside the detector.

Example:

```text
signal_channel NCE_electron
```

Supported channels:

```text
NCE_nucleon
NCE_electron
Pion_Inelastic
Inelastic_Delta_to_Gamma
NCE_nucleon_baryonic
```

---

## Coherent Scattering

Enable coherent scattering:

```text
coherent true
```

Default behavior is incoherent scattering.

---

# Output Configuration

Output event file:

```text
output_file Events/events.dat
```

Summary file:

```text
summary_file Events/summary.dat
```

---

## Output Modes

### Comprehensive

```text
output_mode comprehensive
```

Writes complete event information.

### Summary

```text
output_mode summary
```

Writes only run summaries.

### Particle List

```text
output_mode particle_list
```

Generates particle-list files for reuse as production inputs.

---

# Scattering Energy Cuts

Example:

```text
max_scatter_energy 0.9
min_scatter_energy 0.035
```

These cuts are applied to the outgoing nucleon or electron kinetic energy.

Defaults:

```text
min = 0 GeV
max = 1e9 GeV
```

---

# Detector Configuration

Example detector:

```text
detector sphere

x-position 0.0
y-position -1.9
z-position 491.0

radius 5.0
```

Current detector geometry:

```text
sphere
```

---

# Detector Materials

Materials are specified individually.

Example:

```text
material Carbon

number_density 3.63471e22
proton_number 6
neutron_number 6
electron_number 6
mass 11.2593
```

### Parameters

| Parameter | Description |
|------------|------------|
| `number_density` | Number density of targets |
| `proton_number` | Number of protons |
| `neutron_number` | Number of neutrons |
| `electron_number` | Number of electrons |
| `mass` | Nuclear mass (GeV) |

Multiple materials may be declared and are automatically combined within the detector volume.

Example:

```text
material Carbon
...

material Hydrogen
...
```

---

# Output Files

Typical outputs include:

```text
Events/events.dat
Events/summary.dat
```

The summary file records:

```text
channel_name
mediator_mass
dark_matter_mass
num_events
epsilon
alpha_D
scattering_channel
```

---

# Citation

If you use BdNMC in published work, please cite:

```bibtex
@article{deNiverville:2016rqh,
  title={Dark Matter Production through Proton Bremsstrahlung},
  author={de Niverville et al.},
  eprint={1609.01770},
  archivePrefix={arXiv},
  primaryClass={hep-ph}
}
```

and any additional papers describing the specific production or scattering models used in your analysis.

---

# Troubleshooting

### Missing Submodule

```bash
git submodule update --init --recursive
```

### Build Errors

```bash
cd build
make clean
make main
```

### No Events Generated

Check:

- Production channel configuration
- Detector position and geometry
- Output paths
- Energy cuts
- Physics model parameters

---

# License

Add license information here.