# Metagraph
Program for metagraph attributes calculation
## Overview
The program calculates attributes for given annotated metagraph and agent-functions. At the first stage program initializes and link graph elements, sets attributes and rules. Further, it dynamically turns over the elements without attributes and tries to calculate attribute values. If state of graph doesn't change after iteration of elements without attributes, that means that graph architecture is wrong and it is impossible to calculate all attributes. In this case an error rises. After establishing of attributes for all graph elements, the program print result in given output file.

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
