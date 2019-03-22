# Raspberry Pi Software Repository

# Instructions
1. Install the dependency package `sudo pip3 install rpi_ws281x`
2. Connect the LED strip according to the diagram in this order 
  * 1) Ground(LED) to Ground(PI-pin 12)
  * 2) 5V (LED) to 5v(PI-pin 4)
  * 3) DATA (LED) to GPIO18 (PI-pin 14)
3. From the repo, run the driver program with `sudo python3 pi-lit.py -c`
4. Follow the prompts to change color of strip
