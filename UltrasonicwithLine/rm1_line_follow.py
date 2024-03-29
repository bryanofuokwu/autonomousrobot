from __future__ import division
import time
#import the PCA9685 module.
import osoyoo_PCA9685
import RPi.GPIO as GPIO
#L298N port define
ena = 8
enb = 13
in1 = 9
in2 = 10
in3 = 11
in4 = 12
lf1,lf2,lf3,lf4,lf5=0,0,0,0,0
#from left to right ,three tracking sensors are connected to BCM17,BCM27 and BCM22
lleft = 5
lsensor = 6
msensor = 13
rsensor = 19
rright = 26
high_speed=1400
mid_speed=1200
low_speed=900
turn_speed=1700
# Initialise the PCA9685 using the default address (0x40).
pwm = osoyoo_PCA9685.PCA9685()
# Set frequency to 60hz.
pwm.set_pwm_freq(60)
#Initialise GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lsensor,GPIO.IN)
GPIO.setup(msensor,GPIO.IN)
GPIO.setup(rsensor,GPIO.IN)
GPIO.setup(lleft,GPIO.IN)
GPIO.setup(rright,GPIO.IN)
# Read tracking senbsors's data
def read_sensors():
    global lf1,lf2,lf3,lf4,lf5
    lf1 = abs(GPIO.input(lleft))
    lf2 = abs(GPIO.input(lsensor))
    lf3 = abs(GPIO.input(msensor))
    lf4 = abs(GPIO.input(rsensor))
    lf5 = abs(GPIO.input(rright))
#Set motor speed
def set_speed(lspeed,rspeed):
    pwm.set_pwm(ena,0,lspeed)
    pwm.set_pwm(enb,0,rspeed)

#Robot car forward
def go_forward():
    pwm.set_pwm(in1,0,4095)   #IN1
    pwm.set_pwm(in2,0,0)      #IN2
    
    pwm.set_pwm(in3,0,4095)   #IN3
    pwm.set_pwm(in4,0,0)      #IN4
#Robot car backwards
def go_back():
    pwm.set_pwm(in1,0,0)      #IN1
    pwm.set_pwm(in2,0,4095)   #IN2
    
    pwm.set_pwm(in3,0,0)      #IN3
    pwm.set_pwm(in4,0,4095)   #IN4

#Robot car turn left
def turn_left():
    pwm.set_pwm(in1,0,4095)   #IN1
    pwm.set_pwm(in2,0,0)      #IN2
    
    pwm.set_pwm(in3,0,0)      #IN3
    pwm.set_pwm(in4,0,4095)   #IN4

#Robot turn right
def turn_right():
    pwm.set_pwm(in1,0,0)      #IN1
    pwm.set_pwm(in2,0,4095)   #IN2
    
    pwm.set_pwm(in3,0,4095)   #IN3
    pwm.set_pwm(in4,0,0)      #IN4

#Robot stop move
def stop():
    set_speed(0,0)

#Reset PCA9685's all channels    
def destroy():
    pwm.set_all_pwm(0,0)

#Robot car moves along the black line
def tracking():
    while True:
        read_sensors()
	set_speed(0,0)
        lf=str(lf1)+str(lf2)+str(lf3)+str(lf4)+str(lf5)
        print lf
        if(lf=='00000'):
	    set_speed(high_speed,high_speed)
	    go_forward()
            continue            
        if(lf=='01000' or lf=='01100' or lf=='10000' or lf=='10100' or lf=='11000' or lf=='11100'):
	    set_speed(turn_speed,turn_speed)
	    turn_right()
            continue
        if(lf=='00001' or lf=='00010' or lf=='00011' or lf=='00101' or lf=='00110' or lf=='00111'):
	    set_speed(turn_speed,turn_speed)
	    turn_left()
            continue
	if(lf=='10001' or lf=='10101'  or lf=='11001' or lf=='10011'):
            stop()
if __name__ == '__main__':
    try:
	#start to line follow
        tracking()
    except KeyboardInterrupt:
	#robot car stop
        destroy()

