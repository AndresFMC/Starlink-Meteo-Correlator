import pyshark

# Abrir el archivo pcap con Pyshark
cap = pyshark.FileCapture('/Users/andrew/Desktop/ETSIT 23-24/TFG/Dataset/quic-h3/results-2021_12_23_14h55m29s-12348/capture-h3-10000.pcap')

# Imprimir detalles de los primeros 10 paquetes
for i, pkt in enumerate(cap):
    print(f"Packet {i+1}: {pkt}")
    if i == 9:
        break
