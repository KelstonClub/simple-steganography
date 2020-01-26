from PIL import Image

#
# Open an image and pull out uncompressed
# pixel data, checking that the number of
# pixels is equals to the "pixel area" of
# the image
#
dragon = Image.open("dragon.jpg")
data = dragon.getdata()

## b_with_0_last_bit = b & 0xfe
## b_with_1_last_bit = b | 1

#
# Get the colours of the top-left pixel
#
r, g, b = data.getpixel((0, 0))
#
# Set the last bit of b to zero
#
b &= 0xfe
data.putpixel((0, 0), (r, g, b))

#
# Get the colours of the next pixel
#
r, g, b = data.getpixel((1, 0))
#
# Set the last bit of b to 1
#
b |= 1
data.putpixel((1, 0), (r, g, b))

#
# Put the updated data back into the image
# and save it under a different name
#
dragon.putdata(data)
dragon.save("dragon2.jpg")

def message_as_bits(message):
    #
    # Turn a message into a list of bytes where
    # each byte is a tuple of bits
    #
    message = "Hello, world!"
    message_bytes = bytes(message, encoding="ascii")
    message_bits = []
    for byte in message_bytes:
        bits = []
        for b in range(8):
            bits.append(byte & 1)
            byte = byte >> 1
        message_bits.append(tuple(bits[::-1]))

    return message_bits

def blue_final_bit(rgb, bit):
    r, g, b = rgb
    if bit:
        b |= 0b00000001
    else:
        b &= 0b11111110
    return r, g, b

def encoded(image, message):
    data = image.getdata()
    message_bits = message_as_bits(image, message)
    message_len = len(message)
    if message_len > 255:
        raise RuntimeError("Message must be no longer than 255 letters")

    #
    # Encode the message length in the blue part
    # of the first pixel
    #
    r, g, b = data.getpixel((0, 0))
    data.putpixel((0, 0), (r, g, message_len))
    #
    # Place one byte as the LSB of the blue part of the
    # RGB value of the first 8 pixels of each line
    # NB doing it this way avoids having to map between
    # groups of 8 bits and coordinates in an image.
    #
    for row, bits in zip(range(data.height, message)):
        for column, bit in enumerate(bits):
            rgb = data.getpixel((column, row))
            data.putpixel((column, row), blue_final_bit(rgb, bit))

    image.putdata(data)
    return image

if __name__ == '__main__':
    image_filepath = input("Enter an image filename: ")
    message = input("Enter a message: ")
    dragon = Image.open(image_filepath)
    encoded_dragon = encoded(dragon, message)
    encoded_dragon.save("encoded_dragon.jpg")
