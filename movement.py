from sense_hat import SenseHat
import emailSender

def movement_detection():
	
	sense = SenseHat()
	red = (255, 0, 0)
	
	while True:
		acceleration = sense.get_accelerometer_raw()
		x = acceleration['x']
		y = acceleration['y']
		z = acceleration['z']

		x = abs(x)
		y = abs(y)
		z = abs(z)

		if x > 1 or y > 1 or z > 1:
			try:
				emailSender.sendEmailAlert("The camera has been moved.")
			except:
				print("Can't send email. ")
		else:
			sense.clear()