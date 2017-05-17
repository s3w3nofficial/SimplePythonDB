using System;
using System.Net.Sockets;
using System.Text;
using System.Net;

namespace atm
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			while (true) {
				Console.Write ("type query: ");
				string query = Console.ReadLine ();
				Connect ("127.0.0.1", 5901, query);
			}
		}

		public static void Connect(string ip, int port, string msg)
		{
			Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			try { 

				s.Connect (IPAddress.Parse ("127.0.0.1"), 5901);          
				byte[] data = Encoding.Default.GetBytes (msg);    
				s.Send (data);
			} catch {
				Console.WriteLine ("ERROR");
			}
		}

	}
}
