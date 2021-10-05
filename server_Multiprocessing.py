import csv

import multiprocessing
import socket

import numpy as np
import tensorflow as tf
import keras
from keras.models import load_model
import time

#-----------------------------------------------------------------------


def tratasock(data):

	portsx, inputsx = data.split(',') #agora como string, divide o dado (port, inputs)

	portsx = portsx.replace('"',"") #remove os aspas e parenteses nos dados abaixo do ports pois o dado chega "[porta1, porta2]"
	portsx = portsx.replace('[',"")
	portsx = portsx.replace(']',"")
	portsx1 , portsx2 = portsx.split()
	portsy = np.array([[portsx1, portsx2]], dtype='f') #remonta o dado com o np.array
                        
	inputsx = inputsx.replace('"',"") #remove os aspas e parenteses nos dados abaixo do inputs pois o dado chega "[inputs1, inputs...]"
	inputsx = inputsx.replace('[',"")
	inputsx = inputsx.replace(']',"")
	inputsx1, inputsx2, inputsx3, inputsx4, inputsx5, inputsx6, inputsx7, inputsx8, inputsx9, inputsx10, inputsx11, inputsx12, inputsx13, inputsx14, inputsx15, inputsx16, inputsx17, inputsx18, inputsx19, inputsx20, inputsx21, inputsx22, inputsx23, inputsx24, inputsx25, inputsx26, inputsx27, inputsx28, inputsx29, inputsx30 = inputsx.split()
                        
	inputsy = np.array([[inputsx1, inputsx2, inputsx3, inputsx4, inputsx5, inputsx6, inputsx7, inputsx8, inputsx9, inputsx10, inputsx11, inputsx12, inputsx13, inputsx14, inputsx15, inputsx16, inputsx17, inputsx18, inputsx19, inputsx20, inputsx21, inputsx22, inputsx23, inputsx24, inputsx25, inputsx26, inputsx27, inputsx28, inputsx29, inputsx30]], dtype='f') #remonta o dado com o np.array
	x = portsy, inputsy
	#print(x)
	return(x)


#-----------------------------------------------------------------------
#https://github.com/mmge88/IoT_DL-based_Intrusion_Detection/blob/main/iot_botnet_2_percent_embedding.ipynb
def callmodel(x):



	model = tf.keras.models.load_model('DLModel1.h5', compile=False)
	model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

	portsx , inputsx = x
	xpto = model.predict({'ports': portsx, 'others': inputsx})
	print()
	print(xpto)
	print()


#-----------------------------------------------------------------------
#https://gist.github.com/micktwomey/606178

def handle(connection, address):

	def monitor(x,y):

		name = "monitoringTime.csv"
		f = open(name, 'a')
		try:
			writer = csv.writer(f) 
			writer.writerow((x,y))
		finally:
			f.close()        
             

	try:

		data = connection.recv(2048).decode('UTF-8')
		data = tratasock(data)

		x = time.time() ### VERIFICAR TIME.TIME() OU DATETIME.DATETIME.NOW()
		callmodel(data)
		y = time.time()
		monitor(x,y)
			
	except:
		print("Problem handling request")
	finally:
		print("Closing socket")
		connection.close()

#-----------------------------------------------------------------------

class Server(object):
	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

	def start(self):
		print("listening")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ###TCP
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1)
		self.lista = []

		while True:
			conn, address = self.socket.accept()
			#print("Got connection")
			process = multiprocessing.Process(target=handle, args=(conn, address))
			process.daemon = True
			process.start()
			print()
			#print("Started process %r", process)

	def stop(self):
		self.socket.close




#-----------------------------------------------------------------------


if __name__ == "__main__":
	
	server = Server("", 9000)
	#criarCSV()

	try:
		#print("Listening")
		server.start()

	except:
		print("Unexpected exception")
	finally:
		for process in multiprocessing.active_children():
			print("Shutting down process %r", process)
			process.terminate()
			process.join()
	print("All done")







