def encode():
    message = input("Enter the message to encode: ")  # Get the message from the user
    message += "@@@"  # Enter symbols used to end the message in decoding
    message_bin = []  # Set up a list to store each character in binary
    for i in message:
        message_bin.append('{0:08b}'.format(ord(i)))  # Append each converted character to message_bin
    message = ""  # Clear out the original message variable
    for i in range(len(message_bin)):
        message += message_bin[i]  # Write the binary as a continuous string

    image = input("Choose image (must be .bmp in root folder): ")  # Get the BMP image to use from the user

    byte_list = []  # Set up a list to store each byte
    with open(image, "rb") as file:
        while True:
            byte = file.read(1)
            if not byte:  # Stop when out of bytes to read
                break
            byte_list.append(byte)  # Add each byte to byte_list

    binary = []  # Set up a list to store the binary
    for byte in byte_list:
        int_value = ord(byte)  # Convert the byte to a UTF character
        binary_string = '{0:08b}'.format(int_value)  # Convert the UTF character to binary
        binary.append(binary_string)  # Append the binary to the list as strings

    if len(message) > len(binary) - 54:  # Ensure the message will fit and terminate if it won't
        return "Message too long. Larger BMP needed."
    position = 54  # Set the position in the image binary to start (BMP image data starts at 55)
    for i in message:
        val = binary[position]  # Get the first string of 8 binary digits
        val2 = ""  # Set up a string variable for use
        count = 0  # Set the counter to 0
        for ii in val:
            if count < 7:  # Copy the first 7 digits of the 8 in the binary byte
                val2 += ii
            else:  # Set the 8th bit to one from the converted message
                val2 += i
            count += 1  # Increase the count
        binary[position] = val2  # Replace the image byte with the altered byte
        position += 1  # Increment the position so as to get the next byte from the list

    converted_binary = []  # Set up the list to hold the final binary
    for i in range(len(binary)):
        converted_binary.append(int(binary[i], 2))  # Write the final binary as a list of integers, not strings

    name = input("Choose a name for your new file: ")  # Get a filename from the user for the output

    f = open(name, 'w+b')  # Create the output file in binary write mode
    binary_format = bytearray(converted_binary)  # Create the byte array
    f.write(binary_format)  # Write the byte array
    f.close()  # Close the file

    return "Your message has been encoded into the image."


def decode():
    image = input("Choose image (must be .bmp in root folder): ")  # Get the file to decode from the user
    byte_list = []  # Set up a list to hold the byte data
    with open(image, "rb") as file:  # Open the file in binary read mode
        while True:
            byte = file.read(1)
            if not byte:
                break
            byte_list.append(byte)  # Add the byte data to the list

    binary = []  # Set up a list to hold the actual binary
    for byte in byte_list:
        int_value = ord(byte)  # Convert the byte data to a UTF character
        binary_string = '{0:08b}'.format(int_value)  # Convert the UTf character to binary
        binary.append(binary_string)  # Append the binary to the list as strings

    message = ""  # Set a string to hold the binary message
    position = 54  # Set the position to start reading the binary data (after the BMP headers and stuff)
    while position < len(binary):
        if (position - 54) % 8 == 0 and position != 54:  # Insert a space after every 8 bits
            message += " "
        val = binary[position]
        count = 0
        for i in val:
            if count == 7:  # Read only the last bit in every 8 and add it to the message
                message += i
            count += 1
        position += 1

    letter = ""
    end_counter = 0
    for i in message:
        if i != " ":
            letter += i
            if len(letter) == 8:  # If 8 bits have been put together
                letter = int(letter, 2)  # Turn the byte into a decimal number
                letter = chr(letter)  # Turn the decimal number into a character
                print(letter, end="")
                if letter == "@":
                    end_counter += 1
                else:
                    end_counter = 0
                if end_counter >= 3:
                    break
                letter = ""
    print()



choice = "huh?"
while choice != "exit":
    choice = input("Do you want to (e)ncode, (d)ecode or exit?: ")
    if choice == "e":
        print(encode())
    if choice == "d":
        decode()
