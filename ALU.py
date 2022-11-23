def rotate(value, right):
    inp = f"{bin(value)[2:]:0>8}"
    out = ""
    for index,i in enumerate(inp):
        out += inp[(index+((-1)**right))%8]
    return int(out,2)

class ALU:
    carry = 0
    zero  = 0
    
    def calc(self,operation, A, B):
        self.carry = 0
        self.zero = 0
        if (operation == 0):
            return A
        elif (operation == 1):
            return ~A % 256
        elif (operation in [2,3]):
            return rotate(A, operation)
        elif (operation == 4):
            return A | B
        elif (operation == 5):
            return ~(A | B) % 256
        elif (operation == 6):
            return A & B
        elif (operation == 7):
            return ~(A & B) % 256
        elif (operation == 8):
            if ((A + B) > 255):
                self.carry = 1
            return (A + B) % 256
        elif (operation == 9):
            if ((A - B) == 0):
                self.zero = 1
            return (A - B) % 256
        else:
            return 0
