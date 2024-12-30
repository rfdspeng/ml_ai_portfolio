# <u>Introduction to environments</u>
Environments hold a specific collection of packages. It's recommended to have different environments for different projects. NEVER WORK IN THE BASE ENVIRONMENT.

By default, environments are created in your installation location (on Linux, you can query the location via `echo $CONDA_PREFIX`). The base environment is in your installation folder, and all other environments (also known as virtual environments) are under `installation_folder\envs\env_name`. Running `conda env list` will show you all of your environments and where they are located in your file system.

However, it's generally preferred to create the environment for your project in your project folder so that your project is completely self-contained. This also has the advantage that you do not need to create unique names for each environment since these aren't created in the installation folder.

If you can't find a package, you can check anaconda.org, conda-forge channel.

# <u>conda CLI</u>

General:
* `conda --version`
* `conda update conda`: update conda
* `conda info`

Creating, activating, deleting, and versioning environments:
* `conda env list` or `conda info --envs`: list all of the environments created in your installation folder and see which virtual environment is active (marked with *)
* `conda create -n env_name` or `conda create --name env_name`: create a new environment named `env_name`
* `conda create -n env_name pkg1 pkg2 pkg3`: create a new environment and install `pkg1`, `pkg2`, `pkg3`
* `conda create -n env_name python=3.9`: create a new environment with Python v3.9
* `conda create --name new_env_name --clone current_env_name`: create a new environment that is a copy of the current environment
* `conda create --no-default-packages -n env_name`: create a new environment without installing default packages (default packages are defined in `~/.condarc`)
* `conda activate env_name`: switch to `env_name`
* `conda deactivate`: revert to base environment
* `conda remove --name env_name --all -y`: delete `env_name`
* `conda list --revisions`: list the history of each change to the current environment
* `conda install --revision=rev_num` or `conda install --rev rev_num`: restore the current environment back to revision `rev_num`

Specifying a location for an environment:
* `conda create --prefix ./envs`: create an environment in `current_dir/envs`
* `conda activate ./envs`: activate the environment in `current_dir/envs`
* `conda create --prefix ./envs --clone env_to_clone`: clone environment from installation directory

Exporting and loading environment files:
* `conda env export > env.yml`: export current environment (platform + package specific). Not cross-platform compatible.
* `conda env export --from-history > env.yml`: create cross-platform compatible environment file from current environment. This only includes packages you explicitly installed, excluding additional packages that were installed to solve dependencies. This will not include pip-installed packages; you will need to manage that separately. Remember to remove `prefix: path/to/env_folder` from the bottom of the file.
* `conda env create --name env_name --file env.yml`: create a new environment from environment file

Installing, updating, and removing packages:
* `conda list`: see installed packages in current environment
* `conda list pkg`: check `pkg` version
* `conda search pkg`: search for available packages in your channels
* `conda install pkg1 pkg2 pkg3`: install packages in current environment
* `conda install pkg=v`: install (can also upgrade or downgrade) `pkg` to version `v`, e.g. `conda install numpy=1.26.4`
* `conda install -c conda-forge condastats`: install package (`condastats` in this example) from a specific channel (`conda-forge` in this example) from anaconda.org
* `conda update pkg1 pkg2 pkg3`: update packages
* `conda remove pkg1 pkg2 pkg`: uninstall packages in current environment
* `conda install -n env_name pkg`: install package in `env_name`
* `conda update -n env_name pkg`: update package in `env_name`

# <u>Activating an environment vs. `conda run`</u>

When you activate an environment `myenv`, you're telling Conda to prepare the shell environment to use the packages and binaries installed in `myenv`. This means
1. Prepending the location of `myenv` to `PATH` so it takes precedence over the base environment
2. Changing the environment variables `CONDA_PREFIX` and `CONDA_DEFAULT_ENV`

`conda activate` activates the environment for interactive use. `conda run` runs a command in the specified environment without modifying the current shell.

|Feature|`conda activate`|`conda run`|
|-------|----------------|-----------|
|Purpose|Activates the environment for interactive use|Runs a command in the specified environment without modifying the current shell|
|Usage|Requires a shell session (Bash)|Does not require an activated environment; works with commands directly|
|Modifies environment|Changes the shell's environment (e.g. `PATH`)|Executes the command in a subprocess that does not modify the current shell|
|Docker compatibility|Not ideal for Docker since the container needs to run a shell|Ideal for Docker since it doesn't depend on activating an environment in a shell|
|Example|`conda activate myenv && python script.py`|`conda run -n myenv python script.py`|

