# Jaccuracy Scope
![LoadingScreen2](https://github.com/user-attachments/assets/c57eea87-c5b9-470f-856e-7e7c130cc388)

Thank you for your interest in the Jaccuracy Scope Project!  There is a donation page link to the right if you support this project [Buy Me A Coffee Page](https://buymeacoffee.com/jaccuracyscope). 

[Video Introduction](https://youtu.be/HgzltnaVOiY?si=L6nHdwi97msg5Pw5)

Seems that installing this on Pi 4B with Rasbian Bullseye(64-bit) is the best option for FPS speed. Please bulid this with the Pi 4B option, further developement is needed for good FPS with the new Pi 5 (the SPI bus is slower). 
So please avoid the Pi5 and Bookworm for this project... 


At the time of writing this, I have hope for the community of long range shooting enthusiasts to develop this further as my time to dedicate here has run short. I hope for the following features in the evolution of this project: 

- Inclusion of Coriolis and Eotvos Effects with Coordinate input in the settings.
- Internal IMU Calibration for the Accelerometer, Magnetometer and Gyroscope
- A build using an HDMI small screen for compact builds, Raspberry Pi 5 capability, and support faster frame rate and features.
- A Low Power mode where the ballistic calculations and screen will turn to a slow frame rate to save power consumption wildly. 
- A Separate Menu option for Atmospheric conditions during the time of Zeroing the rifle 
- Inclusion of Scope Height Adjustment  (right now its assumed to be 1.75 inches, but can be edited in the BallisticThreader4Prin….. files , edit the ‘self.scope_height = 1.75’  line for your rifle.  For now. 
-A physical build kit inlcuding a harness for easy building!  (I don’t even know how to start with that…).

![jaccuracyPinoutDoc](https://github.com/user-attachments/assets/4a2a566b-5c7c-425c-a14a-ba66a5440d98)
