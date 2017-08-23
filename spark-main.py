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
load_cmd2 = ("sudo openocd -f spark-ocd4.cfg").split()
load_cmd3 = ("sudo openocd -f spark-ocd5.cfg").split()

debug1 = open("debug1.log","wb")
debug2 = open("debug2.log","wb")
debug3 = open("debug3.log","wb")

# 
# def ListenForErrors():
# 	proc = Popen(monitorCommand.split(), stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True)
#
# 	while proc.poll() is None:
# 		print 'Reading output from monitor...'
# 		sleep(1)
# 		output = proc.stdout.read(1)
# 		print "Read Line: ",output
# 		if "Disconnect" in output:
# 			return True
#
# 	print 'Process is not running'
# 	return False

def isFixtureDone(fixtureNum):
        _file = ""
        rtn = NOT_DONE
        if fixtureNum == 1 :
                _file = "debug1.log"
        elif fixtureNum ==2:
                _file = "debug2.log"
        else:
                _file = "debug3.log"
        with open ( _file) as f:
                for line in f:
                        print(line, end = " ")
                        if "Error" in line:
                                print("got an error in debug file")
                                rtn= ERROR
                                break
                        elif "Verified OK" in line:
                                print("Process Succeeded!")
                                rtn =  GOOD
                                break
        if rtn == NOT_DONE:
                print("Didn't find success or error, so probably still chugging")
        return rtn

running1 = running2 = running3 = False
last1 = last2 = last3 = True
while True:
	# Look for the GPIO pin to go high indicating that the DUT is powered and we're ready to rock.
	pin1 = GPIO.input(18) #A1
	pin2 = GPIO.input(19) #A2
	pin3 = GPIO.input(20) #A3
	if pin1 == True and last1 == False:
		print('Loading To Fixture 1')
		time.sleep(.2)
		running1= True;
		openocd1 = subprocess.Popen(load_cmd1, stdout = debug1)
		time.sleep(1)
		isFixtureDone(1);
	if pin2 == True and last2 == False:
		print('Loading To Fixture 2')
		time.sleep(.2)
		running2= True;
		subprocess.Popen(load_cmd2, stdout = debug2)
		time.sleep(1)
		isFixtureDone(2);
	if pin3 == True and last3 == False:
		print('Loading To Fixture 3')
		time.sleep(.2)
		running3= True;
		subprocess.Popen(load_cmd3,stderr = debug3, stdout = debug3)
		time.sleep(1)
		isFixtureDone(3);
	last1 = pin1
	last2 = pin2
	last3 = pin3
