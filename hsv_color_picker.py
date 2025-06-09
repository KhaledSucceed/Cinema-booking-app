import cv2

# Load your image
image_path = "seating_chart.jpg"  # Make sure the image is in the same folder
img = cv2.imread(image_path)

# Resize to match the tkinter canvas dimensions
img = cv2.resize(img, (1280, 720))

# Convert to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define a mouse callback function
def show_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_hsv = hsv[y, x]
        print(f"HSV at ({x},{y}) = {tuple(pixel_hsv)}")

# Create a window and bind the mouse callback
cv2.namedWindow("Click to Get HSV (Resized 960x540)")
cv2.setMouseCallback("Click to Get HSV (Resized 960x540)", show_hsv)

# Display the image and wait for clicks
print("🖱 Click on the image to print HSV values. Press ESC to exit.")
while True:
    cv2.imshow("Click to Get HSV (Resized 960x540)", img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break

cv2.destroyAllWindows()
