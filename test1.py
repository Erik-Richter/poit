import serial

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

while(True):
	read_ser = ser.readline().strip().decode("utf-8").split(',')
	
	distance = read_ser[0]
	obstacle = read_ser[1]
	print("Distance: ", distance)
	print("Obstacle: ", obstacle)
	print("")
	
	
	
	
