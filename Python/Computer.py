# Fox8+ was created by FirefoxyLeGibus
# This emulation is a way to do funny things with it
# Have fun with it
# You can change the program and frequency in the last line

from ALU import *
from Assembly import assemble
from time import sleep, perf_counter

Adress = 0
Step = 0
Zero = 0
Carry = 0
Halt = False

Ram = [0] * 256
Rom = [0] * 256
Stk = [0] * 256

A    = 0
B    = 0
SP   = 0
IR   = 0
ADR  = 0
ALOP = 0
OUT  = 0
alu  = ALU()

def DoStep():
    global Adress, Step, A, B, SP, ADR, ALOP, OUT, IR, Zero, Carry, Halt
    
    if (Step == 0):
        IR = Rom[Adress]
        Adress += 1
        Adress %= 256
        Step += 1
    else:
        instr = (IR & 0xFF00) >> 8
        par = IR & 0xFF
        
        if (instr == 0x00): # NOP
            Step = 0
            
        if (instr == 0x01): # JMP
            if (Step == 1):
                Adress = par
                Step = 0
                
        if (instr == 0x02): # JIC
            if (Step == 1):
                if (Carry == 1):
                    Adress = par
                Step = 0
            
        if (instr == 0x03): # JIZ
            if (Step == 1):
                if (Zero == 1):
                    Adress = par
                Step = 0
            
        if (instr == 0x04): # LDA
            if (Step == 1):
                ADR = par
                Step += 1
            if (Step == 2):
                A = Ram[ADR]
                Step = 0
                
        if (instr == 0x05): # STA
            if (Step == 1):
                ADR = par
                Step += 1
            if (Step == 2):
                Ram[ADR] = A
                Step = 0
                
        if (instr == 0x06): # LDB
            if (Step == 1):
                ADR = par
                Step += 1
            if (Step == 2):
                B = Ram[ADR]
                Step = 0
                
        if (instr == 0x07): # STB
            if (Step == 1):
                ADR = par
                Step += 1
            if (Step == 2):
                Ram[ADR] = B
                Step = 0
                
        if (instr == 0x08): # PLA
            if (Step == 1):
                SP -= 1
                SP %= 256
                Step += 1
            if (Step == 2):
                A = Stk[SP]
                Step = 0
                
        if (instr == 0x09): # PSA
            if (Step == 1):
                Stk[SP] = A
                Step += 1
            if (Step == 2):
                SP += 1
                SP %= 256
                Step = 0
                
        if (instr == 0x0a): # PLB
            if (Step == 1):
                SP -= 1
                SP %= 256
                Step += 1
            if (Step == 2):
                B = Stk[SP]
                Step = 0
                
        if (instr == 0x0b): # PSB
            if (Step == 1):
                Stk[SP] = B
                Step += 1
            if (Step == 2):
                SP += 1
                SP %= 256
                Step = 0
                
        if (instr == 0x0c): # PLO
            if (Step == 1):
                SP -= 1
                SP %= 256
                Step += 1
            if (Step == 2):
                OUT = Stk[SP]
                Step = 0
                
        if (instr == 0x0d): # PLR
            if (Step == 1):
                SP -= 1
                SP %= 256
                Step += 1
            if (Step == 2):
                Ram[ADR] = Stk[SP]
                Step = 0
                
        if (instr == 0x0e): # PSR
            if (Step == 1):
                Stk[SP] = Ram[ADR]
                Step += 1
            if (Step == 2):
                SP += 1
                SP %= 256
                Step = 0
                
        if (instr == 0x0f): # SSP
            if (Step == 1):
                SP = par
                Step = 0

        if (instr == 0x10): # LIA
            if (Step == 1):
                A = par
                Step = 0

        if (instr == 0x11): # LIB
            if (Step == 1):
                B = par
                Step = 0

        if (instr == 0x12): # JMS
            if (Step == 1):
                Adress = Stk[SP]
                Step = 0
                
        if (instr == 0x13): # JCS
            if (Step == 1):
                if (Carry == 1):
                    Adress = Stk[SP]
                Step = 0
            
        if (instr == 0x14): # JZS
            if (Step == 1):
                if (Zero == 1):
                    Adress = Stk[SP]
                Step = 0

        if (instr == 0x15): # JMR
            if (Step == 1):
                Adress = Ram[ADR]
                Step = 0
                
        if (instr == 0x16): # JCR
            if (Step == 1):
                if (Carry == 1):
                    Adress = Ram[ADR]
                Step = 0
            
        if (instr == 0x17): # JZR
            if (Step == 1):
                if (Zero == 1):
                    Adress = Ram[ADR]
                Step = 0

        if (0x1f < instr < 0x30): # OPR
            if (Step == 1):
                ALOP = instr & 0x0F
                ADR = par
                Step += 1
            if (Step == 2):
                Ram[ADR] = alu.calc(ALOP, A, B)
                Zero = alu.zero
                Carry = alu.carry
                Step = 0

        if (0x2f < instr < 0x40): # OPA
            if (Step == 1):
                ALOP = instr & 0x0F
                Step += 1
            if (Step == 2):
                A = alu.calc(ALOP, A, B)
                Zero = alu.zero
                Carry = alu.carry
                Step = 0

        if (0x3f < instr < 0x50): # OPB
            if (Step == 1):
                ALOP = instr & 0x0F
                Step += 1
            if (Step == 2):
                B = alu.calc(ALOP, A, B)
                Zero = alu.zero
                Carry = alu.carry
                Step = 0

        if (0x4f < instr < 0x60): # OPO
            if (Step == 1):
                ALOP = instr & 0x0F
                Step += 1
            if (Step == 2):
                OUT = alu.calc(ALOP, A, B)
                Zero = alu.zero
                Carry = alu.carry
                Step = 0

        if (0x5f < instr < 0x70): # OPS
            if (Step == 1):
                ALOP = instr & 0x0F
                Step += 1
            if (Step == 2):
                Stk[SP] = alu.calc(ALOP, A, B)
                Zero = alu.zero
                Carry = alu.carry
                Step = 0

        if (instr == 0xff):
            if (par == 0x00):
                if (Step == 1):
                    print("Out :",OUT)
                    Step = 0
            if (par == 0xff): # HLT
                Halt = True

def doOneCycle(frequence):
    t1 = perf_counter()
    DoStep()
    t2 = perf_counter()
    dT = (t2 - t1)
    if (dT > 1/frequence):
        print("TOO FAST! Max is",1/dT)
    else:
        sleep((1/frequence) - dT)

def doMultipleCycle(cycle, frequence):
    for i in range(cycle):
        doOneCycle(frequence)
        if (Halt):
            break

def runComputer(frequence):
    while(not Halt):
        doOneCycle(frequence)

def test():
    t1 = perf_counter()
    while(not Halt):
        DoStep()
    t2 = perf_counter()
    print(t1-t2)

def loadProgram(file):
    with open(file, mode='r') as f:
        data = f.read().split(" ")
    for index,value in enumerate(data):
        Rom[index] = int(value,16)

def readProgram(array):
    data = array.split(" ")
    for index,value in enumerate(data):
        if (value == ""):
            continue
        Rom[index] = int(value,16)

def Main():
    pass

def Loop():
    pass

readProgram(assemble(r"C:\Users\maxen\Documents\Computer\Emulated\Program\Multiplication.txt"))
test()
print(OUT)
input()
