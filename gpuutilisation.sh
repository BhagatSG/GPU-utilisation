#!/bin/sh
cd /root
mkdir -p -- 'gpuutilisation'
apt update && apt install -y libsm6 libxext6 libxrender-dev

apt-get install libgdal-dev -y
apt-get install unixodbc-dev -y

pythonVersion=$(python3 --version)
echo $pythonVersion
version=$(echo "$pythonVersion" | rev | cut -d" " -f1  | rev)
echo $version
finalVersion=$(echo "$version" | rev | cut -d"." -f2-  | rev)
echo $finalVersion

apt-get install python$finalVersion-dev -y

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install gpustat
chmod -R 777 gpuutilisation

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update
ACCEPT_EULA=Y apt-get install msodbcsql17 -y

cd
echo '***************************************************' >> gpuutilisation/utilisation.json
chmod -R 777 gpuutilisation/utilisation.json
echo 'json data directory:: gpuutilisation/utilisation.json'  > gpuutilisation/utilisation.json

vmName=$(curl -H Metadata:true "http://IP/metadata/instance/compute/name?api-version=2017-08-01&format=text")
vmId=$(curl -H Metadata:true "http://IP/metadata/instance/compute/vmId?api-version=2017-08-01&format=text")
vmSize=$(curl -H Metadata:true "http://IP/metadata/instance/compute/vmSize?api-version=2017-08-01&format=text")
resourceGroupName=$(curl -H Metadata:true "http://IP/metadata/instance/compute/resourceGroupName?api-version=2017-08-01&format=text")
subscriptionId=$(curl -H Metadata:true "http://IP/metadata/instance/compute/subscriptionId?api-version=2017-08-01&format=text")

fileName=$vmName##$vmId##$vmSize##$resourceGroupName##$subscriptionId

pip install pyodbc
pip install pandas
pip install configparser
pip install os

while true
do
        echo '***************************************************' >> gpuutilisation/utilisation.json
        current_date_time="`date "+DATE: %Y-%m-%d%nTime: %H:%M:%S"`";

        echo 'Start time: ' $current_date_time >> gpuutilisation/utilisation.json
        gpustat --json >> gpuutilisation/utilisation.json

        gpustat --json > gpuutilisation/$fileName.json

        chmod -R 777 gpuutilisation/$fileName.json

        echo '***************************************************' >> gpuutilisation/utilisation.json

        python3 /root/gpuutilisation.py /root/gpuutilisation/$fileName.json
        sleep 300
done
