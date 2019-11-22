import pygame
import math
import numpy as np

pygame.font.init()
fuente = 30
largeText = pygame.font.Font('freesansbold.ttf', fuente)

def mover(pantalla, DH, color, ref, mag_eje):
    dibujar_ref(pantalla, ref, color, mag_eje)
    p = transformacion(pantalla, DH, color, ref)
    coordenadas = (p[0]-ref[0], -(p[1]-ref[1]))
    texto = str((round(coordenadas[0],2), round(coordenadas[1],2)))
    print 'Centro del efector final:', coordenadas
    TextSurf = largeText.render(texto, True, color[4])
    TextRect = TextSurf.get_rect()
    TextRect.center = (ref[0],(fuente/2))
    pantalla.blit(TextSurf, TextRect)


def transformacion(pantalla, DH, color, ref):
    DH_pinza_a = np.matrix([[0, -10, 0, math.pi/2], [0, 10, 0, 0]])
    DH_pinza_b = np.matrix([[0, 10, 0, math.pi/2], [0, 10, 0, 0]])
    DH_pinza_c = np.matrix([[1, 0, 0, 0], [0, 1, 0, 5], [0, 0, 1, 0], [0, 0, 0, 1]])
    # Rotar segmento
    inicio = ref
    T_1 = np.eye(4)
    articulaciones = np.size(DH,0)
    pinza_a = np.size(DH_pinza_a,0)
    pinza_b = np.size(DH_pinza_b,0)
    for i in range(articulaciones):
	T_pos, T_1 = DenavitHartenberg(DH, T_1,ref, i)
	pygame.draw.line(pantalla, color[i-1], inicio, T_pos, 3)
	inicio = T_pos

	if i == articulaciones - 1:
	    T_p1 = T_1
	    inicio_p = inicio
	    for j in range(pinza_a):
		T_pos_p, T_p1 = DenavitHartenberg(DH_pinza_a, T_p1,ref, j)
		pygame.draw.line(pantalla, color[0], inicio_p, T_pos_p, 3)
		inicio_p = T_pos_p

	    T_p1 = T_1
	    inicio_p = inicio
	    for j in range(pinza_b):
		T_pos_p, T_p1 = DenavitHartenberg(DH_pinza_b, T_p1,ref, j)
		pygame.draw.line(pantalla, color[0], inicio_p, T_pos_p, 3)
		inicio_p = T_pos_p

	    T_1 = np.dot(T_1,DH_pinza_c)
   	    T_pos = [ref[0]+T_1[0,3],ref[1]+T_1[1,3]]
	    pygame.draw.circle(pantalla, (255,255,0), [int(T_pos[0]),int(T_pos[1])], 3)

    return T_pos

def DenavitHartenberg(DH, T_1, ref, i):
    c_theta = math.cos(DH[i,3])
    s_theta = math.sin(DH[i,3])
    c_alfa = math.cos(DH[i,0])
    s_alfa = math.sin(DH[i,0])
    if DH[i,3] == math.pi or DH[i,3] == -math.pi:
	s_theta = 0
    a = DH[i,1]
    d = DH[i,2]
    T_f = np.matrix([[c_theta, -s_theta, 0, a], [s_theta*c_alfa, c_theta*c_alfa, -s_alfa, -s_alfa*d], [s_theta*s_alfa, c_theta*s_alfa, c_alfa, c_alfa*d], [0, 0, 0, 1]])
    T_1 = np.dot(T_1,T_f)
    T_pos = [ref[0]+T_1[0,3],ref[1]+T_1[1,3]]
    return T_pos, T_1

def dibujar_ref(pantalla, ref, color, mag_eje):
 
    # Borrar pantalla y dibujar marco de referencia
    fondo = pantalla.fill(color[3])
    pygame.draw.line(pantalla, color[4], ref, (ref[0]+mag_eje, ref[1]), 3)
    pygame.draw.line(pantalla, color[4], ref, (ref[0], ref[1]-mag_eje), 3)

def angulos(angulos_l,inicio):

    # Mover el primer segmento hasta llegar a su posicion final
    if angulos_l > inicio:
        grado = math.pi/180	   
    else:
        grado = -math.pi/180
   
    inicio += grado
    return inicio

def pedir_angulos(num_angulos):
    angulos = [0]*num_angulos
    for i in range(len(angulos)):
	texto = "Rotacion en radianes segmento {}: ".format(i+1)
	angulo = input(texto)
	while angulo > math.pi or angulo < -math.pi:
	    angulo = input('\nValor debe ser entre -pi y pi: ')
	angulos[i] = -angulo

    return angulos
