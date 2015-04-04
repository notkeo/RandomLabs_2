import sys
from generators import Linear, Additive, LFSR, NFSR
import argparse
from argparse import ArgumentParser

generators_list = {'lc': Linear, 'add': Additive, 'lfsr': LFSR, 'nfsr': NFSR}


def generators_help():
    help = ''
    for x in generators_list.keys():
        help += generators_list[x].help() + '\n'
    return help


def init_parser():
    global generators_list
    parser = ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-g', metavar='generator', choices=dict(generators_list).keys(),
                        help="type of pseudo-random generator. \nvalid values:  " + ",".join(generators_list.keys()))
    parser.add_argument('-i', metavar='init',
                        help="initial vector for selected generator. \n Use -i help")
    parser.add_argument('-n', metavar='numbers', type=int, default=1000,
                        help="amount of generated numbers (default: 1000)")
    parser.add_argument('-f', metavar='filename', help="output file name ")

    return parser


def generate(args):
    init = eval(args.i)
    generator = generators_list[args.g](init, args.n)
    with open(args.f, 'w') as f:
        for x in generator.next_value():
            if args.g == 'lfsr':
                x = int(''.join([str(i) for i in x]), 2)
            f.write(str(x) + '\n')


def main():
    parser = init_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.i == "help":
        print generators_help()
    else:
        if args.f and args.g and args.i:
            generate(args)
        else:
            print "invalid args size"
            parser.print_usage()


if __name__ == '__main__':
    main()