instr = {"NOP":"00",
         "JMP":"01",
         "JIC":"02",
         "JIZ":"03",
         "LDA":"04",
         "STA":"05",
         "LDB":"06",
         "STB":"07",
         "PLA":"08",
         "PSA":"09",
         "PLB":"0A",
         "PSB":"0B",
         "PLO":"0C",
         "PLR":"0D",
         "PSR":"0E",
         "SSP":"0F",
         "LIA":"10",
         "LIB":"11",
         "JMS":"12",
         "JCS":"13",
         "JZS":"14",
         "JMR":"15",
         "JCR":"16",
         "JZR":"17",
         "OPR":"2",
         "OPA":"3",
         "OPB":"4",
         "OPO":"5",
         "OPS":"6",
         "HDR +":"FFFD",
         "HDR P":"FFFE",
         "HLT":"FFFF"}

operation = {"BUFF":"0",
             "NOT" :"1",
             "ROR" :"2",
             "ROL" :"3",
             "OR"  :"4",
             "NOR" :"5",
             "AND" :"6",
             "NAND":"7",
             "ADD" :"8",
             "SUB" :"9"}

def decodeNumber(number,variable):
    if (number[0] == "#"):
        return f"{number[1:]:>02}"
    elif (number[0] == "%"):
        return f"{hex(int(number[1:],2))[2:]:>02}".upper()
    elif (number[0] == "$"):
        return f"{hex(int(number[1:]))[2:]:>02}".upper()
    else:
        return f"{variable[number]:>02}".upper()

def decodeOneInstr(line,variable):
    out = ""
    curr = line.split(" ")
    if (curr[0] in ["OPR","OPA","OPB","OPO","OPS"]):
        if (curr[0] == "OPR"):
            par = decodeNumber(curr[2],variable)
            out += instr[curr[0]] + operation[curr[1]] + par
        else:
            out += instr[curr[0]] + operation[curr[1]] + "00"
    elif (curr[0] in ["HLT","SHO"]):
        out += instr[curr[0]]
    elif (curr[0] in ["PLA","PSA","PLB","PSB","NOP","PLO","JMS","JCS","JZS"]):
        out += instr[curr[0]] + "00"
    else:
        par = decodeNumber(curr[1],variable)
        out += instr[curr[0]] + par
    return out

def decodeVariable(line, variable):
    name = ""
    val = ""
    ind = 0
    step = 0
    for index,value in enumerate(line.replace(" ","")):
        if (value == "="):
            step += 1
        elif (value != "=" and step == 0):
            name += value
        elif (value != "=" and step == 1):
            val += value
            
    return name, decodeNumber(val, variable)

def assemble(file):
    with open(file,mode="r") as of:
        A = of.read()
    lines = A.split("\n")
    out = ""
    count = 0
    variable = {}
    for i in lines:
        curr = i.replace("\t","")
        if (curr == ""):
            continue
        if (curr[-1] == ":"):
            variable[i[:-1]] = hex(count)[2:]
        elif ("=" in curr):
            pass
        else:
            count += 1
    for i in lines:
        curr = i.replace("\t","")
        if (curr == ""):
            continue
        if ("=" in curr):
            A, B = decodeVariable(curr,variable)
            variable[A] = B
        elif not (curr[-1] == ":"):
            out += decodeOneInstr(curr,variable) + " "
    print(out)
    return out

if __name__ == "__main__":
    with open(r"Compiled\B&F.f8p","w") as F:
        F.write(assemble(r"Program\BackAndForth.txt"))
