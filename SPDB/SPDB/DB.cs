using System;
using System.Net.Sockets;
using System.Text;

namespace SPDB
{
	public class DB
	{
		public static string Connect(string ip, int port, string msg)
		{
			TcpClient client = new TcpClient(ip, port);
			NetworkStream nwStream = client.GetStream();
			byte[] bytesToSend = ASCIIEncoding.ASCII.GetBytes(msg);

			//---send the text---
			nwStream.Write(bytesToSend, 0, bytesToSend.Length);

			//---read back the text---
			byte[] bytesToRead = new byte[client.ReceiveBufferSize];
			int bytesRead = nwStream.Read(bytesToRead, 0, client.ReceiveBufferSize);
			string res = Encoding.ASCII.GetString(bytesToRead, 0, bytesRead);
			client.Close();
			return res;
		}
	}
}

