#!/bin/bash

rm ./*.netxml
rm signals.txt
rm default.p
rm gsm_power.txt
#rm dronepath.txt

bit=0
trap ctrl_c INT

function ctrl_c() {
	echo "KILL ALLLLLLLL"
	kill $gps_pid
	kill $kismet_pid
	kill $gnuradio_pid
	kill $videotime_pid
	kill $readfft_pid
	bit=12
	
}


sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1
sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
sleep 1

sudo iw phy phy0 interface add mon0 type monitor > /dev/null 2>&1 &
sleep 1
sudo iw dev wlan0 del > /dev/null 2>&1 &

kismet_server > /dev/null 2>&1 &
kismet_pid=$!
echo "Kismet PID is ",$kismet_pid

python gpstotext.py &
gps_pid=$!
echo "gps PID is ",$gps_pid

echo "Starting up GPS"
python3 gpsWorking.py

echo "Giving Kismet some time..."
sleep 10

./top_block.py > /dev/null 2>&1 & 
gnuradio_pid=$! 
echo "gnuradio_pid is ",$gnuradio_pid

file_exists=0
while [ $file_exists -lt 10 ];
do
	echo "Waiting for GNURADIO.."
    sleep 2
	[[ -s gsm_power.txt ]]
	if [ $? -eq 0 ]; then
	        echo "GNURADIO has started!!"
	        let file_exists=10
	fi;
done

python read_fft.py &
readfft_pid=$!

echo "Start streaming video in 3 seconds"
sleep 3
python3 videoTime.py &
videotime_pid=$!

echo "Everything up and running"

while [ $bit -lt 10 ];
do      
        python3 getsignals.py
        sleep 5
        #sudo echo -e '!1 SHUTDOWN' | nc localhost 2501
        #kismet_server > /dev/null 2>&1 &
        
done

echo "HAHAHAHAH EXIIT !!"

#python3 approximate.py
#python3 convertPictures.py
#node uploadsignals.js
