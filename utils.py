import numpy as np
import serial

def process_byte_data(b_data):
    """
    Converts the weird data from SpikerBox to list of amplitude measurements.

    Data from SpikerBox uses two bytes for a single unit of data. Hence returned array with be ~1/2 the size of the
    passed array.
    """
    data_raw = np.array(b_data)
    data_processed = np.zeros(0)

    i = 0
    while i < len(data_raw) - 1:

        if data_raw[i] > 127:
            # Found beginning of frame. Extract one sample from two bytes.
            int_processed = (np.bitwise_and(data_raw[i], 127)) * 128
            i += 1
            int_processed += data_raw[i]
            # Allocates, fills and returns new array. Likely inefficient.
            data_processed = np.append(data_processed, int_processed)

        i += 1

    return data_processed

def get_data_from_spikerbox(ser, input_buffer_size):
    # Read data from SpikerBox into a buffer of size input_buffer_size.
    byte_data = ser.read(input_buffer_size)
    # byte_data_blue = ser_orange.read(input_buffer_size)
    # Cast to list of ints.
    byte_data = [int(byte_data[i]) for i in range(len(byte_data))]
    # Process with above function.
    data = process_byte_data(byte_data)
    return data

def init_connection(c_port, b_rate, input_buffer_size, timeout):
    try:
        ser_orange = serial.Serial(port=c_port, baudrate=b_rate)
        ser_orange.set_buffer_size(rx_size=input_buffer_size)
        ser_orange.timeout = timeout
    except serial.serialutil.SerialException:
        raise Exception(
            f'Could not open port {c_port}.\nFind port from:\nDevice Manager > Ports (COM & LPT) [Windows]')