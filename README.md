# Protein HMM

##Sample Analysis Vignette - Exosome
Open and follow the instruction in 'TPP_HMM_Analysis_Vignette.Rmd' on the main branch. The Vignette will walk through a full analysis, including EM optimization, of the exosome protein complex. The initial input (as shown in the vignette) is "data/becher_fullCycle_reformat.csv" and the final output we recieved is 'data/exosome_hmm_result.csv'

## Simulator
### Requirements 
Since we did not use python environments like venv or conda, there are 2 requirements files in the simulator directory. `requirements-full.txt` lists all the python packages installed globally on my (Darvesh's) machine. `requirements-min.txt` lists only the packages imported in `simulator.py` and `Development.ipynb`. *Please use requirements-min.txt if you're unsure*. This code was tested on Python 3.9.7 and 3.7.9 but the code should work for Python 3.x.x. Please reach out if there are version-specific issues. The simulator is quite light and runs within seconds on a Intel dual-core Macbook Pro from 2017. Your mileage may vary. This has not been tested on Apple Silicon or Windows (10 or 11). The safest, most reliable way to test this would be inside a conda environment or virtual environment.

### Data
Although some data was used for debugging and exploratory purposes the simulator itself does not use sample data. All relevant data for exploratory purposes and debugging can be found in the `protein-hmm/data` directory. Debugging takes place in `debugging.py` and exploration takes place n `Development.ipynb`.

### Compilation 
We use python for the simulator so no compilation is necessary unless you would like to install the requirements from source and potentially compile some C libraries on your own. This is not recommended, but not hindered.

### Validation
To check and see if everything runs fine, you can run the `test.py` from within the `simulator/` directory (i.e. `cd` into the directory). To run the tests simply run 

```
python3 test.py
```

Running this should also highlight any missing dependencies or incompatible versions which may not have been captured during initial installation. You can also generate some figures from the paper by running (again from within the `simulator/` directory).

```
python3 generate_figures.py
```
