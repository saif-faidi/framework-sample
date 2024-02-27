# framework-sample
## Config:
if an explicit .yaml file is provided it will be used as the config file
if not then the default config.yaml file will be used from the PROJECT_DIR/src folder

## Function name:
a function name will be provided to all the project
a function name will be provided to the protocol instance ( a sub function ) if no function is provided
in the protocol then the global function name is used, if no global function name is provided then we should
use the project name as the function name

## Callbacks
callbacks should be implemented externally not in the associated class itself because this class should not know about
which protocol is being used """

## Thread handling
TODO : we should find a way to automatically clean up all the threads in the main program