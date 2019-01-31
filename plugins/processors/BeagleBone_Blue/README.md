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
