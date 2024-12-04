
#Aqui poneis el Docstring que querais
"""
Este codigo esta descrito en codigo c en el siguiente documento con licencia propia : https://www.printables.com/model/818975-compact-robot-arm-arduino-3d-printed/files
Este script de Python está diseñado para controlar la posición de las diferentes partes de un brazo robótico utilizando servos y potenciómetros. 
El objetivo principal es mapear las entradas de los potenciómetros a los motores de los servos, permitiendo el movimiento de las distintas partes del brazo.

Características principales:
1. **Control de Servos:** Los servos se controlan a través de señales  enviadas por el controlador de servos (PCA9685).
2. **Potenciómetros:** Los potenciómetros se utilizan para establecer la posición deseada de los servos (y, consecuentemente, de las partes del robot).
3. **Manejo del "gripper":** Se usa un botón para abrir y cerrar un "gripper" mecánico.

Flujo del código:
1. Importación de los módulos de python necesarios.
2. Definición de las variables globales utilizadas para configurar la señal PWM.
3. Asignación de potenciómetros a pines de entrada, y de motores a pines de salida.
4. Creación de señal PWM para posicionar el "gripper" en la posición inicial.
5. Función "moveMotor" para mapear las entradas de los potenciómetros a las salidas PWM de los servos.
6. Instrucción doctest para probar el funcionamiento del método "moveMotor", a partir del ejemplo de uso definido en el docstring.
7. Bucle de ejecución continuo donde la posición de las diferentes partes del robot se actualiza constantemente en base a los valores de los potenciómetros, y donde se escucha el estado de un botón (conectado a la entrada digital 7) para abrir o cerrar el "gripper".
"""
#import Wire 
#import Adafruit_PWMServoDriver 
import board    
import busio 
import Jetson.GPIO as GPIO
import adafruit_pca9685 
import time 
i2c = busio.I2C(board.SCL, board.SDA) 
from adafruit_servokit import Servokit
import doctest



#Declaro variables globales 
MIN_PULSE_WIDTH= 650 
MAX_PULSE_WIDTH= 2350 
FREQUENCY = 50 
#Instancio el Driver del controlador de servos 
pwm = adafruit_pca9685.PCA9685(i2c)
kit = Servokit(channels=16)






#Configuro el sETup
time.sleep(5) 
pwm.frequency = FREQUENCY 
GPIO.setmode(GPIO.BOARD) 

#hand = pwm.channels[0]

hand = adafruit_motor.servo.Servo(1)  #cualquiera de las dos 
wrist = adafruit_motor.servo.Servo(2)
elbow = adafruit_motor.servo.Servo(3)
shoulder = adafruit_motor.servo.Servo(4)
base = adafruit_motor.servo.Servo(5)

potWrist = adafruit_motor.servo.Servo(6)    # Asociar potenciómetros a pines de entrada
potElbow = adafruit_motor.servo.Servo(7)
potShoulder = adafruit_motor.servo.Servo(8)
potBase = adafruit_motor.servo.Servo(9)




pwm.setPWMFreq(FREQUENCY)
pwm.setPWM(32, 0, 90)  
pwm.begin()
GPIO.setup(7, GPIO.IN)        #channel tiene que ser un pin valido en jetson 

def moveMotor(controlIn, motorOut):
    """
    Controla un motor utilizando una señal PWM basada en la posición de un potenciómetro.

    :param controlIn: Entero representativo del pin de entrada asociado al potenciómetro correspondiente.
    :param motorOut: Entero representativo del pin de salida conectado al motor que se va a controlar.
    :return: No retorna ningún valor. 
    
    Ejemplo de uso:
    >>> moveMotor(potWrist, wrist)
    # Esto configurará el motor conectado al pin 2 (wrist) según la posición del potenciómetro en el pin 6 (potWrist).
    """

    pulse_wide, pulse_width, potVal = -7
    potVal = GPIO.input(controlIn)

    pulse_wide = map(potVal, 800, 240, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH)
    pulse_width = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096)                #Map Potentiometer position to Motor
  
    #pwm.setPWM(motorOut, 0, pulse_width);
    pwm.GPIO.PWM(motorOut, pulse_width)

# Ejecuta el ejemplo de uso
doctest.testmod()



while (True) :
    
    
    moveMotor(potWrist, wrist)

    moveMotor(potElbow, elbow)                                                      #Assign Motors to corresponding Potentiometers
    
    moveMotor(potShoulder, shoulder)
   
    moveMotor(potBase, base)
    
    
    
    pushButton = GPIO.input (7)
    if(pushButton == GPIO.LOW):

        pwm.setPWM(hand, 0, 180)                             #Keep Gripper closed when button is not pressed
        print("Grab")
    else:
        pwm.setPWM(hand, 0, 90)                              #Open Gripper when button is pressed
        print("Release")
  
GPIO.cleanup()
    















