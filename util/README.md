# root-shell.c

This folder contains code to support exploitation of shared object misconfigurations, notably when implementing shared objects. When compiled in the correct location, with the correct function signature, the code in `root-shell.c` spawns a Bash process running as root.

## Compilation Instructions

To compile this code, run the following commands (which require `gcc` to be installed):

```
gcc -c -Wall -fPIC root-shell.c 
```

```
gcc -shared -o root-shell.so root-shell.o -nostartfiles
```


