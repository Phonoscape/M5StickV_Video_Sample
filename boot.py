import video, sensor, image, lcd, time, uos
from fpioa_manager import *

fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)

#
noname="no.txt"
basename="capture"
ext=".avi"
no = 1

while True:
    while True:
        img = sensor.snapshot()
        img.draw_string(img.width()//2-100,img.height()//2-4, "STOP", color=(0,0,255), scale=2,mono_space=False)
        lcd.display(img)

        if but_a.value() == 0:
            break

        if but_b.value() == 0:
            sensor.run(0)
            sys.extt()

    lcd.clear()

    print("Start")

    try:
        f = open("/sd/"+noname,"r")
        no = int(f.read())
        f.close()
    except:
        no = 1

    print(no)

    name = "/sd/" + basename + str(no) + ext
    v = video.open(name, record=1, interval=200000, quality=50)
    i = 0
    while True:
        img = sensor.snapshot()
        img_len = v.record(img)
#		lcd.draw_string(lcd.width()//2-100,lcd.height()//2-4, "REC", lcd.WHITE, lcd.RED)
        img.draw_string(img.width()//2-100,img.height()//2-4, "REC", color=(255,0,0), scale=2,mono_space=False)
        lcd.display(img)

        if but_a.value() == 0:
            break

    v.record_finish()
    print("Stop")

    lcd.clear()

    no = no + 1
    f = open("/sd/"+noname,"w")
    f.write(str(no))
    f.close()


