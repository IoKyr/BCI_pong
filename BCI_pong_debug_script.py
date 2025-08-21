from controller_YOUR_NAME_HERE import CONTROLLER_NAME
from pong_code import PONG_GAME
from utils import init_connection, get_data_from_spikerbox

# SpikerBox Specifications (Cannot be changed)
b_rate = 230400

# Pong update rate
FPS = 30

# Set the correct port and baudrate, buffer size for the serial.
c_port_blue = 'COM3'

# Determines frequency of buffer filling up. 20000 = 1s.
SB_sampling_freq = 20000
input_buffer_size = int(SB_sampling_freq/FPS)
print(f"input_buffer_size: {input_buffer_size}")

# Set maximum time to read the buffer for. None for no timeout.
timeout = None

# geek1 == blue
ser_blue = init_connection(c_port_blue, b_rate, input_buffer_size, timeout)

controller_orange = CONTROLLER_NAME() #you can pass parameters that you'll need here

def main():
    pause = False
    running = True

    pong = PONG_GAME(FPS)

    while running:
        data_blue = get_data_from_spikerbox(ser_blue, input_buffer_size)

        # Event handling by EEG data
        cmnd_blue = controller_orange.decision(data_blue)
        if cmnd_blue == 1:
            geek1YFac = -1
        elif cmnd_blue == 0:
            geek1YFac = 1
        else:
            geek1YFac = 0

        running = pong.step_forward(geek1YFac, 0, pause)

    pong.quit()

if __name__ == "__main__":
    main()




