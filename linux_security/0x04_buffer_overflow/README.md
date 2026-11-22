# Buffer overflow

## 0. Hack the VM

`read_write_heap.py` finds the first matching sequence of ASCII bytes
in a running Linux process's writable `[heap]` mapping and replaces it
in place. It uses `/proc/PID/maps` to locate the heap and `/proc/PID/mem`
to read and write it.

```sh
./read_write_heap.py pid search_string replace_string
```

The search string must be nonempty. The replacement may be empty or
up to the length of the search string. Shorter replacements are padded
with NUL bytes to fit the original space.

For the supplied C program, run `./main` in one terminal and use its
actual PID in the other. Use `sudo` if your VM requires elevated
permissions to access the process.

```sh
sudo ./read_write_heap.py 6515 Holberton maroua
```

The script is silent on success. Set `RWH_VERBOSE=1` to print the
replacement address. Usage errors go to stdout and exit with status 1.
