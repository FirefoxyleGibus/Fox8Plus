using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using static Fox8Assembly.Assembly;

namespace Fox8
{
	class ALU {
		internal bool zero = false;
		internal bool carry = false;

		internal byte Calc(byte A, byte B, byte Adr) {
			switch (Adr) {
				case 0:
					return A;
				case 1:
					return (byte)~A;
				case 2:
					return (byte)((A >> 1) | (A & 0b1));
				case 3:
					return (byte)((A << 1) | ((A & 0b10000000) >> 7));
				case 4:
					return (byte)(A | B);
				case 5:
					return (byte)(~(A | B));
				case 6:
					return (byte)(A & B);
				case 7:
					return (byte)(~(A & B));
				case 8:
					if (A + B > 255){
						carry = true;
					}
					return (byte)(A + B);
				case 9:
					if (A - B == 0)
					{
						zero = true;
					}
					return (byte)(A - B);
				default:
					return 0;
			}
		}
	}

	internal class Computer {
		ALU calculator = new ALU();

		byte adress = 0;
		bool HALT = false;

		byte[] Ram = new byte[256];
		ushort[] Rom = new ushort[256];
		byte[] Stk = new byte[256];

		byte A = 0;
		byte B = 0;
		byte SP = 0;
		ushort IR = 0;
		byte OUT = 0;

		void DoStep(int step)
		{
			if (step == 0) {
				IR = Rom[adress];
				adress++; step++;
			}
			else {
				byte par = (byte)(IR & 0x00FF);
				byte instr = (byte)((IR & 0xFF00) >> 8);
				switch (instr) {
					case 0x00: // NOP
						break;
					case 0x01: // JMP
						adress = par;
						break;
					case 0x02: // JIC
						if (calculator.carry) {
							adress = par;
						}
						break;
					case 0x03: // JIZ
						if (calculator.zero) {
							adress = par;
						}
						break;
					case 0x04: // LDA
						A = Ram[par];
						break;
					case 0x05: // STA
						Ram[par] = A;
						break;
					case 0x06: // LDB
						B = Ram[par];
						break;
					case 0x07: // STB
						Ram[par] = B;
						break;
					case 0x08: // PLA
						SP--;
						A = Stk[SP];
						break;
					case 0x09: // PSA
						Stk[SP] = A;
						SP++;
						break;
					case 0x0A: // PLB
						SP--;
						B = Stk[SP];
						break;
					case 0x0B: // PSB
						Stk[SP] = B;
						SP++;
						break;
					case 0x0C: // PLO
						SP--;
						OUT = Stk[SP];
						break;
					case 0x0D: // PLR
						SP--;
						Ram[par] = Stk[SP];
						break;
					case 0x0E: // PSR
						Stk[SP] = Ram[par];
						SP++;
						break;
					case 0x0F: // SSP
						SP = par;
						break;

					case 0x10: // LIA
						A = par;
						break;
					case 0x11: // LIB
						B = par;
						break;
					case 0x12: // JMS
						adress = Stk[SP];
						break;
					case 0x13: // JCS
						if (calculator.carry) {
							adress = Stk[SP];
						}
						break;
					case 0x14: // JZS
						if (calculator.zero) {
							adress = Stk[SP];
						}
						break;
					case 0x15: // JMR
						adress = Ram[par];
						break;
					case 0x16: // JCR
						if (calculator.carry) {
							adress = Ram[par];
						}
						break;
					case 0x17: // JZR
						if (calculator.zero) {
							adress = Ram[par];
						}
						break;
					case 0xFF: // INT
						if ((par == 0xFF) || (par == 0xFE)) {
							HALT = true;
						}
						break;
					default:
						if ((0x20 <= instr) && (instr <= 0x2F)) { // OPR
							Ram[par] = calculator.Calc(A, B, (byte)(instr & 0x0F));
						}
						else if ((0x30 <= instr) && (instr <= 0x3F)) { // OPA
							A = calculator.Calc(A, B, (byte)(instr & 0x0F));
						}
						else if ((0x40 <= instr) && (instr <= 0x4F)) { // OPB
							B = calculator.Calc(A, B, (byte)(instr & 0x0F));
						}
						else if ((0x50 <= instr) && (instr <= 0x5F)) { // OPO
							OUT = calculator.Calc(A, B, (byte)(instr & 0x0F));
						}
						else if ((0x60 <= instr) && (instr <= 0x6F)) { // OPS
							Stk[SP] = calculator.Calc(A, B, (byte)(instr & 0x0F));
							SP++;
						}
						break;
				}
			}
		}

		internal void loadProgram(ushort[] program) {
			for (int i = 0; i < 256; i++) {
				try {
					Rom[i] = program[i];
				}
				catch (IndexOutOfRangeException) {
					Rom[i] = 0;
				}
			}
		}

		internal void loadFile(string filename) {
			string[] content = File.ReadAllText(filename).Split(" ");
			ushort[] program = new ushort[content.Length-1];
			for (int i = 0; i < content.Length-1; i++) {
				program[i] = Convert.ToUInt16(content[i], 16);
			}
			loadProgram(program);
		}

		internal void DoCycles(int number) {
			for (int i = 0; i < number; i++) {
				DoStep(0); DoStep(1);
				if (HALT) {
					Console.WriteLine("HALT");
					break;
				}
			}
		}

		internal void runComputer() {
			while (!HALT) {
				DoStep(0); DoStep(1);
			}

		}

		internal void Test() {
			Stopwatch sp = Stopwatch.StartNew();
			runComputer();
			Console.WriteLine(OUT.ToString() + " " + sp.Elapsed);
		}
	}

	internal class Program
	{
		static void Main(string[] args)
		{
			Computer A = new Computer();
			A.loadProgram(GenerateCode(@"C:\Users\maxen\Documents\Computer\Emulated\Program\Multiplication.txt"));
			A.Test();
		}
	}
}
