#Importacion de librerias
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.integrate import odeint
import matplotlib.animation as ani

"""
    Se declaran las constantes:
        P: total de la poblacion en Ecuador: 17.37 millones
        S0 : Suseptibles inicial = P -> 1 relacion a P total, 
        I0 : Infectados iniciales = 10 -> 5.757052389176741e-07 en relacion a P total
        R0: Recuperados iniciales = 0 -> 0
        K = 1/14 : en un rango de [0,1] con pasos de 1/14
        b : tiene un rango de [1.5,2.5] de acuerdo a OMS ó puede ser [1,5]
        dias : numero de dias 
        N = numero de datos para un intervalo de dias
        
"""
## definir los intervalos para Slide
k_range = [0, 1]
b_range = [1,5]
N = 100 #Puntos en las lineas
dias = 70 
t = np.linspace(0,dias,N)
k = 1/14
b = sum(b_range)/2 #Valor medio de b
# Valores iniciales de s, i, r
s0 = 1.0
i0 = 5.757052389176741e-07
r0 = 0
w0 = [s0, i0, r0] #pasar a una lista los valores iniciales.

"""
    Funciones
        model: retorna una lista con los valores:
            [ds/dt, di/dt, dr/dt]
        Donde:
            ds/dt = -b * s(t) * i(t)
            di/dt =  b * s(t) * i(t) - k*i(t)
            dr/dt =  k * i(t)
        Susceptibles    : s(t)
        Infectious      : i(t)
        Recovered       : r(t)
"""
#Funcion para crear las ecuaciones diferenciales
def model(w, t, b, k):
    return [-1 * b*w[0]*w[1], b*w[0]*w[1] - k*w[1], k*w[1]]

# Algoritmo

"""
    Se configura los componentes de la figura, agregando axis donde se va a graficar
    Slide para los valores de k,b 
    botones para resetear lo valores de los slide y para guardar la animacion
    Se inicializa la variable para la animacion de la grafica 
"""
   
## 
fig, axis = plt.subplots(1,1)
plt.suptitle("Modelación SIR para Covid-19 en Ecuador",fontsize=25,fontweight="heavy") #titulo de la grafica
### cambia el tamaño de letra en los ejes x y 'y'
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
axis.set_position((0.1,0.33,0.8,0.6)) # Cuadro de la grafica #izquierda,abajo,ancho,alto 

### Se configuran los Slider de k y b
k_ax = plt.axes((0.1,0.23,0.8,0.025),facecolor="aliceblue") 
k_sl = Slider(ax=k_ax,
              label="k",
              valmin=k_range[0],
              valmax=k_range[1],
              valinit= k,
              valstep=1/14,
              orientation="horizontal",
              color="steelblue")
b_ax = plt.axes((0.1,0.19,0.8,0.025),facecolor="aliceblue")
b_sl = Slider(ax=b_ax,
              label="b",
              valmin=b_range[0],
              valmax=b_range[1],
              valinit= b,
              valstep=0.02,
              orientation="horizontal",
              color="steelblue")
### Se configura los botones
animacion_ax = plt.axes((0.45,0.15,0.125,0.025),facecolor="aliceblue")
animacion_bt = Button(ax=animacion_ax,label="Guardar Animación")
reset_ax = plt.axes((0.45,0.11,0.125,0.025),facecolor="aliceblue")
reset_bt = Button(ax=reset_ax,label="Reiniciar")
# Cambiar el tamaño de la letra de los sliders
b_sl.label.set_fontsize(15)
k_sl.label.set_fontsize(15)
b_sl.valtext.set_fontsize(15)
k_sl.valtext.set_fontsize(15)

"""
    Gráfica.
"""
animator = ani.FuncAnimation(fig, lambda _ :0)  # Variable para la animación   

def animacion(y,t):          # Genera la animación.
    global animator
    animator.event_source.stop()     # Detiene la animación.
    axis.cla()                       # Se limpian los ejes. 
    axis.set_xlabel('tiempo (dias)', fontsize=16)
    axis.set_ylabel('Proporción de la población',fontsize=16)
    def buildmebarchart(i = int):  # Genera el gift.
        axis.plot(t[:i],y[:i,0],color="#1b9e77",lw=3,zorder=0,linestyle="--")  # Se grafica "s". 
        axis.plot(t[:i],y[:i,1],color="#d95f02",lw=3,zorder=0,linestyle="-")   # Se grafica "i". 
        axis.plot(t[:i],y[:i,2],color="#7570b3",lw=3,zorder=0,linestyle=":")   # Se grafica "r". 
        axis.legend(['Susceptibles','Infectados', 'Recuperados'],loc="best", title_fontsize="x-large")
        fig.canvas.draw_idle()
        # -------------------------------------------------------------
        if i == 150:          # Se detiene las iteraciones de "i". 
            animator.event_source.stop()
    
    animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)         # Se llama a "buildmebarchart()".

def generarGIFAnimacion(y, t):  # Guarda la animación.
    fig = plt.figure()          # Se genera una figura.
    plt.subplots_adjust(bottom = 0.2, top = 0.9)   # Dimensiones de la figura.
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor",)
    plt.suptitle("Covid - 19",fontsize=25,fontweight="heavy")    
    plt.ylabel('Proporción de la población',fontsize=13)
    plt.xlabel('tiempo (dias)',fontsize=13)
    def buildmebarchart(i=int):
        plt.plot(t[:i], y[:i,0],color="#1b9e77",lw=3,zorder=0,linestyle="--")  # Se grafica "s". 
        plt.plot(t[:i], y[:i,1], color="#d95f02",lw=3,zorder=0,linestyle="-")  # Se grafica "i".
        plt.plot(t[:i], y[:i,2], color="#7570b3",lw=3,zorder=0,linestyle=":")  # Se grafica "r".
        plt.legend(['Susceptibles','Infectados', 'Recuperados'],loc="best", title_fontsize="x-large")
    
    animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)         # Se llama a "buildmebarchart()".
    animator.save(r'covidSIRAnimacion.gif')     # Se guarda la animación.
    
def actualizarY():   # Actualiza los valores del eje "y".
    k = k_sl.val     # Actualiza "b".
    b = b_sl.val     # Actualiza "k".
    y  =  odeint(model, w0, t, args=(b,k))
    return y

def cambiaBK(val):  # Actualiza los valores de "b" y "k".
    y = actualizarY()
    animacion(y,t)
# Cambio de los Sliders "k_s1" y "b_s1".
k_sl.on_changed(cambiaBK)   # Para los cambios de "k".
b_sl.on_changed(cambiaBK)   # Para los cambios de "b".

def guardarAnimacion(env):  # Guarda la animación.
    y  =  actualizarY()
    generarGIFAnimacion(y, t)
animacion_bt.on_clicked(guardarAnimacion) # Al pulsar "Guardar Animación".

def reset(ev):      # Resetea los valores de los Sliders.
    b_sl.reset()
    k_sl.reset()
reset_bt.on_clicked(reset)  # Al pulsar "Reiniciar".

# Inicia el algoritmo
y  =  odeint(model, w0, t, args=(b,k))   # Se resuelven las ecuaciones diferenciales
animacion(y,t)                           # Graficación   

plt.show()
