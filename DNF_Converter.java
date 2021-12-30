import java.util.Scanner;

public class DNF_Converter {
	
	//helper parameters
	private static int i=0, n=0;
	private static String answer="";
	private static char type;
	
	//convert to DNF (or CNF)
	public static void convert(int[] p, int valid) {
		if(type=='D' && valid==1) {
			answer+="(";
			for(int k=0; k<=n; k++) {
				if(p[k]==-1)
					answer+="-";
				if(k<n)
					answer+="p"+(k+1)+"^";
				else
					answer+="p"+(k+1)+")v";
			}
		}
		else if(type=='C' && valid==-1) {
			answer+="(";
			for(int k=0; k<=n; k++) {
				if(p[k]==1)
					answer+="-";
				if(k<n)
					answer+="p"+(k+1)+"v";
				else
					answer+="p"+(k+1)+")^";
			}
		}
	}
	
	//assign value to p and runs formula validation function
	public static void assign(int[] p, int j, final char[] x) {
		if(j!=0)
			for(int k=1; k>=-1; k-=2) {
				p[j]=k;
				assign(p,j-1,x);
			}
		else
			for(int k=1; k>=-1; k-=2) {
				p[0]=k;
				i=0;
				convert(p, validate(x,p));
			}
	}
	
	//calculate validity of formula for assigned p values
	public static int validate(final char[] x, final int p[]) {
		int l = 0;
		while(x[i] != ';') {
			switch (x[i]) {
				case '(':
					i++;
					if(i!=1)
						return validate(x,p);
					l=validate(x,p);
					break;
					//***
					
				case ')':
					i++;
					return l;
					//***
					
				case 'p':
					int j = 1;
					String s = "";
					while(Character.isDigit(x[i+j])) {
						s += Character.toString(x[i+j]);
						j++;
					}
					l = p[Integer.parseInt(s)-1];
					j--;
					i+=j;
					if(i!=j)
						if(x[i-j-1]!='(')
							if(x[i-j-1]!='-')
							return l;
					break;
					//***
					
				case '-':
					i++;
					if(x[i+1] == '>')
						break;
					l=-validate(x,p);
					break;
					//***
					
				case '>':
					i++;
					l = Math.max(-l, validate(x,p));
					break;
					//***
					
				case '^':
					i++;
					l = Math.min(l, validate(x,p));
					break;
					//***
					
				case 'v':
					i++;
					l = Math.max(l, validate(x,p));
					break;
					//***
					
				default:
					i++;
			}
		}
		return l;
	}
	
	
	public static void main(String[] args) {
	//***************
		//input formula
		Scanner reader = new Scanner(System.in);
		System.out.println("Type formula with no spaces. (this program does not recognize priority of ^ over V) "
				+ "\n example: p1v(p2^-p1)->p2\noperators: ( ) v ^ -> p1 p2 ...\n");
		final char[] x = (reader.next()+";").toCharArray();
		System.out.println("\nDNF or CNF? (type with capital letters)\n");
		type = reader.next().charAt(0);
		reader.close();
		
		//number of p
		while(x[i] != ';') {
			if(x[i] == 'p') {
				int j = 1;
				String s = "";
				while(Character.isDigit(x[i+j])) {
					s += Character.toString(x[i+j]);
					j++;
				}
				i+=j-1;
				n=Math.max(Integer.parseInt(s), n);
			}
			i++;
		}
		int[] p = new int[n];
		n--;
		
		//start
		assign(p,n,x);
		
		//output
		System.out.println(answer.substring(0, answer.length()-1));
		
		
		
	//***************
	}
}
