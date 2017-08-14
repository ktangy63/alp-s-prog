import RPi.GPIO as GPIO
import time
import subprocess

ERROR = 0
GOOD = 1
NOT_DONE = 2

print('Starting up spark-main')
print('V1.0 Aug 14')

GPIO.setmode(GPIO.BCM)

# Set up our pulldowns b/c we are looking for the power to turn on to the DUT
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

load_cmd1 = ("sudo openocd -f spark-ocd1.cfg").split()
load_cmd2 = ("sudo openocd -f spark-ocd2.cfg").split()
load_cmd3 = ("sudo openocd -f spark-ocd3.cfg").split()

debug1 = open("debug1.log","w")
debug2 = open("debug2.log","w")
debug3 = open("debug3.log","w")

def isFixtureDone(fixtureNum):
	file = ""
	rtn = NOT_DONE
	if fixtureNum == 1:
		file = debug1
	elif fixtureNum ==2:
		file = debug2
	else:
		file = debug3
	lines = debug1.readlines()
	for i, line in enumerate(lines):
		if "Error" in line:
			print("got an error in debug file")
			rtn= ERROR
			break
		elif "Verified OK" in line:
			print("Process Succeeded!")
			rtn =  GOOD
			break
#	if rtn == NOT_DONE:
#		print("Didn't find success or error, so probably still chugging")
	return rtn
while True:
	# Look for the GPIO pin to go high indicating that the DUT is powered and we're ready to rock.
	pin1 = GPIO.input(18) #A1
	pin2 = GPIO.input(19) #A2
	pin3 = GPIO.input(20) #A3
	if pin1 == True and last1 == False:
		print('Loading To Fixture 1')
		openocd1 = subprocess.Popen(load_cmd1, stdout = debug1)
		time.sleep(.2)
	if pin2 == True and last2 == False:
		print('Loading To Fixture 2')
		subprocess.Popen(load_cmd2, stdout = debug2)
		time.sleep(.2)
	if pin3 == True and last3 == False:
		print('Loading To Fixture 3')
		subprocess.Popen(load_cmd3, stdout = debug3)
		time.sleep(.2)
	last1 = pin1
	last2 = pin2
	last3 = pin3
