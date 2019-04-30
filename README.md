# Raspberry Pi Software Repository

This repository contains everything necessary for a remote Raspberry Pi to
receive commands from the central server. The two main components are the client
(client.js) and the driver (pi-lit.py).

### Directions
1. npm install
2. Install the dependency package `sudo pip3 install rpi_ws281x`
3. Connect the LED strip according to the diagram in this order
  * 1) Ground(LED) to Ground(PI-pin 12)
  * 2) 5V (LED) to 5v(PI-pin 4)
  * 3) DATA (LED) to GPIO18 (PI-pin 14)
4. From the repo, run the driver program with `sudo node client.js | sudo python3 pi-lit.py -c`

### Registration
Before the pi can receive commands it must be registered by a user. The MAC address of the
network interface specified in the config.json file is used to identify the pi during
the registration process. After the registration process is finished the information
is stored in the config.json file.
