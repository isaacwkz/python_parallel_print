# Part of pywin32 library
import win32print, win32ui, win32con
from PIL import Image, ImageWin

class InternalPrinter():
    def __init__(self):
        return
        # Nothing to do here for now

    def get_list_of_printers(self, printer_name):
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers = win32print.EnumPrinters(flags)
        list_of_printers = []
        for device in printers:
            if printer_name in device[2]:
                list_of_printers.append(device[2])
        return list_of_printers
    
class Printer():
    def __init__(self, printer_name="Canon SELPHY CP1500"):
        # printer_name shall be the string that the driver looks for
        self.int_drv = InternalPrinter()
        self.printers = self.int_drv.get_list_of_printers(printer_name)
        self.num_printers = len(self.printers)
        print("Found {} printers".format(self.num_printers))
        # Setup connection to the printers
        # List of Device Contexts
        self.hDC = []
        for x in range(self.num_printers):
            try:
                self.hDC.append(win32ui.CreateDC())
                self.hDC[x].CreatePrinterDC(self.printers[x])
            except Exception as e:
                print("Error connecting to printer {}: {}".format(x, e))
                raise
        print("Printer(s) connected!")
        # Get the specs of the printer
        # We will assume all printers are the same
        self.printer_size = self.hDC[0].GetDeviceCaps(win32con.HORZRES), \
            self.hDC[0].GetDeviceCaps(win32con.VERTRES)
        print("Printer size: {}".format(self.printer_size))


    def print_images(self, file_path, num_copies=1):
        print("File: {} Copies: {}".format(file_path, num_copies))
        # 1. Open the image
        try:
            im = Image.open(file_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return
        print("Image opened successfully.")

        # Scale the image to fit printer size
        # We compare the width ratio and height ratio and take the smaller one
        scale = min(self.printer_size[0] / im.width, self.printer_size[1] / im.height)
        print("Scale factor: {}".format(scale))

        # Calculate new size
        new_width = int(im.width * scale)
        new_height = int(im.height * scale)
        print("Scaling image to: {}x{}".format(new_width, new_height))
        
        # Center the image on the page (optional, remove offsets to print top-left)
        x_offset = (self.printer_size[0] - new_width) // 2
        y_offset = (self.printer_size[1] - new_height) // 2

        page_per_printer = num_copies // self.num_printers
        remainder = num_copies % self.num_printers
        
        for x in range(self.num_printers):
            try:
                # Start the document to print
                self.hDC[x].StartDoc("{} - {}".format(x, file_path))
                pages = page_per_printer + (1 if x < remainder else 0)
                for y in range (pages):
                    self.hDC[x].StartPage()
                    # Creat Windows bitmap
                    dib = ImageWin.Dib(im)
                    # Draw the image on the new page with the scaling calculated from earlier
                    dib.draw(self.hDC[x].GetHandleOutput(), (x_offset, y_offset, x_offset + new_width, y_offset + new_height))
                    self.hDC[x].EndPage()
                # End the document to print
                self.hDC[x].EndDoc()
                print("Sent {} pages to printer {}".format(pages, x))
            except Exception as e:
                print("Error printing from {}: {}".format(x, e))
                # If a job was started but failed, we might need to abort
                try:
                    self.hDC[x].AbortDoc()
                except:
                    pass
                raise
        