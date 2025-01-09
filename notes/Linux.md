# <u>Linux</u>

Install Ubuntu in VirtualBox: https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview

## <u>Basics</u>

First thing to run after installation:
* `sudo apt update && sudo apt upgrade -y`
* `sudo snap refresh`: Snap is a package management system. It allows you to install and manage SW packages that are containerized. Snap packages are automatically updated in the background, but you can run this command to update manually.

Other basic commands:
* `passwd`: change password



.bashrc: file in your home directory. A bash script that is executed every time you start up a new terminal/bash.
* Define environment variables here so they persist across sessions

sudo = "superuser do". Allows you to run the command following sudo with superuser/root privileges. Similar to "Run as administrator" in Windows.
apt = package manager
update = apt command to update all packages

sudo apt update
sudo apt upgrade (-y if you want to answer yes to all prompts)
sudo apt install package-name
sudo chmod a-w file-name: chmod means to change permissions. a means the change applies to all users. -w means to remove write permissions - no one can write to this file.

ls -a: list all files, including hidden files and folders
ls -al: list all files, hidden files and folders, and properties like permissions
ls -l file-name: list file-name, including properties like permissions
touch file-name: create file-name
cp file-name new-file-name: make a copy of file-name and name it new-file-name
mv file-name new-file-name: rename file-name to new-file-name
mv file-name folder: move file-name to folder
mkdir -p dir-name: create directory dir-name. -p means to create parent folders as needed.
mkdir -p dir-name/{subdir1, subdir2, subdir3}: create multiple subdirectories under dir-name
export env_var=value: create an environment variable env_var set to value, e.g. env_var could be DATA_PATH and value could be path/to/data
echo $env_var: print the value of env_var
cd $env_var: if env_var is a path, then change directory to path

chmod: typically followed by an octal (base 8) number that specifies read/write/execute permissions
* 3 digits corresponding to owner (user, or u), group (g), others (o): p2, p1, p0 = user, group, others
* Each digit is an octal number (3 bits). Each bit toggles read/write/execute: b2, b1, b0 = read, write, execute
* Examples
	* 777 = full access for everyone
	* 755 = owner has full access, otherwise read/execute
	* 700 = owner has full access, otherwise no access
	* 644 = owner has read/write, otherwise read-only
	* 600 = owner has read/write, otherwise no access
	* 444 = read-only
	* 555 = read/execute
* Format: chmod 600 file-name
* Alternatively, instead of using an octal number, you can execute chmod using this kind of format: chmod (u/g/o)(+/-)(r/w/x) to specify adding (+) or removing (-) access (r/w/x) from user (u), group (g), or others (o).


/etc/ - system directory containing configuration files for the system and installed software

Install OpenSSH server on virtual machine running Ubuntu: https://ubuntu.com/server/docs/openssh-server
* sudo sshd -t -f /etc/ssh/sshd_config
	* sshd is the OpenSSH daemon (server) program. Used to test configurations or start the SSH server.
	* -t: tells sshd to test the configuration file for syntax errors without starting the SSH server
	* -f /etc/ssh/sshd_config: specifies the path to the configuration file
* sudo systemctl restart ssh
	* systemctl = command to interact with the systemd system and service manager that controls and manages services (aka "units") on Linux distros
	* restart: tells systemd to stop and start the service
	* ssh: refers to SSH service

nano
nano txt-file
Ctrl + O to save changes. Press Enter to confirm
Ctrl + X to exit.

# Shells and scripts

Resources:
* https://askubuntu.com/questions/1411833/what-goes-in-profile-and-bashrc
* https://medium.com/@linuxadminhacks/what-are-interactive-and-non-interactive-shells-in-linux-5f25ce19e537#:~:text=An%20interactive%20shell%20in%20Linux,%60bash%60%20in%20the%20terminal.

A shell is a program that allows the user to interact with the OS by typing commands, which the shell interprets and executes. Bash (`bash`) is the most popular Unix shell.

A script is a file of shell commands that can be executed in a batch, e.g. `bash myscript.sh` or `source myscript.sh`. `bash` runs the script in a new shell (subshell), while `source` runs the script in the current shell. Anything executed using `bash` will not carry over into the current shell.

Shells and scripts can be interactive or non-interactive. 

An **interactive shell** takes terminal commands from the user and returns the output to the user, enables job control by default, and reads startup files. An interactive script requires input from the user, which means they can't be run in the background.

Quick note on job control: this is managing background and foreground processes with `Ctrl+Z`, `fg`, and `bg`.

Startup files are executed when the interactive shell starts up. For interactive shells, it's common practice to declare environment variables in startup files.
* `~/.bashrc` is executed by non-login shells
* `~/.profile` (or sometimes `~/.bash_profile` for `bash`) is executed by login shells. For consistent behavior, `~/.profile` usually sources `~/.bashrc`.
* `~/etc/profile.d` is a folder containing scripts that are executed by login shells. It's used for system-wide configurations like setting environment variables or adding paths to `PATH`. These scripts are sourced by `/etc/profile`, a script that is executed before `~/.profile`.

For best practice, use `/etc/profile.d` for global settings and `~/.bashrc` and `~/.profile` for user-specific settings.

Here's an example of how to append a folder to `PATH` system-wide:
```bash
echo 'export PATH=$PATH:/custom/global/path' > /etc/profile.d/custom_path.sh
chmod +x /etc/profile.d/custom_path.sh
```

Login shells are typically started by logging into a system (e.g. via SSH or at a console), but you can also start a login shell by typing `bash -l` in a terminal. You can start a non-login shell by typing `bash` in a terminal.

A **non-interactive shell** executes commands without requiring any user interaction, so they're typically used for running scripts in the background. Non-interactive shells do not execute startup files, so you'll typically need to specify full paths for executables since `PATH` declarations in startup files will not be executed. However, you can explicitly source startup files in your script, e.g. `source ~/.bashrc`, `source ~/.profile`, or `source ~/etc/profile`.

# Regular files vs. special files

Regular files are what we typically think of as files, e.g. .txt, .md, .jpg, .png, .exe, .sh, etc.

Special files can be directories, character devices, block devices, named pipes or FIFOs, or sockets.

In shell scripting, `-f` (used within conditional brackets) checks for regular files. `-d` checks for directories, `-c` checks for character devices.

# Variables

## Local vs. environment variables

Variables defined at the command line are called **local** or **shell** variables. They exist only in the shell session in which they are defined, and they aren't accessible to child processes (i.e. shell scripts or commands launched from the shell) unless they're exported.

**Environment** variables, also known as **exported** variables, are accessible by child processes. Environment variables can only be scalars (numbers or strings), not arrays.

Creating an environment variable can be done in one line: `export PATHNAME="path/to/folder"`

If you need to declare attributes, it can be done in two lines:
```bash
declare -r PATHNAME="path/to/folder"
export PATHNAME
```

You can instantiate persistent environment variables in `~/.bashrc`: simply add a line at the bottom `export MYVAR=VALUE`.

## Declaring variables

See here for more info: https://unix.stackexchange.com/questions/510220/what-is-declare-in-bash

The `declare` command is used to set variable values and attributes (if needed). Most of the time, an implicit declaration is good enough, e.g. `NUM=5`. However, sometimes, we want to specify attributes.

Common declarations:
* `declare -i INT=15`: create `INT`, specify that it is an integer, and set its value to 15
* `declare -a IND_ARRAY`: create an indexed array
* `declare -A ASSOC_ARRAY`: create an associative array, which is like a dictionary
* `declare -r READONLY_VAR`: create a read-only variable

## Querying variables

`declare -p VAR_NAME`: print the variable's type, value, and attributes  
`declare -p`: print all variables  
`declare -x`: print all environment variables (exported variables)  
`declare -a`: print all indexed arrays
`declare -A`: print all associative arrays
`set`: print all shell variables and functions

## Clearing variables

`unset VAR1 VAR2 VAR3` to remove variables.

## Strings

https://www.geeksforgeeks.org/string-manipulation-in-shell-scripting/

## Indexed arrays

## Associative arrays

Associative arrays are like Python dictionaries - they store key-value pairs. 

```bash
# Declare an associative array
declare -A species_count

# Add key-value pairs to the array
species_count["Iris-setosa"]=10
species_count["Iris-versicolor"]=15
species_count["Iris-virginica"]=12

# Access elements by key
echo "Count for Iris-setosa: ${species_count["Iris-setosa"]}"
echo "Count for Iris-versicolor: ${species_count["Iris-versicolor"]}"

# Checking if a key exists
if [[ -v species_count["Iris-setosa"] ]]; then
    echo "Iris-setosa exists in the array."
fi

# Deleting an element by key
unset species_count["Iris-setosa"]

# Getting the length of the array
echo "Number of species: ${#species_count[@]}"
```

To loop over key-value pairs, use
```bash
# Looping over key-value pairs
for species in "${!species_count[@]}"; do
    echo "$species: ${species_count[$species]}"
done
```
`[@]` means all elements. When used with an array, like `${species_count[@]}`, it means to get all the array values. Adding `!`, `${!species_count[@]}` means to get all the keys instead.  
In the loop, `species` is a variable that loops through the keys.

# Functions

```bash
my_function() { echo "Hello from my_function"; }
type my_function  # Output: my_function is a function
```

# <u>Control flow</u>

## <u>`if`</u>

```bash
if [ condition 1 ]; then
	do 1
elif [ condition 2 ]; then
	do 2
else
	do other
fi
```

In Bash, `[ ... ]`, which is called a test condition, returns 0 for True and 1 for False.

### <u>Example conditions</u>

* `[ $? -eq 0 ]`: since `$?` holds the exit status of the previous command and `-eq` is a binary operator used for numeric comparison that means *equal to*, this checks if the exit status of the previous command is 0, indicating success.
	* Alternatively, you can also use the command itself: `if some_command; then`. The `if` statement itself will interpret the command's success or failure.
* `[ -v VAR_NAME ]`: checks if the variable is set
* `[ -v ASSOC_ARRAY_NAME[KEY] ]`: checks if the element in the associative array indexed by `KEY` is set
* `[ -f "$FILE_NAME" ]`: checks if the file name in FILE_NAME exists and is a regular file
* `[ -d "$DIR_NAME" ]`: checks if the directory name in DIR_NAME exists

### <u>`[ ... ]` vs. `[[ ... ]]`</u>

Both `[ ... ]` and `[[ ... ]]` are used to perform tests. These are the key differences:  
* `[ ... ]` is supported in all POSIX-compliant shells. `[[ ... ]]` is specific to certain shells like `bash` and `ksh`.
* `[ ... ]` is limited to simple comparisons. `[[ ... ]]` supports regex (`=~`), logical operators (`&&`, `||`).
* You need to surround string variables in `[ ... ]` with quotes, `"$VAR"`, but not in `[[ ... ]]`.

# <u>Other commands and scripts</u>

## <u>`$`</u>

`$` is called the substitution operator, dereferencing operator, or expansion operator.

If you have a variable `VAR_NAME`, `$VAR_NAME` or `${VAR_NAME}` substitutes the value of `VAR_NAME` in place of `VAR_NAME`. If `VAR_NAME` stores a string, it's recommended to put double quotes around it: `"$VAR_NAME"`.

`${}` can also be used for parameter expansion and substring manipulation.
* `"${VAR_STR:-Default}"` outputs the value of `VAR_STR` if it exists; otherwise it outputs `Default`.
* `${#VAR_STR}` outputs the length of `VAR_STR` (the number of characters)
* `${VAR_STR:0:7}` extracts the first 7 characters of `VAR_STR`
* `"${FILE_NAME%.pdf}"` removes .pdf from `FILE_NAME`

If you have a command `command`, `$(command)` runs the `command` and replaces `command` with its output.
```bash
TODAY=$(date)	# runs date and stores the output of the call to TODAY
echo "Today is $TODAY"
```

Similarly, `$(( ... ))` performs the arithmetic operation inside `(( ... ))` and then substitutes the result, e.g. `echo $(( 5 * 10 ))` is equivalent to `echo 50`.

`$` also signifies special variables.
* `$0`: name of current script
* `$1-9`: position parameters, representing arguments passed to a script
* `$#`: the number of positional arguments
* `$@`: all arguments passed to the script as a list
* `$?`: the exit status of the last command (0 for success, non-zero for failure)
* `$$`: the process ID (PID) of the current shell
* `$!`: the PID of the last background command

## <u>`&`</u>

`&` at the end of a command will run the command in the background (leaving the terminal free), e.g. `sleep 60 &`.

`&&` acts as a logical AND between commands. It executes the second command if the first is successful (exit status 0), e.g. `mkdir new_folder && cd new_folder`.

In arithmetic and bitwise operations, `&` is a bitwise AND operator, e.g.
```bash
(( result = 5 & 3 ))
echo $result
```

## <u>`>`</u>

The redirection operator.

`echo some_expression > X`: redirect the output of echo to X, which can be  
* `output_file_name`: print to an output file (overwrites the file if it already exists)
* `>&1`: redirect to stdout
* `>&2`: redirects output to stderr. Useful for error messages to be separated from stdout.

## <u>`>>`</u>

`echo some_expression >> output_file_name`: appends the output of `echo` to the output file

## <u>`|` or pipe</u>

## <u>`(( ... ))`</u>

Command for evaluating arithmetic expressions. Inside `(( ... ))`, you can use arithmetic and logical operators like
* Basic math: `+`, `-`, `*`, `/`, `%`
* Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
* Bitwise operators: `&`, `|`, `^` (XOR), `<<` (bitwise shift), `>>`
* Increment/decrement: `++`, `--`

Inside `(( ... ))`, you can use variable names directly - no need to prepend `$` - and you can assign variables, e.g. `(( x = 5 ))`.

`(( ... ))` returns an exit status based on the evaluation, and it can be used in `if` statements, replacing `[]`.
```bash
(( 5 > 3 ))  # Evaluates to true (exit status 0)
echo $?      # Outputs: 0
(( 3 > 5 ))  # Evaluates to false (exit status 1)
echo $?      # Outputs: 1
```
```bash
x=10
if (( x > 5 )); then
    echo "x is greater than 5"
else
    echo "x is 5 or less"
fi
```

`(( ... ))` can be used as the counter in loops:
```bash
for (( i = 1; i <= 5; i++ )); do
    echo "Count: $i"
done
```

When used with `$`, like `$(( ... ))`, the expression inside `(( ... ))` is evaluated and then substituted, e.g. `result=$(( 5 * 10 ))` is equivalent to `result=50`, and `echo $(( 5 * 10 ))` is equivalent to `echo 50`.

## <u>awk</u>

awk is a scripting language/command-line tool for processing text files. One of its main applications is parsing and manipulating tabular data stored in text files (such as CSVs), but it can also be used for more general text processing.

You can write an awk script (good practice is to use a `.awk` extension) and call it in your shell like this:
`awk -f my_awk_script.awk file_to_process`

Alternatively, you can script directly in your terminal using the syntax:
`awk options instructions file_to_process`

The full syntax looks like:
`awk -F'delim_char' 'BEGIN {BEGIN instructions} filter {Per-line instructions} END {END instructions}' file_to_process`

`-F'delim_char'` is optional and specifies the delimiting character (e.g. `-F','` for CSVs). By default, awk splits on whitespace (spaces and tabs).

Within `{}`, you can write instructions in awk syntax - declaring and assigning variables, performing arithmetic, using control flow structures, printing, etc.
* `BEGIN` instructions are executed once, prior to processing any rows
* `filter` is an optional condition (e.g. `NR>1`): only rows that meet this condition will be processed
* The instructions after `filter` are applied to each row that meets the `filter` condition
* `END` instructions are executed once, after all rows have been processed

Example:
```bash
# For rows where the second column's ($2) value is > 30, print the first and second column's values
awk -F',' 'BEGIN {print "Processing CSV file..."} $2 > 30 {print $1, $2} END {print "Processing completed."}' file.csv
```

### <u>Built-in variables</u>

The column values in each row can be accessed via `$1` for the first column, `$2`, etc. `$0` gets the entire line.
```bash
awk '{sum+=$1} END {print sum}' file # find sum of values in column 1
awk '{print $0}' file # print each row
```

`NR` is the record (row) number, e.g. `NR`=1 is the first row in the file.
```bash
awk 'NR>1 {sum+=$1} END {print sum}' file # skip first row
```

`NF` is the number of fields (columns) in the current row.
```bash
awk '{print $NF}' file # print last field in each row
```

Logical operators: `&&`, `||`, `!`
Arithmetic operators:
Printing: https://www.gnu.org/software/gawk/manual/html_node/Print-Examples.html
Variable types:


3. Programming Constructs: 
(a) Format output lines 
(b) Arithmetic and string operations 
(c) Conditionals and loops 


`{}` are used to group commands executed for each matching line or within `BEGIN`/`END` blocks.

CSV example: `awk -F',' 'NR>1 {sum+=$1} END {printf "%.2f", sum/(NR-1)}' "$INPUT_FILE"`
* There are three arguments to `awk`.
	* `-F` is the field separator flag. `-F','` means that the columns are separated by commas. `$1`, `$2`, ... refer to the first column, second column, ...
	* `'NR>1 {sum+=$1} END {printf "%.2f", sum/(NR-1)}'` is the main script.
		* `NR` is a built-in `awk` variable that tracks the current record number (line number). `NR>1` only matches lines where `NR` is greater than 1, meaning it skips the first line (avoiding the header row).
		* `{sum+=$1}` accumulates the values stored in the first column. `sum` is implicitly initialized to 0.
		* `END { ... }` is the `END` block and runs after processing all lines. In this example, we calculate the average of the values in column 1, `sum/(NR-1)`, and print the output.
	* `"$INPUT_FILE"` is the CSV file name

## <u>`curl`</u>

https://medium.com/free-code-camp/how-to-start-using-curl-and-why-a-hands-on-introduction-ea1c913caaaa

Client URL. Run with `-f` option to fail silently. `curl --help` for options.

1. curl -f http://localhost:8501/

    curl: A command-line tool to send HTTP requests and receive responses from a server.
    -f (fail silently):
        This flag tells curl to fail and return a non-zero exit code if the HTTP response status code is 400 or higher (e.g., 404 Not Found, 500 Internal Server Error).
        Without this flag, curl would output the error message to the console but still return a success code (0), which is not useful in health checks.

## <u>`dirname`</u>

Extracts the directory name from a full file path, e.g. `dirname a/b/c/d.txt` will return the string `a/b/c/d`

## <u>`echo`</u>

`echo` is like `print` in Python but simpler.  
`echo "$string_var"`
`echo non_string_var`, e.g. `echo $?` to query the exit value of the last command/script

Common options:  
* `echo -n`: no newline at end
* `echo -e`: enable escape sequence interpretation (like `\t`, `\n`)
* `echo -E`: disable escape sequence interpretation

## <u>`exit`</u>

Used in a script, `exit n` terminates the script. `n`, an integer, is the exit status. By convention, `exit 0` means success, and any other integer means failure.

After running the script, you can query the exit value like so:  
```bash
./my_script.sh  
echo $?  
```

## <u>`mkdir`</u>

Create a new directory. `mkdir -p a/b/c/d` to create directory `d` with all of the required parent directories if they don't exist.

## <u>`nano`</u>

## <u>`wget`</u>

## <u>`which`</u>

# <u>Program execution in Linux terminal</u>

* `execute-command &`: to run the process in the background.
* Ctrl+C to interrupt a process running in the terminal.
* `ps -a`: list processes running in the terminal
* `ps -aux`: list processes with information
* `ps -aux | grep str`: look for processes that contain `str`, e.g. "python" to check for Python processes
	* `|` (aka pipe): send the output of `ps -aux` to the next command
	* `grep` is a regex-type program
* `kill`

## <u>`test`</u>

`test -f "$file" && echo "File exists" || echo "File does not exist"`

# Python in Linux

## System-wide commands

when is it python3 and when is it python?
pip3 vs pip?

python3 --version
pip --version
sudo apt install python3-pkg: use this to install essential tools like pip, venv. Manage project dependencies within virtual environments.
python3: start Python interpreter. exit() or Ctrl+D to exit interpreter.
python3 file-name.py: run file-name.py
python3 -m module: -m tells the Python interpreter to run module as a module (to look for and execute the main script inside the module code)
* You can create your own module with "if __name__ == '__main__':" to enable running it from the command line using python3 -m custom-module

## Virtual environments

Recommended: use separate virtual environments for different projects. 

Packaging environment information with your project:
* Using pip: pip freeze > requirements.txt / pip install -r requirements.txt

conda manages Python and non-Python dependencies. Its environments can have different Python versions. conda works across Windows, macOS, and Linux with a consistent interface on all platforms.

venv is a standard Python module for creating virtual environments for Python-only projects. Uses pip. Uses the same version of Python for all virtual environments (the Python version it's created with).
* To use venv, run the command "python3 -m venv folder-name": creates a virtual environment inside folder-name. Probably makes sense to create it inside your project folder.
* To activate a virtual environment, run the command "source folder-name/bin/activate". Within the virtual environment, use pip to install packages. Use the command "deactivate" to deactivate the virtual environment.
* To check which virtual environment is active, you can run "echo $VIRTUAL_ENV". VIRTUAL_ENV is the environment variable that holds the path to the current virtual environment. You can also run "which python", which shows the path to the Python interpreter, which should be within the virtual environment folder.


conda?

# Git in Linux

Apt-get install vs apt install?

sudo apt-get install git
git --version
git config --global user.name "rfdspeng"
git config --global user.email "tsai.ryanw@gmail.com"
ls -al ~/.ssh
ssh-keygen -t ed25519 -C "tsai.ryanw@gmail.com" -> enter enter enter