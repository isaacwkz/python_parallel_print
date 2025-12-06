from printer import Printer
from mock_printer import MockPrinter

drv = MockPrinter(num_printers=3)
#drv = Printer()
#drv = Printer("Microsoft Print to PDF")
drv.print_images("sample.jpg", 3)