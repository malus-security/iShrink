# iShrink
Minimization of  Apple sandbox profiles

## Dependencies

The project requires the following dependencies in order to run:
* `cmake`
* `nlohmann/json`

To install these dependencies use homebrew likewise:
```sh
$ brew tap nlohmann/json
$ brew install cmake nlohmann_json
```

## Installation
```sh
git clone --recursive https://github.com/malus-security/iShrink.git
# Install submodule
# - maap: For the installation guide check Jakob Rieck's repo at https://github.com/0xbf00/maap

# Build matching-core
$ mkdir matching-core/build
$ cd matching-core/build
$ cmake ..
$ make
```

## Usage

To minimize a profile, follow these steps:

1. Use the analysis script from Jakob Rieck's macos-sandbox-coverage solution.
2. Use the minimization script to obtain the minimized `rules.sb` sandbox profile in SBPL.
3. Compile using compile\_sb from Stefan Esser's sandbox\_toolkit.
4. Use the test script to apply the compiled minimized profile to the app.

## Using macos-sandbox-coverage

The program only supports two switches:

1. Use `--app` to specify the path to the application you want to collect sandbox coverage data for
2. Use `--timeout` to specify the number of seconds for the app to run. If you do not specify a timeout, the app will run indefinitely or until it is closed by the user.

```sh
$ ./sandbox_coverage.py --app /Applications/Calculator.app > output.json
```
## Obtaining the minimized sandbox profile

```sh
$ ./minimize.py output.json
```

## Compiling the resulted profile

```sh
$ ./maap/extern/compile_sb rules.sb rules.bin
```

## Applying the compiled profile
The test script has three switches:
1. `--app` to provide the path to the application
2. `--timeout` to specify the amount of time in seconds for the app to be tested. This is an optional argument, the application will run until is terminated by the user unless a timeout is specified.
3. `--m` to provide the path to the compiled minimized profile.

```sh
$ test.py --ap /System/Applications/Calendar.app/ --timeout 60 --m rules.bin
```

## Compiling the resulted profile

```sh
$ ./maap/extern/compile_sb rules.sb rules.bin
```

