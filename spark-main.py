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

global debug1
global debug2
global debug3
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

def programFixture(fixtureNum, numTries):
	global debug1
	global debug2
	global debug3
	if fixtureNum == 1:
		print('Loading To Fixture 1')
		debug1.close()
		debug1 = open("debug1.log","wb")
		subprocess.Popen(load_cmd1, stderr = debug1, stdout = debug1)
	if fixtureNum == 2 : 
		print('Loading To Fixture 2')
		debug2.close()
		debug2 = open("debug2.log","wb")
		subprocess.Popen(load_cmd2, stderr = debug2, stdout = debug2)
	if fixtureNum == 3 :
		print('Loading To Fixture 3')
		debug3.close()
		debug3 = open("debug3.log","wb")
		subprocess.Popen(load_cmd3, stderr = debug3, stdout = debug3)

	time.sleep(4)
	result = isFixtureDone(fixtureNum)
	if numTries == 0:
                print("**************** We've blown our load tring to program this thing :(")
	elif result == ERROR:
		numTries = numTries - 1
		programFixture(fixtureNum , numTries)
	else :
		print("***********Done with Fixture!");
	
def isFixtureDone(fixtureNum):
	parse_file = ""
	file_obj = "";
	rtn = NOT_DONE
	global debug1
	global debug2
	global debug3
	if fixtureNum == 1 :
		parse_file = "debug1.log"
		file_obj = debug1
	elif fixtureNum ==2:
		parse_file = "debug2.log"
		file_obj = debug2
	else:
		parse_file = "debug3.log"
		file_obj = debug3
	with open ( parse_file) as f:
		for line in f:
			print(line, end = "/")
			if "Error: init mode failed" in line:
				print("****got an error in debug file")
				rtn= ERROR
				
			elif "** Programming Started **" in line:
				print("Programming started!")
				rtn =  GOOD
				
	if rtn == NOT_DONE:
		print("Didn't find success or error, so probably still chugging")
	return rtn

def initLogs():
	global debug1
	global debug2
	global debug3
	debug1 = open("debug1.log","wb")
	debug2 = open("debug2.log","wb")
	debug3 = open("debug3.log","wb")

running1 = running2 = running3 = False
last1 = last2 = last3 = True
default_num_tries = 4
initLogs()

while True:
	
	# Look for the GPIO pin to go high indicating that the DUT is powered and we're ready to rock.
	pin1 = GPIO.input(18) #A1
	pin2 = GPIO.input(19) #A2
	pin3 = GPIO.input(20) #A3
	if pin1 == True and last1 == False:
				time.sleep(1)
				programFixture(1, default_num_tries)
	if pin2 == True and last2 == False:
				time.sleep(1)
				programFixture(2, default_num_tries)
	if pin3 == True and last3 == False:
				time.sleep(1)
				programFixture(3, default_num_tries)
	last1 = pin1
	last2 = pin2
	last3 = pin3
