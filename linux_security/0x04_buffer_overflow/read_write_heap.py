#!/usr/bin/python3
"""Replace an ASCII C string in a running Linux process's heap."""

import os
import sys


CHUNK_SIZE = 1024 * 1024


def find_in_range(fd, start, end, needle):
    """Return the address of the first match wholly inside the range."""
    address = start
    tail = b""
    overlap = len(needle) - 1

    while address < end:
        chunk = os.pread(fd, min(CHUNK_SIZE, end - address), address)
        if not chunk:
            raise OSError("Heap read ended before the mapping boundary")

        data = tail + chunk
        offset = data.find(needle)
        if offset != -1:
            return address - len(tail) + offset

        tail = data[-overlap:] if overlap else b""
        address += len(chunk)

    return None


def replace_in_heap(pid, search, replacement):
    """Replace the first byte match and return its address."""
    payload = replacement.ljust(len(search), b"\0")
    proc_path = "/proc/{}".format(pid)
    proc_fd = os.open(proc_path, os.O_RDONLY | os.O_DIRECTORY)

    def open_proc_file(name, flags):
        """Open a file relative to the pinned process directory."""
        return os.open(name, flags, dir_fd=proc_fd)

    try:
        with open("maps", "rb", opener=open_proc_file) as maps, open(
            "mem", "r+b", buffering=0, opener=open_proc_file
        ) as memory:
            fd = memory.fileno()
            for line in maps:
                fields = line.split(None, 5)
                if len(fields) != 6 or fields[5].rstrip() != b"[heap]":
                    continue
                if not fields[1].startswith(b"rw"):
                    continue

                bounds = fields[0].split(b"-", 1)
                start, end = (int(bound, 16) for bound in bounds)
                address = find_in_range(fd, start, end, search)
                if address is None:
                    continue

                if os.pread(fd, len(search), address) != search:
                    raise OSError("Heap contents changed before the write")
                if os.pwrite(fd, payload, address) != len(payload):
                    raise OSError("Incomplete write to the heap")
                return address
    finally:
        os.close(proc_fd)

    raise ValueError("Search string not found in a writable [heap] mapping")


def main(args):
    """Validate arguments, replace the string, and return a status."""
    if len(args) != 3:
        print("Usage: read_write_heap.py pid search_string replace_string")
        return 1

    try:
        pid_text, search_text, replacement_text = args
        if not pid_text or pid_text.strip("0123456789"):
            raise ValueError("PID must be a positive integer")
        pid = int(pid_text)
        if pid <= 0:
            raise ValueError("PID must be a positive integer")
        search = search_text.encode("ascii")
        replacement = replacement_text.encode("ascii")
        if not search:
            raise ValueError("Search string must be nonempty")
        if len(replacement) > len(search):
            raise ValueError("Replacement must fit within the search string")
    except UnicodeEncodeError:
        print("Error: both strings must contain only ASCII characters")
        return 1
    except ValueError as error:
        print("Error: {}".format(error))
        print("Usage: read_write_heap.py pid search_string replace_string")
        return 1

    try:
        address = replace_in_heap(pid, search, replacement)
    except (OSError, ValueError) as error:
        print("Error: {}".format(error))
        return 1

    if os.environ.get("RWH_VERBOSE") is not None:
        print("Replaced string at {:#x} in PID {}".format(address, pid))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
