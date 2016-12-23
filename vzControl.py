# Made by Vilhelm Prytz 2016.
# Email: vilhelm@prytznet.se
#
# Release 1.1.
version = "1.1"
# https://github.com/MrKaKisen/Python-Powered-OpenVZ-Container-Controller
import subprocess

def getStatus(CTID):
        print("CT IS RUNNING.")
        print("CPU USAGE:")
        #p = subprocess.Popen(["vzctl", "exec", str(CTID), "cat", "/proc/loadavg"])
        loadAvg = subprocess.check_output(["vzctl", "exec", str(CTID), "cat", "/proc/loadavg"])
        print(loadAvg)
        print("UPTIME:")
        uptimeGet = subprocess.check_output(["vzctl", "exec", str(CTID), "uptime"])
        print(uptimeGet)

def createCT(CTID):
	newID = raw_input("Enter new ID: ")
	newIP = raw_input("Enter new IP for CT: ")
	newHostname = raw_input("Enter new hostname for CT: ")
	newOSTemplate = raw_input("Enter the OS name (template): ")
	newRootPassword = raw_input("Enter new root password: ")
	newRAM = raw_input("Enter new amount of RAM (in G or M format): ")
	newSWAP = raw_input("Enter new amount of SWAP (in G or M format): ")
	newCPU = raw_input("Enter new amount of CPUs: ")
	newDisk = raw_input("Enter new amount of disk (with G): ")
	print("-------------------------")
	print("Information collected.")
	proceedAsk = raw_input("Proceed y/n?: ")
	if (proceedAsk == "y" or proceedAsk == "Y" or proceedAsk == "j" or proceedAsk == "J"):
		print("Doing stuff. This might take a while!")
		nullRoute = subprocess.check_output(["vzctl", "create", newID, "--ostemplate", newOSTemplate])
		nullRoute = subprocess.check_output(["vzctl", "set", newID, "--diskspace", newDisk + ":" + newDisk, "--save"])
		nullRoute = subprocess.check_output(["vzctl", "set", newID, "--ipadd", newIP, "--nameserver", "8.8.8.8", "--ram", newRAM, "--swap", newSWAP, "--cpus", newCPU, "--save"])
		nullRoute = subprocess.check_output(["vzctl", "set", newID, "--hostname", newHostname, "--save"])
		nullRoute = subprocess.check_output(["vzctl", "set", newID, "--userpasswd", "root" + ":" + newRootPassword, "--save"])
		print("Settings set. Booting CT.")
		nullRoute = subprocess.check_output(["vzctl", "start", newID])
		print("Booted!")
		print("vzcontrol changed to " + newID)
		CTID = newID
	else:
		print("Aborting")
	return CTID

print("Welcome to VZ control by Vilhelm Prytz. Version: " + version)
print("1 - Control Existing CT")
print("2 - Create new CT")
toDo = raw_input("Enter 1 or 2: ")
if toDo == "1":
	CTID = raw_input("Input CT ID to control: ")
elif toDo == "2":
	print("Launching create new CT script")
	print("-------------------------------")
	CTID = "0"
	CTID = createCT(CTID)
else:
	print("Invalid option. Controlling existing CT.")
	CTID = raw_input("Input CT ID to control: ")
print("Current status:")
print("----------------------------")
powerStatus = subprocess.check_output(["vzctl", "status", str(CTID)])
if (powerStatus == "CTID " + str(CTID) + " exist mounted running" + "\n"):
	getOtherStatus = True
	getStatus(CTID)
else:
	getOtherStatus = False
	print("CT IS NOT RUNNING, NO STATUS DISPLAYED")

exitCode = False
while exitCode is False:
	print("----------------------------")
	print("Controlling CT: " + str(CTID))
	powerStatus = subprocess.check_output(["vzctl", "status", str(CTID)])
	if (powerStatus == "CTID " + str(CTID) + " exist mounted running" + "\n"):
		print("--- CT IS RUNNING!")
	else:
		print("--- CT IS OFFLINE!")
	print("exit - Exit this program")
	print("0 - Create CT")
	print("1 - Stop CT")
	print("2 - Start CT")
	print("3 - Display status")
	print("4 - Change root password")

	actionDo = raw_input("Input action: ")

	if (actionDo == "exit"):
		exitCode = True
		exit(0)
	
	if (actionDo == "0"):
		CTID = createCT(CTID)
	if (actionDo == "1"):
		print("Stopping CT")
		nullRoute = subprocess.check_output(["vzctl", "stop", str(CTID)])
		print("Done")
	if (actionDo == "2"):
		print("Starting CT")
		nullRoute = subprocess.check_output(["vzctl", "start", str(CTID)])
		print("Done")
	if (actionDo == "3"):
		powerStatus = subprocess.check_output(["vzctl", "status", str(CTID)])
		if (powerStatus == "CTID " + str(CTID) + " exist mounted running" + "\n"):
			getStatus(CTID)
		else:
			print("CT IS NOT RUNNING, NO STATUS DISPLAYED")
	if (actionDo == "4"):
		print("Changing password for root")
		newPassword = raw_input("New root password for (" + CTID + "): ")
		nullRoute = subprocess.check_output(["vzctl", "set", CTID, "--userpasswd", "root" + ":" + newPassword, "--save"])
		print("Password changed!")
	else:
		print("Command not found.")
#p = subprocess.Popen(["vzctl", "stop", "623"])
