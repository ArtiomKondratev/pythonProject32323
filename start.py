from main import NedoScannerSN, ScannerSN
choice = input("Выберите метод. Scanner или NedoScanner) ")
if choice == "Scanner":
    try:
        port_scanner = ScannerSN()
        port_scanner.start_cumming()
    except KeyboardInterrupt:
        pass

elif choice == "NedoScanner":
    try:
        port_scanner = NedoScannerSN()
    except KeyboardInterrupt:
        pass
