# BeagleBone Blue Plugin

## Hardware Setup

### Install Debian Image

Download: https://rcn-ee.net/rootfs/bb.org/testing/2019-01-13/stretch-console/bone-debian-9.6-console-armhf-2019-01-13-1gb.img.xz

Flash the Debian image to a microSD card using Etcher (https://etcher.io). Then insert the microSD into the BeagleBone Blue and power it on.

### Connect to the BeagleBone Blue

If you have not connected the BeagleBone Blue to your computer via microUSB, do so now. Lights on the board should start flashing. Once LED 0 begins flashing in a heartbeat pattern, the board is ready.

Now we will log into the BeagleBone Blue via SSH. The default username and password are:

    * Username: debian
    * Password: temppwd

----

**For MacOS and Linux**
```
ssh debian@192.168.6.2
```
When prompted, enter **temppwd** as the password for the debian account.

**For Windows**

I prefer to use PuTTY to connect to **192.168.7.2** using the default credentials above.

----

We will now allow the debian user to **sudo** without needing to enter the password subsequent times.

```
echo "debian ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers.d/debian >/dev/null
```

Now would be a good time to change the password for our debian user to something more secure.

```
passwd
```

### Connect to WiFi

Next we are going to connect the BeagleBone Blue to our local Wi-Fi network. For the next command, we will need the SSID of the network.

```
sudo -s connmanctl services | grep "<your SSID>" | grep -Po 'wifi_[^ ]+'
```

This command will output a hash like the following.
```
$ sudo -s connmanctl services | grep "My Wi-Fi Network" | grep -Po 'wifi_[^ ]+'
wifi_8030dc047131_536e7964657227732057692d4669204e6574776f726b_managed_psk
```

Now we will use the hash to configure our Wi-Fi connection. Make sure to type each line carefully; do not copy/paste.
```
$ sudo chmod -R 777 /var/lib/connman/
$ cat >/var/lib/connman/wifi.config
[service_<your hash>]
Type = wifi
Security = wpa2
Name = <your SSID>
Passphrase = <your Wi-Fi password>
```

After entering your passphrase, `Ctrl-D` to quit the prompt. Then type `exit`.

A green light should turn on to show that Wi-Fi is working. The BeagleBone Blue is now connected to the Wi-Fi network and its ip address can be found using
```
ip addr show wlan0
```

### Update and Install Available Software

Now that the BeagleBone Blue is connected to Wi-Fi, we can perform the following steps:
1. Update software onboard
```bash
sudo apt-get -y update
sudo apt-get -y dist-upgrade
sudo apt-get install -y cpufrequtils git
```
2. Update scripts
```bash
cd /opt/scripts && git pull
```
3. Specify real-time kernel
```bash
sudo /opt/scripts/tools/update_kernel.sh --lts-4_19 --bone-rt-channel
```
4. Specify device tree binary to be used at startup
```bash
sudo sed -i 's/#dtb=/dtb=am335x-boneblue.dtb/g' /boot/uEnv.txt
```
5. Set clock frequency
```bash
sudo sed -i 's/GOVERNOR="ondemand"/GOVERNOR="performance"/g' /etc/init.d/cpufrequtils
```
6. Adjust bb-wl18xx-wlan0.service
```bash
sudo sed -i 's/RestartSec=5/RestartSec=1/g' /lib/systemd/system/bb-wl18xx-wlan0.service
```
7. Maximize the microSD card's existing partition (which is /dev/mmcblk0p1)
```
sudo /opt/scripts/tools/grow_partition.sh
```
8. Reboot
```
sudo reboot
```
## ArduPilot Setup

Now we will configure the BeagleBone Blue for use with ardupilot.
#### 1. Create the ArduPilot environment configuration file.
```bash
sudo vim /etc/default/ardupilot
```
Or:
```
sudoedit /ect/default/ardupilot
```
Then paste into the file your configuration values and save. Below is an example of a valid configuration.
```bash
TELEM1="-C /dev/ttyO1"
TELEM2="-A udp:<target IP address>:14550"
GPS="-B /dev/ttyS2"
```
Switches A-F are defaulted to the following protocols and can be individually configured as shown in the example above.
```bash
Switch -A  -->  "Console", SERIAL0, default 115200
Switch -B  -->  "GPS", SERIAL3, default 57600
Switch -C  -->  "Telem1", SERIAL1, default 57600
Switch -D  -->  "Telem2", SERIAL2, default 38400
Switch -E  -->  Unnamed, SERIAL4, default 38400
Switch -F  -->  Unnamed, SERIAL5, default 57600
```
Consult the official ArduPilot documentation for more details on the various serial ports: http://ardupilot.org/plane/docs/parameters.html?highlight=parameters

#### 2. Next, we'll create the ArduPilot systemd service files.

* **ArduCopter** */lib/systemd/system/arducopter.service*
```bash
[Unit]
Description=ArduCopter Service
After=networking.service
StartLimitIntervalSec=0
Conflicts=arduplane.service ardurover.service antennatracker.service

[Service]
EnvironmentFile=/etc/default/ardupilot
ExecStartPre=/usr/bin/ardupilot/aphw
ExecStart=/usr/bin/ardupilot/arducopter $TELEM1 $TELEM2 $GPS

Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target
```

* **ArduPlane** */lib/systemd/system/arduplane.service*

```bash
[Unit]
Description=ArduPlane Service
After=networking.service
StartLimitIntervalSec=0
Conflicts=arducopter.service ardurover.service antennatracker.service

[Service]
EnvironmentFile=/etc/default/ardupilot
ExecStartPre=/usr/bin/ardupilot/aphw
ExecStart=/usr/bin/ardupilot/arduplane $TELEM1 $TELEM2 $GPS

Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target  
```

* **ArduRover** */lib/systemd/system/ardurover.service*

```bash
[Unit]
Description=ArduRover Service
After=networking.service
StartLimitIntervalSec=0
Conflicts=arducopter.service arduplane.service antennatracker.service

[Service]
EnvironmentFile=/etc/default/ardupilot
ExecStartPre=/usr/bin/ardupilot/aphw
ExecStart=/usr/bin/ardupilot/ardurover $TELEM1 $TELEM2 $GPS

Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target
```

* **AntennaTracker** */lib/systemd/system/antennatracker.service*

```bash
[Unit]
Description=AntennaTracker Service
After=networking.service
StartLimitIntervalSec=0
Conflicts=arducopter.service arduplane.service ardurover.service

[Service]
EnvironmentFile=/etc/default/ardupilot
ExecStartPre=/usr/bin/ardupilot/aphw
ExecStart=/usr/bin/ardupilot/antennatracker $TELEM1 $TELEM2 $GPS

Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target
```

#### 3. Create a new directory for hardware configuration files.
```bash
sudo mkdir -p /usr/bin/ardupilot
```
Create the hardware configuration file: */usr/bin/ardupilot/aphw*
```
#!/bin/bash
# aphw
# ArduPilot hardware configuration.

/bin/echo 80 >/sys/class/gpio/export
/bin/echo out >/sys/class/gpio/gpio80/direction
/bin/echo 1 >/sys/class/gpio/gpio80/value
/bin/echo pruecapin_pu >/sys/devices/platform/ocp/ocp:P8_15_pinmux/state
```

Lines 5 to 7 switch on power to the BBBlue's +5V servo rail - i.e. for when you're using servos. Not necessary for ESCs.

Line 8 enables the PRU.

Use `sudo chmod 0755 /usr/bin/ardupilot/aphw` to set permissions for this file.

#### 4. Download the ArduCopter, ArduPlane, etc. executables, built specifically for the BeagleBone Blue's architecture.
* **ArduCopter** (http://bbbmini.org/download/blue/ArduCopter/)
```bash
cd ~/
mkdir ArduCopter
cd ArduCopter/
wget http://bbbmini.org/download/blue/ArduCopter/arducopter-3_5_4
cp arducopter-3_5_4.dms /usr/bin/ardupilot/
```
* **ArduPlane** (http://bbbmini.org/download/blue/ArduPlane/)
```bash
cd ~/
mkdir ArduPlane
cd ArduPlane/
wget http://bbbmini.org/download/blue/ArduPlane/arduplane-3_8_3
cp arduplane-3_8_3.dms /usr/bin/ardupilot/
```
* **ArduRover** (http://bbbmini.org/download/blue/ArduRover/)
```bash
cd ~/
mkdir ArduRover
cd ArduRover/
wget http://bbbmini.org/download/blue/ArduRover/ardurover
cp ardurover.dms /usr/bin/ardupilot/
```
Once downloaded and copied to the `/usr/bin/ardupilot` directory, make sure to set proper permissions: 
```
sudo chmod 0755 /usr/bin/ardupilot/a*
```
#### 5. Start up ArduPilot
Choose your flavor of ArduPilot and start it up with `systemctl`
```
sudo systemctl enable arducopter.service
```
Or:
```
sudo systemctl enable arduplane.service
```
Or:
```
sudo systemctl enable ardurover.service
```
Or:
```
sudo systemctl enable antennatracker.service
```
After a reboot, you should see a flashing red LED which means everything is working as expected.

You can use `systemctl` to start and stop the ArduPilot service whenever you like.
```
sudo systemctl disable ...
sudo systemctl start ...
sudo systemctl stop ...
```