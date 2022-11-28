using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace Fox8Assembly
{
	static internal class Assembly
	{
	    static Dictionary<string, string> variable = new Dictionary<string,string>();

		static Dictionary<string, string> INSTR = new Dictionary<string, string> {
			{ "NOP", "00" },
			{ "JMP", "01" },
			{ "JIC", "02" },
			{ "JIZ", "03" },
			{ "LDA", "04" },
			{ "STA", "05" },
			{ "LDB", "06" },
			{ "STB", "07" },
			{ "PLA", "08" },
			{ "PSA", "09" },
			{ "PLB", "0A" },
			{ "PSB", "0B" },
			{ "PLO", "0C" },
			{ "PLR", "0D" },
			{ "PSR", "0E" },
			{ "SSP", "0F" },
			{ "LIA", "10" },
			{ "LIB", "11" },
			{ "JMS", "12" },
			{ "JCS", "13" },
			{ "JZS", "14" },
			{ "JMR", "15" },
			{ "JCR", "16" },
			{ "JZR", "17" },
			{ "OPR", "2" },
			{ "OPA", "3" },
			{ "OPB", "4" },
			{ "OPO", "5" },
			{ "OPS", "6" },
			{ "HDR+", "FFFD" },
			{ "HDRP", "FFFE" },
			{ "HLT", "FFFF" },
		};

		static Dictionary<string, string> OP = new Dictionary<string, string> {
			{ "BUFF", "0" },
			{ "NOT",  "1" },
			{ "ROR",  "2" },
			{ "ROL",  "3" },
			{ "OR",   "4" },
			{ "NOR",  "5" },
			{ "AND",  "6" },
			{ "NAND", "7" },
			{ "ADD",  "8" },
			{ "SUB",  "9" }
		};

		public static string DecodeNumber(string number) {
			if (number[0] == '#') {
				return number.Substring(1);
			}
			else if (number[0] == '%') {
				return String.Format("{0:X2}", Convert.ToUInt64(number.Substring(1), 2));
			}
			else if (number[0] == '$') {
				return String.Format("{0:X2}", Convert.ToUInt64(number.Substring(1)));
			}
			else {
				return variable[number];
			}
		}

		public static string DecodeOneInstr(string line) {
			string[] lines = line.Split(' ');
			string output = "";
			if (lines[0] == "OPR") { output = INSTR[lines[0]] + OP[lines[1]] + DecodeNumber(lines[2]); }
			else if (lines[0] == "OPA" || lines[0] == "OPB" || lines[0] == "OPO" || lines[0] == "OPS") { output = INSTR[lines[0]] + OP[lines[1]] + "00"; }
			else if (lines[0] == "HLT" || lines[0] == "HDR+" || lines[0] == "HDRP") { output = INSTR[lines[0]]; }
			else if (lines[0] == "NOP" || lines[0] == "PLA" || lines[0] == "PSA" || lines[0] == "PLB" || lines[0] == "PSB" || lines[0] == "PLO" || lines[0] == "PLR" || lines[0] == "PSR"
			|| lines[0] == "JMS" || lines[0] == "JCS" || lines[0] == "JZS") { output = INSTR[lines[0]] + "00"; }
			else { output = INSTR[lines[0]] + DecodeNumber(lines[1]); }
			return output;
		}

		public static string DecodeFile(string filename) {
			string[] content = File.ReadAllText(filename).Replace("\t","").Replace("\r","").Split("\n");
			string output = "";
			int count = 0;
			foreach (string line in content) {
				if (line.Trim() == "") { continue; }
				if (line.EndsWith(":")) { variable.Add(line.Remove(line.Length - 1), String.Format("{0:X2}", count)); }
				else if (line.Contains("=") || line.StartsWith("/")) { continue; }
				else { count++; }
			}
			foreach (string line in content) {
				if (line.Trim() == "") { continue; }
				if (line.Contains("=")) {
					string[] info = line.Split('=');
					variable.Add(info[0].Trim(), DecodeNumber(info[1].Trim()));
				}
				else if (line.StartsWith("/") || line.EndsWith(":")) { continue; }
				else {
					output += DecodeOneInstr(line) + " ";
				}
			}
			return output;
		}

		public static ushort[] GenerateCode(string filename) {
			string[] prog = DecodeFile(filename).Split(" ");
			ushort[] code = new ushort[prog.Length - 1];
			for (int i = 0; i < prog.Length - 1; i++)
			{
				code[i] = Convert.ToUInt16(prog[i], 16);
			}
			return code;
		}
	}

	/*internal class Program
	{
		static void Main(string[] args)
		{
			Console.WriteLine(Assembly.DecodeFile(@"C:\Users\maxen\Documents\Computer\Emulated\Program\Multiplication.txt"));
		}
	}*/
}
