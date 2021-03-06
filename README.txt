PLATFORM
========
DistAlgo version: 1.0.11
Python3 (CPython) version: 3.5.1, 3.6 (for multi-host on Docker)
Operating System: Windows 7, MAC OS
Hosts: Laptop (without VMs), Docker Images

DEPENDENCIES
============
PyDistAlgo
PyNacl
Pickle [Pre-installed]
JSON [Pre-installed]

pip install --upgrade pydistalgo pynacl

INSTRUCTIONS
============

python3 -m da <src file> -i <config file>

e.g.
python3 -m da src/bcr.da -i config/phase3/test_phase3.txt

For large workloads, we increased the recursion limit of Python.

For multi-node:
Node 1: Other Replicas, Client, Olympus
Node 2 : Head

python3 -m da --logfile --logfilename=logs/simple-log.txt --logfilelevel=info --message-buffer-size=96000 -n Node1 -H <Node1's own IP> -R <Other node's IP> src/multihost/bcr.da -i config/phase3/simple.txt
python3 -m da --logfile --logfilename=logs/simple-log.txt --logfilelevel=info --message-buffer-size=96000 -n Node2 -D -H <Node2's own IP> -R <Other node's IP> src/multihost/bcr.da -i config/phase3/simple.txt

WORKLOAD GENERATION
===================

Python's random module and random module's random function is used for pseudorandom workload generation. Initially, the given seed is set, and one of the four operations is randomly selected. Similarly, the keys and values of a particular set length are randomly generated using the above module and function.
As a convention, all keys and values generated have a fixed length of 3 to keep the system simple.

BUGS AND LIMITATIONS
====================
1. For large workloads, some of logs randomly gets omitted even if those commands have been executed. It has been reproduced by other students as well, thus this appears to be a bug in Python/DistAlgo [Windows 7]. We didn't face this issue yet when running on Unix system.

COMPARISON WITH RAFT
====================
Considering the design of our program, gracefully exiting all nodes was a challenge, so instead we used time utility given in Linux systems for calculating program running times.

e.g. time <python command>

After the logs were printed, we just used Ctrl + C to end the execution and get the timing stats.

RAFT2: ~10s
BCR on single host: ~36s [approximately] [print output to stdout takes a lot of time]
BCR on multiple host: ~40s [approximately] [print output to stdout takes a lot of time]

Note: We were adding 0.1s sleep between each client request for stability, we subtracted that from total time taken by the program for more appropriate timing stats.

Multi-Host Setup
================
We used two docker images (on Mac) with Python 3.6 and PyDistAlgo 1.0.11 to simulate multi-host setup. 
For large workloads, we increased the recursion limit of Python and RAM given to the docker images.

CONTRIBUTIONS
=============

Ankit Aggarwal (anaaggarwal, 111485578):
Reconfiguration
Checkpointing
Failure Triggers and Injection
Digital Signing and Verification
Multi-host support
Logging
Testing

Saraj Munjal (smunjal, 111497962):
Reconfiguration
Checkpointing
Failure Triggers and Injection
Digital Signing and Verification
Multi-host support
Logging
Testing

MAIN FILES
==========

Main entry: src/bcr.da
Implementation of the Replica: src/replica.da
Implementation of the Olympus: src/olympus.da
Implementation of the Client: src/client.da
Setting up configuration for the program and workload generation: src/config.py
Parsing the configuration file: src/read_config.py

Implementation for multi-node setup: Head on Node2, everything else on Node1
Main entry: src/multihost/bcr.da
Implementation of the Replica: src/multihost/replica.da
Implementation of the Olympus: src/multihost/olympus.da
Implementation of the Client: src/multihost/client.da
Setting up configuration for the program and workload generation: src/multihost/config.py
Parsing the configuration file: src/multihost/read_config.py


CODE SIZE
=========

(1a) Lines of code for:
    Algorithm: ~1200
    Other: ~500
    Total: ~1700

(1b) Counts are obtained using: https://github.com/AlDanial/cloc

(2) Lines of code for:
    Core Algorithm: ~800
    Interleaved testing: ~400

LANGUAGE FEATURE USAGE
====================== 

List Comprehensions: ~15
Dictionary Comprehensions: ~2-3
Set Comprehensions: ~8-9
Aggregations: 1
Quantifications: ~2-3
Classes: 5
Enums: 3
Lambda: ~10
Map: ~10
