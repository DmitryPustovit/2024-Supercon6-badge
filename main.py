from machine import I2C, Pin
import time
from IRRemote import IRRemoteSAO

counter = 0

tv_remote_sao = None
health = 9
lastHealth = -1


def init_tv_remote_SAO(): 
    global tv_remote_sao
    if not tv_remote_sao:
        print("Trying to Init TV Remote SAO")
        try:
            tv_remote_sao_bus =  which_bus_has_device_id(0x08)[0]
            tv_remote_sao = IRRemoteSAO(tv_remote_sao_bus, 0x08, False, .1)
            tv_remote_sao.set_ir_mode(1)
            tv_remote_sao.set_ir_address(121)
            tv_remote_sao.clear_ir_receive_buffer()
        except:
            pass
    if not tv_remote_sao:
        print(f"Warning: TV Remote SAO not found.")

init_tv_remote_SAO()

## do a quick spiral to test
if petal_bus:
    for j in range(8):
        which_leds = (1 << (j+1)) - 1 
        for i in range(1,8):
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
            time.sleep_ms(30)
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
    

while True:
    if petal_bus:
        if lastHealth != health:
            lastHealth = health
            for i in range(health, 9):
                petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([0x00]))

    ## see what's going on with the touch wheel
    
    if tv_remote_sao:
        if touchwheel_bus:
            tw = touchwheel_read(touchwheel_bus)
            if (tw > 0):
                print("Fire!")
                tv_remote_sao.write_ir_data_byte(121, 4)
                time.sleep_ms(100)

        byte = tv_remote_sao.read_ir_byte()
        isHit = int.from_bytes(byte, 'big')

        if isHit == 4:
            print("Hit!")
            health -= 1
            print(health)


    ## display touchwheel on petal
    """
    if petal_bus and touchwheel_bus:
        if tw > 0:
            tw = (128 - tw) % 256 
            petal = int(tw/32) + 1
        else: 
            petal = 999
        for i in range(1,9):
            if i == petal:
                petal_bus.writeto_mem(0, i, bytes([0x7F]))
            else:
                petal_bus.writeto_mem(0, i, bytes([0x00]))
    """


    
    time.sleep_ms(100)
    bootLED.off()