import cv2 #openCV
import numpy as np

class Imagen:
	def __init__(self, archivo):
		self.__img = archivo
		self.__imResultante = np.zeros(self.__img.shape, self.__img.dtype)
	def mostrarImagenOriginal(self):
		cv2.imshow('imagen', self.__img)
		#cv2.waitKey(0)
	def mostrarImagenProcesada(self, resultado):
		cv2.imshow(resultado, self.__imResultante)
		cv2.waitKey(0)
	def obtenerImagenOriginal(self):
		return self.__img
	def obtenerImagenProcesada(self):
		return self.__imResultante
	def dilatar(self, ee):
		tamax=self.__img.shape[0]
		tamay=self.__img.shape[1]
		tam_ee=ee.shape
		tamasex=int(np.floor(tam_ee[0]/2))
		tamasey=int(np.floor(tam_ee[1]/2))
		Igray=np.zeros((tamax+2*tamasex, tamay+2*tamasey), np.uint8)
		Idilatada=np.zeros((tamax, tamay))
		if(len(self.__img.shape)==3):
			Irgbtogray=cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
		else:
			Irgbtogray=self.__img
		Igray[tamasex:tamasex+tamax, tamasey:tamasey+tamay]=Irgbtogray
		for x in range(tamasex, tamax+tamasex):
			for y in range(tamasey, tamay+tamasey):
				se_imagen = Igray[ (x-tamasex):(x+tamasex+1), (y-tamasey):(y+tamasey+1)].copy()
				se_imagen=(se_imagen)*ee
				maximo=(se_imagen).max()
				Idilatada[x-tamasex, y-tamasey]=maximo
		self.__imResultante = np.uint8(Idilatada)
	def erosionar(self, ee):
		tamax=self.__img.shape[0]
		tamay=self.__img.shape[1]
		tam_ee=ee.shape
		tamasex=int(np.floor(tam_ee[0]/2))
		tamasey=int(np.floor(tam_ee[1]/2))
		Igray=np.ones((tamax+2*tamasex, tamay+2*tamasey),np.uint8)*255
		Ierosionada=np.zeros((tamax, tamay))
		if(len(self.__img.shape)==3):
			Irgbtogray=cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
		else:
			Irgbtogray=self.__img
		Igray[tamasex:tamasex+tamax, tamasey:tamasey+tamay]=Irgbtogray
		for x in range(tamasex, tamax+tamasex):
			for y in range(tamasey, tamay+tamasey):
				se_imagen = Igray[ (x-tamasex):(x+tamasex+1), (y-tamasey):(y+tamasey+1)].copy()
				se_imagen=(se_imagen)*ee
				minimo=(se_imagen).min()
				Ierosionada[x-tamasex, y-tamasey]=minimo
		self.__imResultante = np.uint8(Ierosionada)

	def apertura(self, ee):
		self.erosionar(ee)
		Iero=self.obtenerImagenProcesada()
		self.__init__(Iero)
		self.dilatar(ee)
		self.mostrarImagenProcesada('Apertura')

	def cierre(self, ee):
		self.dilatar(ee)
		Idil=self.obtenerImagenProcesada()
		self.__init__(Idil)
		self.erosionar(ee)
		self.mostrarImagenProcesada('Cierre')


#Apertura metodo

I = cv2.imread('lena.jpg')
im = Imagen(I)
ee = np.ones((3,3), np.uint8)
im.apertura(ee)

#Cierre metodo
im2 = Imagen(I)
im2.cierre(ee)

'''
#Apertura
I = cv2.imread('lena.jpg')
ee = np.ones((3,3), np.uint8)
im = Imagen(I)
im.erosionar(ee)
Ie = im.obtenerImagenProcesada()
im = Imagen(Ie)
im.dilatar(ee)
Ia = im.obtenerImagenProcesada()
cv2.imshow('Apertura', Ia)

#Cierre
im2 = Imagen(I)
im2.dilatar(ee)
Id = im2.obtenerImagenProcesada()
im2 = Imagen(Id)
im2.erosionar(ee)
Ic = im2.obtenerImagenProcesada()
cv2.imshow('Cierre', Ic)
cv2.waitKey(0)
'''