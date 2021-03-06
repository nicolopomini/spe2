# SPE 2
### Simulating Aloha-like protocols in Python
Second assignment of 'Simulation and Performance Evaluation' course

The original simulator has been modified, to implement the _Trivial Carrier Sensing_ and the _Simple Carrier Sensing_ protocols, and the _Realistic Propagation_. Three new optional flags have been added to the main file of the simulator:
- `-p` (or `--protocol`) to set the protocol. Use either `aloha`, `trivial` or `simple` to set one of the two protocols;
- `-R` (or `--realistic_propagation`) to use the probabilistic reception model.

In case _Simple Carrier Sensing_ protocol is used, another mandatory flag must be set:
- `-P` (or `--persistence`), to set the persistence of the protocol. Use a floating point number between 0 and 1.

It was preferred to add two flags instead of putting these new parameters inside the `config.json` file, because in this way is easier to automatically run the simulator with different settings. In fact, the whole process of launching the simulation and analysing the results is executed by a script -- see later for details.

For example, to launch a simulation with _Simple Carrier Sensing_ with persistence _p = 0.45_ and the realistic reception model, run `python simulator/main.py -c config.json -s simulation -r 0 -p simple -P 0.45 -R`.

In addition to that, a new python module, called _analysis_, has been added. It reads the outputs of the simulations and it prepares the plots.
The plots are both at node level - plotting the throughput, the collision rate and the drop rate of each node - and aggregated, considering all the nodes together.
This module is expecting to find the raw files of the outputs of the simulations divided by type of simulations:
1. Aloha + original reception
2. Aloha + realistic reception
3. Trivial carrier sensing + original reception
4. Trivial carrier sensing + realistic reception
5. Simple carrier sensing (with persistence = 0.75, 0.5, 0.25, 0) + original reception
5. Simple carrier sensing (with persistence = 0.75, 0.5, 0.25, 0) + realistic reception

Indeed, with the original reception model only Aloha, Trivial Carrier Sensing and Simple Carrier Sensing with p = 0 are simulated. With the probabilistic reception model, all the configurations are simulated.

Another parameter is added to the `config.json` file, called `skip_sensing` and accepting a boolean value. If set to true, it allows a node with a sensing protocol to skip the sensing phase when coming from the IDLE state - see the report for more details about this behaviour.

This module uses `matplotlib` and `Pandas` for its operations. To install them, just run `pip install -r requirements.txt`. The project was developed and tested with Python 3.6 or higher.

To reproduce the results, the script `run_simulations.sh` runs all the simulations and produces the plots. Running `sh run_simulations.sh` is possible to obtain the results in the report, manually varying the `skip_sensing` value to change the behaviour of the nodes.
To clean the results, removing the plots and the raw data, is possible to use the `cleaner.sh` script. Just run `sh cleaner.sh`.

The analysis script need to export the simulator path in the Pythonpath. To launch it, do the following:
```
export PYTHONPATH=$PYTHONPATH:./simulator/
python analysis/main.py
```
