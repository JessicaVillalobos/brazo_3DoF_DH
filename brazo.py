import pygame
import math
import Tr
import numpy as np

def main():
    
    # Inicializar modulo pygame
    pygame.display.init()
    pygame.display.set_caption("Brazo 3DoF")
    
    # Medidas de la pantalla
    ancho_pantalla = 500
    alto_pantalla = 500

    # Crear superficie en la pantalla
    pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))

    # Control del ciclo main
    nueva_funcion = True
    
    # Definir marco de referencia
    cero = (ancho_pantalla/2, alto_pantalla/2)
    mag_eje = 10
    eje_x = (cero[0]+mag_eje, cero[1])
    eje_y = (cero[0], cero[1]-mag_eje)

    colores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
    angulos = [0, 0, 0]
    fps = 30
    clock = pygame.time.Clock()
    grado = math.pi/180
    # Dibujar brazo en posicion inicial (segmentos y ejes)
    fondo = pantalla.fill(colores[3])
    DH = np.matrix([[0, 0, 0, 0], [0, 100, 0, 0], [0, 50, 0, 0], [0, 25, 0, -math.pi/2]])

    Tr.mover(pantalla, DH, colores, cero, mag_eje)
    pygame.display.update()
    regresar = False

    # Ciclo main
    while 1:
        if nueva_funcion:

            # Mover brazo y actualizar angulos iniciales
	    if regresar:
	        angulos = [0, 0, 0]
	    else:
	    	angulos = Tr.pedir_angulos(len(angulos))
	    for i in range(len(angulos)):
	        if not regresar:
		    k = i
	        else:
		    k = len(angulos) - 1 - i
   	        error = abs(angulos[k] - DH[k,3])
	        while error > grado:
    	            # Calcular y dibujar las rotaciones
    	            DH[k,3] = Tr.angulos(angulos[k], DH[k,3])
		    Tr.mover(pantalla, DH, colores, cero, mag_eje)
		    error = abs(angulos[k] - DH[k,3])
		    pygame.display.update()
		    clock.tick(fps)

		# Calcular y dibujar las rotaciones finales
	        DH[k,3] = angulos[k]
	    	Tr.mover(pantalla, DH, colores, cero, mag_eje)
	    	pygame.display.update()

	    if not regresar:
	        nueva_funcion = input('\nAngulos nuevos: \
		                \n0) No \
			        \n1) Si \n')

	        while nueva_funcion > 1 or nueva_funcion < 0:
		    nueva_funcion = input('\nNo existe la opcion elegida. \
			        \n Angulos nuevos:\
			        \n0) No \
			        \n1) Si \n')
	    

	        # Salir del programa 
	        if not nueva_funcion:
	            pygame.quit()
		    exit()
	        else:
		    regresar = True
	    else:
		regresar = False
	
    

if __name__=="__main__":
    # llamar a la funcion main
    main()
