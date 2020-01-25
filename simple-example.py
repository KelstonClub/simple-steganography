from PIL import Image

#
# Open an image and pull out uncompressed
# pixel data, checking that the number of
# pixels is equals to the "pixel area" of
# the image
#
dragon = Image.open("dragon.jpg")
data = dragon.getdata()
assert len(data) == dragon.width * dragon.height

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
print(message_bits)

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