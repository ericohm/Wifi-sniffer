#!/bin/bash
echo none > /sys/class/leds/led0/trigger
rm /home/pi/Test/*.*
rm test.txt
rm signals.txt
rm default.p
sudo iw phy phy0 interface add mon0 type monitor > /dev/null 2>&1 &
sudo iw dev wlan0 del > /dev/null 2>&1 &

kismet_server > /dev/null 2>&1 &

(while [ 1 ]; do sleep 1; done) |  mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600 --aircraft Mycopter  > /dev/null 2>&1 &
my_pid=$!

echo "Mavproxy and Kismet is starting so wait man"

file_exists=0
while [ $file_exists -lt 10 ];
do
        echo 1 > /sys/class/leds/led0/brightness
	echo "Waiting for Mavproxy.."
        echo 'status GPS_RAW_INT' > /proc/$my_pid/fd/0
        sleep 2
        [[ -s test.txt ]]
        if [ $? -eq 0 ]; then
                echo "Mavproxy has started!!"
                let file_exists=10
        fi;
	echo 0 > /sys/class/leds/led0/brightness
	sleep 2
done


echo "MavProxy is Online!"
 echo heartbeat > /sys/class/leds/led0/trigger
for i in {1..10000}
do
        sleep 1
        echo 'status GPS_RAW_INT' > /proc/$my_pid/fd/0
        sleep 2
	#cat test.txt
	#cat signals.txt
        python3 getsignals.py
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

python3 approximate.py
node uploadsignals.js




