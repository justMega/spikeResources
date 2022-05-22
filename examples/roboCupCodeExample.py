from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import utime
import hub

pHub = PrimeHub()
hub_status = hub.status()

#definiraj motorje, senzorje
hub = PrimeHub()
motorpair = MotorPair("B", "A")
motorLevi = Motor("A")
motorDesni = Motor("B")
roka = Motor("E")
colorLevi = ColorSensor('C')
colorDesni = ColorSensor('D')
opeka = ForceSensor('F')
stevec =0
zeljenaVrednost = 80
kotNum =0


#variables here
#nej bojo vse poimenovane po istem principu 
zacetniCas = 0
motorDesni.set_stall_detection(True)
motorLevi.set_stall_detection(True)
arr=[0,0]

def sledenjeEnLevo():
    if (colorLevi.get_reflected_light() > zeljenaVrednost):
        motorpair.start_tank(-18, -20)
    else:
        napaka = zeljenaVrednost-colorLevi.get_reflected_light()
        motorpair.start_tank(-20, 45)

def sledenjeEnDesno():
    if (colorDesni.get_reflected_light() > zeljenaVrednost):
        motorpair.start_tank(-20, -18)
    else:
        napaka = zeljenaVrednost-colorLevi.get_reflected_light()
        motorpair.start_tank(45, -20)

def sledenjeEnDesnoTime(cas):
    zacetniCas = utime.time()
    while zacetniCas-utime.time() > -cas:
        sledenjeEnDesno()

def sledenjeEnLevoTime(cas):
    zacetniCas = utime.time()
    while zacetniCas-utime.time() > -cas:
        sledenjeEnLevo()

def simpleSledenje():
    if colorLevi.get_reflected_light() < 60: 
        motorLevi.start(30) 
        videlCrno = True
    else: 
        motorLevi.start(-10) 
    if colorDesni.get_reflected_light() < 60: 
        motorDesni.start(-30)
        videlCrno = True
    else: 
        motorDesni.start(10)

#smer je parameter ki je lahk sam "levo" al pa "desno"
def obrat(smer, deg=90):
    #dic is a dictionary 
    #želeno vrednost mapira drugi vrednosti - če dic["levo"] bo out put -1
    dic = {"levo":-1, "desno":1}
    motorpair.stop() 
    motorpair.move_tank(8.5, "cm", 10*dic[smer], -10*dic[smer])
    motorpair.stop()
    motorpair.stop()

def obratKrizisce(smer, sensor):
    dic = {"levo":-1, "desno":1}
    while sensor.get_color() != "black":
        motorpair.start_tank(10*dic[smer], -10*dic[smer])
    motorpair.move_tank(3.5, "cm", 10*dic[smer], -10*dic[smer])
    motorpair.stop()

def obratDveZeleni():
    while colorDesni.get_color() != "black":
        motorpair.start_tank(10, -10)
    motorpair.move_tank(10, "cm", 10, -10)
    motorpair.stop()

def memOpekeLevo():
    motorpair.move(5, "cm", 0, 20)
    #obrne 90s levo gre naprej pol obrne 90s desno gre napej obrne desno 90s
    obrat("levo", 90)
    motorpair.move(-17, "cm", 0, 20)
    obrat("desno", 90)
    motorpair.move(-35, "cm", 0, 20)
    obrat("desno", 90)
    #gre naprej dogkler sensor ne zazna črne
    while colorLevi.get_color() != "black":
        motorpair.start(0, -20)
    motorpair.stop() 
    #gre mal naprej se obrača v levo dokler sensor ne zazna črne v primeru da je uvinek in bi blo 90s preveč  
    motorpair.move(-2, "cm", 0, 20)
    while colorDesni.get_color() != "black":
        motorpair.start_tank(-20, 20) 

def memOpekeDesno():
    motorpair.move(5, "cm", 0, 20)
    #obrne 90s levo gre naprej pol obrne 90s desno gre napej obrne desno 90s
    obrat("desno", 90)
    motorpair.move(-17, "cm", 0, 20)
    obrat("levo", 90)
    motorpair.move(-35, "cm", 0, 20)
    obrat("levo", 90)
    #gre naprej dogkler sensor ne zazna črne
    while colorLevi.get_color() != "black":
        motorpair.start(0, -20)
    motorpair.stop()
    #gre mal naprej se obrača v levo dokler sensor ne zazna črne v primeru da je uvinek in bi blo 90s preveč
    motorpair.move(-2, "cm", 0, 20)
    while colorLevi.get_color() != "black":
        motorpair.start_tank(20, -20)

def dveCrni(prviCas, stevec):
    delta = prviCas - utime.time()
    prviCas = utime.time()
    if abs(delta) < 10:
        stevec += 1
    else:
        stevec = 0
    if stevec >= 10:
        motorpair.move(-5, "cm", 20, 20)
        stevec = 0
    return [prviCas, stevec]

nazajPoPo = 22
obrati = 4500

def prvo(smer):
    dic={"levo":-1, "desno":1}
    motorpair.move_tank(6, "cm", -10*dic[smer], 10*dic[smer])
    for i in range(3):
        roka.run_for_degrees(-obrati, 100)
        motorpair.start(0,10)
        if i ==0 and kotNum ==0:
            motorpair.move_tank(95, "cm", -5*dic[smer], 50)
            motorpair.stop()
        elif i ==2 and kotNum ==2:
            motorpair.move_tank(95, "cm", -5*dic[smer], 50)
            motorpair.stop()
        else:
            motorpair.move(130, "cm", 0, 50)
        motorpair.start(0,-10)
        roka.run_for_degrees(obrati, 100)
        motorpair.stop()
        motorpair.move_tank(nazajPoPo, "cm", 10, 10)
        motorpair.move_tank(8.5, "cm", 10*dic[smer], -10*dic[smer])
    motorpair.move_tank(20, "cm", 10, 10)
    motorpair.move_tank(8.5, "cm", 10*dic[smer], -10*dic[smer])
    roka.run_for_degrees(-obrati, 100)
    motorpair.move(130, "cm", 0, 50)
    motorpair.start(0,-10)
    roka.run_for_degrees(obrati, 100)
    motorpair.stop()

def zadnaSoba(smer1):
    dic = {"levo":-1, "desno":1}
    kotNum = 0
    zacKot = pHub.motion_sensor.get_yaw_angle()
    print(zacKot)
    while opeka.get_force_newton() < 3:
        motorpair.start(0, -50)
    if smer1 == "desno":
        motorpair.move_tank(80,"cm", -100,0)
    else:
        motorpair.move_tank(80,"cm",0,-100)
    motorpair.move_tank(3, "cm", -10, -10)
    motorpair.stop()
    if abs(pHub.motion_sensor.get_yaw_angle()-zacKot) > 10:
        print(pHub.motion_sensor.get_yaw_angle())
        kotNum = 0
        for i in range(3):
            motorpair.move(10, "cm", 0, 100)
            motorpair.move(-15,"cm",0,100)
        print("kot je")
    else:
        kotNum = 2

    print(kotNum)

    motorpair.move_tank(8, "cm", 10, 10)

    if kotNum == 0:
        prvo(smer1)
        motorpair.stop()
        motorpair.move(-130, "cm", -15*dic[smer1], 100)
        for i in range(10):
            motorpair.move(10, "cm", 0, 100)
            motorpair.move(-15,"cm",0,100)
        motorpair.move_tank(3,"cm", 10, 10)
        motorpair.move_tank(6, "cm", -10*dic[smer1], 10*dic[smer1])
        motorpair.move_tank(17, "cm", 10*dic[smer1], -10*dic[smer1])
        while colorDesni.get_color() != "green" and colorLevi.get_color() != "green":
            motorpair.start(-5*dic[smer1], -50)
    elif kotNum == 2:
        motorpair.move_tank(3, "cm", 10, 10)
        motorpair.move_tank(8.5, "cm", 10*dic[smer1], -10*dic[smer1])
        while colorDesni.get_color() != "green" and colorLevi.get_color() != "green":
            motorpair.start(-5*dic[smer], 50)
        motorpair.move_tank(3, "cm", 10, 10)
        motorpair.move_tank(8.5, "cm", 10*dic[smer1], -10*dic[smer1])
        motorpair.move(130, "cm", 0, 100)
        prvo(smer1)
        motorpair.stop()
        motorpair.move(-130, "cm", -15*dic[smer1], 100)
        for i in range(10):
            motorpair.move(10, "cm", 0, 100)
            motorpair.move(-15,"cm",0,100)
        motorpair.move_tank(3, "cm", 10, 10)
        motorpair.move_tank(3, "cm", -10*dic[smer1], 10*dic[smer1])
        motorpair.move_tank(17, "cm", 10*dic[smer1], -10*dic[smer1])
        motorpair.move(130, "cm", 0, 100)
        motorpair.move_tank(3, "cm", 10, 10)
        motorpair.move_tank(8.5, "cm", 10*dic[smer1], -10*dic[smer1])
        while colorDesni.get_color() == "green" and colorLevi.get_color() == "green":
            motorpair.start(-5*dic[smer1], -50)
        motorpair.stop()

while 1:
    print(opeka.get_force_newton())
    simpleSledenje()
    #if (colorDesni.get_color() == "green" and colorLevi.get_color() == "green"):
    #    motorpair.move(-6, "cm", 0, 20)
    #    obratDveZeleni()
    if (colorDesni.get_color() == "green" and zacetniCas-utime.time() < -2):
    #    print("desni")
    #    while colorLevi.get_color() == "white":
    #        motorLevi.start(-50)
    #    motorLevi.stop()
    #    if colorLevi.get_color() != "green":
        motorpair.move(-6, "cm", 0, 20)
        obratKrizisce("desno", colorDesni)
        sledenjeEnLevoTime(1)
        zacetniCas = utime.time()
    elif (colorLevi.get_color() == "green" and zacetniCas-utime.time() < -2):
    #    print("Levi")
    #    while colorDesni.get_color() == "white":
    #        motorDesni.start(50)
    #    motorDesni.stop()
    #    if colorDesni.get_color() != "green":
        motorpair.move(-5, "cm", 0, 20)
        obratKrizisce("levo", colorLevi)
        sledenjeEnDesnoTime(1)
        zacetniCas = utime.time()
    elif opeka.is_pressed():
        motorpair.stop()
        if stevec == 0:
            memOpekeLevo()
        elif stevec == 1:
            memOpekeDesno()
        else: 
            zadnaSoba("levo")
        stevec += 1
    elif abs(hub.motion_sensor.get_pitch_angle()) > 15 and zacetniCas-utime.time() < -2:
        motorpair.move(10, "cm", 0, -100)
        zacetniCas = utime.time()
    elif (colorDesni.get_color() == "red" or colorDesni.get_color()=="violet") and (colorLevi.get_color() == "red" or colorLevi.get_color() == "violet"):
        break
    #elif colorDesni.get_color() == "black" and colorLevi.get_color() == "black":
    #    arr = dveCrni(arr[0],arr[1])
    #    print(arr)
    
    
