# Metagraph
Program for metagraph attributes calculation
## Overview

## Input Requirements
To run program ones should prepare input file (see `input.txt` for example format).

## Usage

To run a program, use the following command in a Linux terminal:

```bash
main <INPUT_FILE> <OUTPUT_FILE>
```

Where:
- `<INPUT_FILE>`: Path to the input parameters file (e.g., `input.txt`)
- `<OUTPUT_FILE>`: Path to output file

### Example
```bash
main input.txt output.txt
```

## Output File

The program produces file with attributes of metagraph. First NV strings reflect attributes of vertexes, next NE strings - attributes of edges.
