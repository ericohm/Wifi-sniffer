#!/bin/bash
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
echo none > /sys/class/leds/led0/trigger
rm /home/pi/Test/*.*
rm /home/pi/Pictures/*.*
rm signals.txt
rm default.p
sudo iw phy phy0 interface add mon0 type monitor > /dev/null 2>&1 &
sleep 1
sudo iw dev wlan0 del > /dev/null 2>&1 &
kismet_server > /dev/null 2>&1 &
python gpstotext.py &

echo "Starting up Kismet and GPS"
sleep 30

echo "Everything up and running"

echo heartbeat > /sys/class/leds/led0/trigger
#python3 sdr.py &
for i in {1..10000}
do      
        sleep 5
        echo " "
        echo "---- getsignals.py begins ----"
        python3 getsignals.py
        echo "---- getsignals.py ends ----"
        sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
        kismet_server > /dev/null 2>&1 &
done



sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1

#python3 approximate.py
#python3 convertPictures.py
#node uploadsignals.js





