import lgpio
import time

laser = 4
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, laser)

while True:
    if(lgpio.gpio_read(h, laser)):
        time.sleep(.01)
        print("detected")
        break

