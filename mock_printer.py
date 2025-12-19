from PIL import Image

class MockPrinter():
    def __init__(self, num_printers=3, printer_name="Canon SELPHY CP1500"):
        # printer_name shall be the string that the driver looks for
        print("MOCK: Using {}".format(printer_name))
        self.num_printers = num_printers
        print("MOCK: Found {} printers".format(self.num_printers))
        print("MOCK: Printer(s) connected!")
        self.printer_size = (1200, 1800)
        print("MOCK: Printer size: {}".format(self.printer_size))

    def print_images(self, file_path, num_copies=1, autorotate=True, autoscale=False):
        print("MOCK: File: {} Copies: {}".format(file_path, num_copies))
        # 1. Open the image
        try:
            im = Image.open(file_path)
        except Exception as e:
            print(f"MOCK: Error opening image: {e}")
            return
        print("MOCK: Image opened successfully.")

        if (autorotate):
            if (im.width > im.height):
                # This is a landscape image, rotate it
                im = im.rotate(90, expand=True)
                print("MOCK: Rotated image to portrait mode.")

        if (autoscale):
            print("MOCK: Autoscale is enabled.")
            # Scale the image to fit printer size
            # We compare the width ratio and height ratio and take the smaller one
            scale = min(self.printer_size[0] / im.width, self.printer_size[1] / im.height)
            print("MOCK: Scale factor: {}".format(scale))
        else:
            scale = 1.0
            print("MOCK: Autoscale is disabled. Using scale factor: {}".format(scale))

        # Calculate new size
        new_width = int(im.width * scale)
        new_height = int(im.height * scale)
        if (autoscale):
            print("MOCK: Scaling image to: {}x{}".format(new_width, new_height))
        else:
            print("MOCK: Keeping original image size: {}x{}".format(new_width, new_height))

        page_per_printer = num_copies // self.num_printers
        remainder = num_copies % self.num_printers
        print("MOCK: Page per printer: {}, Remainder: {}".format(page_per_printer, remainder))

        for x in range(self.num_printers):
            pages = page_per_printer + (1 if x < remainder else 0)
            if (pages > 0):
                print("MOCK: Sent {} pages to printer {}".format(pages, x))
