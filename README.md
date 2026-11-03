# BdNMC

BdNMC is a Monte Carlo event generator for simulating dark matter production and detector interactions in fixed-target and beam-dump experiments.

The code generates dark matter fluxes and detector event predictions using user-supplied physics and detector parameters. Detailed theoretical background, physics implementation, and validation studies are described in the appendix of Dark Matter Production through Proton Bremsstrahlung and Other Processes. 【1-83b52f】

---

## Features

- Dark matter production through multiple beam-dump production channels
- Monte Carlo event generation
- Detector acceptance calculations
- Configurable experimental geometries
- User-defined model parameters through input files
- Automated build-and-run workflow

---

## Repository Structure

```text
BdNMC/
├── bin/
│   └── BDNMC          # Build and execution script
├── build/             # Build directory
├── Events/            # Generated event output
├── parameter.dat      # Example parameter file
└── BdNMC_LANL/        # Required submodule
```

---

## Requirements

### Software

- Linux or macOS
- Bash
- GNU Make
- C++ compiler
- Git

### Required Submodule

BdNMC depends on the `BdNMC_LANL` submodule.

Clone the repository with submodules:

```bash
git clone --recursive https://github.com/taylorjcolaizzi/BdNMC.git
```

or initialize them after cloning:

```bash
git submodule update --init --recursive
```

---

## Building

The project is built automatically when executed through the provided launcher script.

To build manually:

```bash
cd build
make main
```

The executable will be generated as:

```text
build/main
```

---

## Running Simulations

From the repository root:

```bash
./bin/BDNMC parameter.dat
```

where `parameter.dat` is a valid input parameter file.

### Default Behavior

If no parameter file is specified:

```bash
./bin/BDNMC
```

the code automatically uses:

```text
parameter.dat
```

located in the repository root.

### Multiple Parameter Files

The launcher script accepts multiple parameter files:

```bash
./bin/BDNMC run1.dat run2.dat run3.dat
```

Each file is passed sequentially to the simulation executable.

---

## Output

Simulation output is written to the `Events/` directory.

If the directory does not already exist, it is automatically created by the launcher script.

```text
Events/
├── ...
```

The exact contents depend on the selected physics process and simulation configuration.

---

## Input Parameter Files

Simulation settings are controlled through a parameter file.

Typical parameters include:

- Dark matter mass
- Mediator mass
- Coupling constants
- Beam energy
- Detector geometry
- Production channels
- Event generation settings

See the sample:

```text
parameter.dat
```

for a complete example.

---

## Workflow

A typical workflow is:

1. Configure a parameter file.
2. Run the simulation.
3. Inspect generated files in `Events/`.
4. Analyze event yields and detector observables.

Example:

```bash
cp parameter.dat myrun.dat

# Edit parameters
nano myrun.dat

# Run simulation
./bin/BDNMC myrun.dat
```

---

## Documentation

Full physics and implementation documentation can be found in the appendix of:

Dark Matter Production through Proton Bremsstrahlung and Other Processes. 【1-83b52f】

ArXiv:

```text
https://arxiv.org/abs/1609.01770
```

---

## Citation

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

Please also cite any additional papers describing the specific production or detector models used in your analysis.

---

## Troubleshooting

### Missing Submodule

Error during compilation:

```text
BdNMC_LANL not found
```

Solution:

```bash
git submodule update --init --recursive
```

### Build Failure

Clean and rebuild:

```bash
cd build
make clean
make main
```

### No Events Produced

Verify:

- Parameter file path is correct.
- Physics parameters are valid.
- Detector geometry is properly configured.
- Output files are being written to `Events/`.

---

## License

Specify the repository license here.