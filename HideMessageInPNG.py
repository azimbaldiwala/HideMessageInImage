import cv2
import numpy as np
from PIL import Image




def toBinary(data):
    #Convert the string data into binary
    p = ''
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]   # Returns array of bin values of pix
    return p


# hide data in given img

def hidedata(img, data):   
    data += "$#"  # appending end delimeters at the end of the string to denote end of the messasge.                           
    d_index = 0
    b_data = toBinary(data)
    len_data = len(b_data)
    #iterate pixels from image and update pixel values
    for value in img:
        for pix in value:
            r, g, b = toBinary(pix)

            # For each pixel and for r g and b of each pixel

            # editing the last bit which is the msb 
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index])
                d_index += 1
            if d_index >= len_data:
                break
    return img


def encode():
    img_name = input("\nEnter image name:")
    image = cv2.imread(img_name)#gives pixels format
    img = Image.open(img_name, 'r')#gives width height
    w, h = img.size
    data = input("\nEnter Message:")
    if len(data) == 0:
        return print("Encrypting failed because the message is empty")
    enc_img = input("\nEnter Encoded Image Name:")
    enc_data = hidedata(image, data)
    cv2.imwrite(enc_img, enc_data)
    img1 = Image.open(enc_img, 'r')
    img1 = img1.resize((w, h),Image.Resampling.LANCZOS)
    # optimize with 65% quality
    if w != h:
        img1.save(enc_img, optimize=True, quality=65)
        return print("Image Encrypted Successfully...")
    else:
        img1.save(enc_img)
        return print("Image Encrypted Successfully...")

# decoding

def extract_data(img):
    bin_data = ""   # hidden message

    #traverse all the pixels 
    for value in img:
        for pix in value:
            #Extract last bit of r g and b of each pixels  
            r, g, b = toBinary(pix)     # returns the numpy array
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    # Grouping 8 bits into 1 byte
    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]  
    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$#":      # Stop when we get end delimeter
            break
    return readable_data[:-2]  # return original data excluding the delimeters


def decode():
    img_name = input("\nEnter Encoded Image Name : ")
    image = cv2.imread(img_name)
    msg = extract_data(image)
    return msg

if __name__ == '__main__':
    x = 0
    while x != 3:
        print('''
           1.Encrypt
           2.Decrypt
           3.Exit''')
        x = int(input("\n Enter your choice: "))
        if x == 1:
            encode()
        elif x == 2:    
            ans = decode()
            print("\nEncoded message is :" + ans)
        elif x > 3 or x <=0:
            print("Invalid Input!!")
    
    print("Program exited!")