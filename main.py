from argparse import ArgumentParser

from metagraph import Metagraph


def main():
    parser = ArgumentParser()                                                            # Read arguments from
    parser.add_argument('inp_pth', type=str, help='Path to file with input parameters')  # command line
    parser.add_argument('outp_pth', type=str, help='Path to output file')                #
    args = parser.parse_args()

    graph = Metagraph(args.inp_pth)          # Initialization of metagraph
    graph.calculate_attributes()             # Perform calculations of missed attributes
    graph.print_attrs_in_file(args.outp_pth) # Write result in file


if __name__ == '__main__':
    main()