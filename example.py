from printer import (
    MockPrinter,
    Printer
)

drv = MockPrinter()
# drv = Printer()
drv.print_images("sample.jpg", 3)