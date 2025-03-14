import numpy as np

def float_to_int8(float_value, min_value=-1.0, max_value=1.0):
    """
    Converts a 32-bit float to an 8-bit integer, scaling and clipping the value.

    Args:
        float_value (float): The 32-bit float value to convert.
        min_value (float, optional): The minimum possible value of the float. Defaults to -1.0.
        max_value (float, optional): The maximum possible value of the float. Defaults to 1.0.

    Returns:
        int: The 8-bit integer representation of the float value.
    """
    # Scale the float value to the range 0-255
    scaled_value = float(float_value - min_value) / float(max_value - min_value) * 255.

    # Clip the scaled value to the range 0-255
    clipped_value = np.clip(scaled_value, 0., 255.)

    # Convert to 8-bit integer
    int8_value = int(clipped_value)

    return int8_value

# Example usage:
float_val = 0.5
int8_val = float_to_int8(float_val)
print(f"Original float value: {float_val}")
print(f"Converted 8-bit integer value: {int8_val}")

# Example with numpy array
float_array = np.array([-0.5, 0.0, 0.5, 1.0], dtype=np.float32)
print(float_array)
print(float_to_int8(float_array[0]))
int8_array = np.array([float_to_int8(x) for x in float_array], dtype=np.uint8)
print(f"Original float array: {float_array}")
print(f"Converted 8-bit integer array: {int8_array}")