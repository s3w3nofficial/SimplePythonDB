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
			TcpClient client = new TcpClient(ip, port);
			NetworkStream nwStream = client.GetStream();
			byte[] bytesToSend = ASCIIEncoding.ASCII.GetBytes(msg);

			//---send the text---
			Console.WriteLine("Sending : " + msg);
			nwStream.Write(bytesToSend, 0, bytesToSend.Length);

			//---read back the text---
			byte[] bytesToRead = new byte[client.ReceiveBufferSize];
			int bytesRead = nwStream.Read(bytesToRead, 0, client.ReceiveBufferSize);
			Console.WriteLine("Received : " + Encoding.ASCII.GetString(bytesToRead, 0, bytesRead));
			client.Close();
		}
	}
}
