import apa102
import time

class Pixels:
    PIXELS_N = 3

    def __init__(self):
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

    def setPixels(self):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, 0, 0, 200)
        self.dev.show()

    def off(self):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, 0, 0, 0)
        self.dev.show()


pixels = Pixels()
#
# if __name__ == '__main__':
#     while True:
#
#         try:
#             pixels.setPixels()
#             time.sleep(3)
#             pixels.off()
#             time.sleep(3)
#         except KeyboardInterrupt:
#             break
#
#     pixels.off()
#     time.sleep(1)
