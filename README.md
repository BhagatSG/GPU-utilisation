# GPU-utilisation

Whenever you are creating a new VM using GPU, You need to do this one-time activity to run GPU utilisation service.  
 
Please use the attached script for copying to your user home directory on VM.  
Once Copied, Please run following commands:    
cd   
chmod -R 777 gpuutilisation.sh  
chmod -R 777 gpuutilisation.service   
chmod -R 777 gpuutilisation.py   
chmod -R 777 config.ini   
 
sudo cp gpuutilisation.py /root/   
sudo chmod u+x /root/gpuutilisation.py    
sudo cp config.ini /root/   
sudo chmod u+x /root/config.ini    
sudo cp gpuutilisation.sh /root/   
sudo chmod u+x /root/gpuutilisation.sh    
sudo cp gpuutilisation.service /etc/systemd/system/   
 
After running above commands, to start service please run below command and it shouldn’t throw any error:   
sudo systemctl start gpuutilisation   
 
Enable it to run at boot:   
sudo systemctl enable gpuutilisation   
 
Let me know if you face any issue in above process.    
 
Things to remember:    
i)                    Every time when you are re-starting your VM after de-allocating, It always gets the new IP. This IP needs to be whitelisted for DB Connection.
