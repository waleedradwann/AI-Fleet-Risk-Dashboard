import serial

esp32 = serial.Serial(
    '/dev/cu.usbserial-1110',
    115200
)

while True:

    data = esp32.readline().decode().strip()

    values = data.split(",")

    if len(values) == 3:

        x = int(values[0])
        y = int(values[1])
        z = int(values[2])

        print(f"X={x} | Y={y} | Z={z}")

        movement = abs(x) + abs(y)

        if movement > 15000:

            print("HARSH MOVEMENT DETECTED")