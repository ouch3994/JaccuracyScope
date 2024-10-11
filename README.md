# Jaccuracy Scope
![LoadingScreen2](https://github.com/user-attachments/assets/c57eea87-c5b9-470f-856e-7e7c130cc388)

Thank you for your interest in the Jaccuracy Scope Project!  There is a donation page link to the right if you support this project [Buy Me A Coffee Page](https://buymeacoffee.com/jaccuracyscope). 

The First Video Overview of the project: [Video Introduction](https://youtu.be/HgzltnaVOiY?si=L6nHdwi97msg5Pw5)
Hackaday Article: [Hackaday](https://hackaday.io/project/193031-jaccuracy-scope)
Element-14 Article: [Element-14](https://community.element14.com/products/raspberry-pi/raspberrypi_projects/b/blog/posts/a-diy-pi-ballistic-smart-scope)

![piscope](https://github.com/user-attachments/assets/f6926fb6-95f0-497f-baee-cb35fe6f75c5)


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



# Example Images
![Z_testImage271691202858 2353685](https://github.com/user-attachments/assets/8ea5a688-8321-4bd6-b4a4-8bdf02f1c21b)
![Z_testImage271691202865 5513597](https://github.com/user-attachments/assets/f9413376-f0d3-4573-8bb3-f28f060447b2)
![Z_testImage271691202868 0333173](https://github.com/user-attachments/assets/3709839b-ee0d-4b56-a6c4-71a1fe163fb3)
![Z_testImage271691202873 1352634](https://github.com/user-attachments/assets/786ea88e-12ee-451f-9093-233692934cfd)
![Z_testImage271691203231 064795](https://github.com/user-attachments/assets/70e4516e-2513-469e-a9b5-6ffc52dad7d1)
