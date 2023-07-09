# Import the Image module from PIL
from PIL import Image
import fitz
import cv2
def find_per():

    # Open the image file
    img1 = Image.open("C:\\Users\\shahs\\OneDrive\\Desktop\\match.png")
    img2 = Image.open("C:\\Users\\shahs\\GITHUB\\TCET OPENSOURCE\\resumee.png")
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Get the width and height of the image
    width1, height1 = img1.size
    width2, height2 = img2.size

    # Initialize the variables to store the total number of pixels and the number of white pixels
    total_pixels1 = 0
    white_pixels1 = 0
    black_pixels1 = 0

    total_pixels2 = 0
    white_pixels2 = 0
    black_pixels2 = 0


    # Loop through all the pixels in the image
    for x in range(width1):
        for y in range(height1):
            # Get the pixel value at (x, y)
            pixel = img1.getpixel((x, y))
            
            # Increment the total number of pixels
            total_pixels1 += 1
            
            # Check if the pixel is white
            if pixel == (255, 255, 255):
                # Increment the number of white pixels
                white_pixels1 += 1
            
            # Otherwise, do nothing
            else:
                img1.putpixel((x, y), (0, 0, 0))
                black_pixels1 += 1

    # Print the results
    print(f"Total number of pixels: {total_pixels1}")
    print(f"Total number of white pixels: {white_pixels1}")
    print(f"Total number of black pixels: {black_pixels1}")
    print(f"Percentage of white pixels: {(white_pixels1 / total_pixels1) * 100:.2f}%")
    print(f"Percentage of black pixels: {(black_pixels1 / total_pixels1) * 100:.2f}%")
    blackper1 = (black_pixels1 / total_pixels1) * 100

    img1.save("image1.png")

    for x in range(width2):
        for y in range(height2):
            # Get the pixel value at (x, y)
            pixel = img2.getpixel((x, y))
            
            # Increment the total number of pixels
            total_pixels2 += 1
            
            # Check if the pixel is white
            if pixel == (255, 255, 255):
                # Increment the number of white pixels
                white_pixels2 += 1
            
            # Otherwise, do nothing
            else:
                img2.putpixel((x, y), (0, 0, 0))
                black_pixels2 += 1

    # Print the results
    print(f"Total number of pixels: {total_pixels2}")
    print(f"Total number of white pixels: {white_pixels2}")
    print(f"Total number of black pixels: {black_pixels2}")
    print(f"Percentage of white pixels: {(white_pixels2 / total_pixels2) * 100:.2f}%")
    print(f"Percentage of black pixels: {(black_pixels2 / total_pixels2) * 100:.2f}%")
    blackper2 = (black_pixels2/total_pixels2)*100



    img2.save("image2.png")


    print("BLANK AREA PERCENTAGE")
    print(100-((blackper2*100)/blackper1))
    return 100-((blackper2*100)/blackper1)
a=0
i=0
file_path = "C:\\Users\\shahs\\GITHUB\\LINKEDIN ANALYSIS\\resume_meta.pdf"
doc = fitz.open(file_path)  # open document
for page in doc:
    i+=1
    pix = page.get_pixmap()  # render page to an image
    pix.save("resumee.png")
    a+=find_per()
print("the final percentage of blank area for the resume is")
print(a/(i))



