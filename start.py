from main import NedoScannerSN

try:
    port_scanner = NedoScannerSN()
    port_scanner.output()
except KeyboardInterrupt:
    pass
