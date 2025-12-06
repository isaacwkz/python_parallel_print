from PIL import Image, ImageWin

class MockPrinter():
    def __init__(self, printer_name=None):
        # printer_name shall be the string that the driver looks for
        print("Printer initialized.")

    def print_images(self, file_path, num_copies=1):
        print("File: {} Copies: {}".format(file_path, num_copies))
        # 1. Open the image
        try:
            Image.open(file_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return
        print("Image opened successfully.")
    
class Printer():
    def __init__(self, printer_name=None):
        # printer_name shall be the string that the driver looks for
        print("UNIMPLEMENTED")

    def print_images(self, file_path, num_copies=1):
        print("File: {} Copies: {}".format(file_path, num_copies))
        # 1. Open the image
        try:
            Image.open(file_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return
        print("Image opened successfully.")
