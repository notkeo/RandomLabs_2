class Linear:
    @staticmethod
    def help():
        return "[*] lc: [[seed array of numbers], lag_index, modulus]"

    def __init__(self, args, count):
        self.count = count
        self.seed = args[0]
        self.i = args[1]
        self.m = args[2]

    def next_value(self):
        for x in range(self.count):
            current_value = (self.seed[0] + self.seed[self.i]) % self.m
            self.seed = self.seed[1:]
            self.seed.append(current_value)
            yield current_value


class Additive:
    @staticmethod
    def help():
        return "[*] add: [seed, multiplier, increment ,modulus]"

    def __init__(self, args, count):
        self.count = count
        self.seed = args[0]
        self.a = args[1]
        self.c = args[2]
        self.m = args[3]


    def next_value(self):
        current_value = self.seed
        for x in range(self.count):
            current_value = (current_value * self.a + self.c) % self.m
            yield current_value


class LFSR:
    @staticmethod
    def help():
        return "[*] lfsr: [seed_number,[array of polynom degs],required bitlen for output numbers]"

    def create_seed(self, tmp_seed):
        tmp_seed = bin(tmp_seed)[2:]
        if len(tmp_seed) < self.max_deg:
            tmp_seed = tmp_seed[:self.max_deg]
        else:
            tmp_seed.zfill(self.max_deg)
        return [int(x) for x in tmp_seed]

    def __init__(self, args, count):
        self.count = count
        self.mask = args[1]
        self.max_deg = max(self.mask)
        self.seed = self.create_seed(args[0])
        self.bitlen = int(args[2])

    def next_value(self):
        for x in range(self.count):
            result = []
            for i in range(self.bitlen):
                random_bit = sum([self.seed[x] for x in self.mask]) % 2
                result.append(random_bit)
                self.seed = self.seed[1:] + [random_bit]
            yield result


class NFSR:
    @staticmethod
    def help():
        return "[*] nfsr: [[seed numbers],[[degs#1],[degs#2],[degs#3]],required bitlen for output numbers]"

    def __init__(self, args, count):
        self.seeds = args[0]
        self.degs = args[1]
        self.bitlen = args[2]
        self.count = count
        self.linear_generators = []
        for x in range(len(self.seeds)):
            self.linear_generators.append(LFSR([self.seeds[x], self.degs[x], 1], self.count))

    def next_value(self):
        for x in range(self.count):
            result = []
            for i in range(self.bitlen):
                x1 = self.linear_generators[0].next_value()[0]
                x2 = self.linear_generators[1].next_value()[0]
                x3 = self.linear_generators[2].next_value()[0]
                result.append((x1 * x2 ^ x2 * x3) ^ x3)
            yield result


class Mersenne:
    MATRIX_A = 0x9908b0df
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7fffffff

    @staticmethod
    def help():
        return "[*] nfsr: [[seed numbers],[[degs#1],[degs#2],[degs#3]],required bitlen for output numbers]"

    def create_seed(self, tmp_seed):
        seed = [tmp_seed]
        for x in range(622):
            seed.append(((1812433253 * (seed[x] ^ (seed[x] >> 30))) + x) & 0xFFFFFFFF)

    def __init__(self):
        pass
