The web server is started as a service called plantwatering.service
 /lib/systemd/system/plantwatering.service
```
Description=Web Server of Plant Watering Control Panel 

[Service]
ExecStart=/usr/bin/python /home/pi/PlantWateringProject/web-plant-watering.py
WorkingDirectory=/home/pi/PlantWateringProject
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

And the cron job that runs everyday at 7 am to determine if watering is necessary or not, belongs to root
0 7 * * * /usr/bin/python2.7 /home/pi/PlantWateringProject/SoilMoistureRead.py
