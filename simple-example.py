from PIL import Image

dragon = Image.open("dragon.jpg")
data = dragon.getdata()
assert len(data) == dragon.width * dragon.height

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

b_with_0_last_bit = b & 0xfe
b_with_1_last_bit = b | 1