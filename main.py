import machine, time, max7219, mpu6050

spi = machine.SPI(-1, 10000000, miso=machine.Pin(2), mosi=machine.Pin(13), sck=machine.Pin(14))
display = max7219.Matrix8x8(spi, machine.Pin(12))
display.fill(0)
display.brightness(1)
display.show()

m = mpu6050.MPU(scl=22,sda=21,intr=16,d=display)
while not m.calibrated:
    m.calibrate()

acx, acy, acz, seq, gx, gy, gz = 0, 0, 0, 0, 0, 0, 0

starttime = int(time.time())

while True:

    try:
        acx, acy, acz, seq, gx, gy, gz = m.read_sensors_scaled()
    except:
        pass
    if sum([abs(x) for x in [acx, acy, acz, gx, gy, gz]]) > 50:
        starttime = int(time.time())

    seconds = int(time.time()) - starttime
    hrs = '%02d' % (seconds / 3600)
    mins = '%02d' % ((seconds % 3600) / 60)
    secs = '%02d' % (seconds % 60)
    clock = '%s.%s.%s' % (hrs, mins, secs)
    display.nprint(clock)
    #display.dot(2, seconds % 2)
    display.show()

    time.sleep(0.1)
