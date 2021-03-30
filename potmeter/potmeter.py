import serial

#arduino object with port, baud rate and timeout specified
arduino = serial.Serial('COM4',9600,timeout=.1)

def angle():
    while(True):
        data = arduino.readline()[:-1]
        #decode the data
        decoded_data = str(data,'utf-8')
        print(decoded_data)
        #grabs the first 3 symbols
    return decoded_data


angle()
