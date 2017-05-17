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
			Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			try
			{
				s.Connect(IPAddress.Parse("127.0.0.1"), 5901); 
				Console.Write("Zadej nejakej text : ");
				string q = Console.ReadLine();                 
				byte[] data = Encoding.Default.GetBytes(q);    
				s.Send(data);
			}
			catch
			{
				Console.WriteLine ("ERROR");
			}
		}
	}
}
