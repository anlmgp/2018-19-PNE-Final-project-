class Seq:

    def __init__(self, strbases):
        self.strbases = strbases

    def len (self):
        return len(self.strbases)

    def complement(self):
        bases = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        result1 = []
        for i in self.strbases:
            if i in bases:
                result1.append(bases[i])
        result1 = "".join(result1)
        return Seq(result1)

    def reverse(self):
        return Seq(self.strbases[::-1])

    def count1(self, base):
        return self.strbases.count(base)

    def perc(self, base ):
        if len(self.strbases) > 0:
            cb = self.count1(base)
            return round(100.0 * cb / len(self.strbases), 1)
        else:
            return 0