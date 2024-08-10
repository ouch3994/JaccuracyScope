

##TODO LIST HERE 
#Reference the TestAlone WIND Script and incorporate the Wind Drift.
#Next Incorporate Spindrift and Coreilolis  (GPS? ) 


from threading import Thread 
import math 
import time 
import numpy as np
from time import strftime
import time

import serial
import adafruit_thermal_printer

import ctypes 

import DataPlotter as grapher 


class BallisticThread(Thread): 

    def __init__(self): 
    
        
        
        
        
    
        Thread.__init__(self)
        
        #need for the GNU compiled solver to run fast :) link path below 
        self.GNUballCLASS = ctypes.CDLL("/home/pi/share/Display/GNUball3.so") #compiled, after edits, recompile with     gcc -fPIC -shared -o example.so example.c -lm 
        
        self.GNUball  = self.GNUballCLASS.main
        self.GNUball.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double] 
        self.GNUball.restype = ctypes.c_double
        
        self.GNUscope  = self.GNUballCLASS.SolveforAngler
        self.GNUscope.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double] 
        self.GNUscope.restype = ctypes.c_double
        
        
        #rounds the stuff 
        self.GNUp = self.GNUballCLASS.getThePosition
        self.GNUp.argtypes = [ctypes.c_double]
        self.GNUp.restype = ctypes.c_int
        
        #handsoverXposition at target dist
        self.GNUxdistance = self.GNUballCLASS.HandMeXdistance
        self.GNUxdistance.argtypes = [ctypes.c_int]
        self.GNUxdistance.restype = ctypes.c_double
        
        #handsoverYposition at target dist
        self.GNUydistance = self.GNUballCLASS.HandMeYdistance
        self.GNUydistance.argtypes = [ctypes.c_int]
        self.GNUydistance.restype = ctypes.c_double
        
        
        #Give back MOA at target dist
        self.GNUdropMOA = self.GNUballCLASS.HandMeMOA
        self.GNUdropMOA.argtypes = [ctypes.c_int]
        self.GNUdropMOA.restype = ctypes.c_double
        
        #HandMeWindage at target dist
        self.GNUdriftWind = self.GNUballCLASS.HandMeWindage
        self.GNUdriftWind.argtypes = [ctypes.c_int]
        self.GNUdriftWind.restype = ctypes.c_double
        
        
        #hand WindageMOA
        self.GNUWindageMOA = self.GNUballCLASS.HandMeWindageMOA
        self.GNUWindageMOA.argtypes = [ctypes.c_int]
        self.GNUWindageMOA.restype = ctypes.c_double
        
        #hand net Velocity
        self.GNUVnet = self.GNUballCLASS.HandMeVelocity
        self.GNUVnet.argtypes = [ctypes.c_int]
        self.GNUVnet.restype = ctypes.c_double
        
        
        #hand net HandMeTime
        self.GNUTime = self.GNUballCLASS.HandMeTime
        self.GNUTime.argtypes = [ctypes.c_int]
        self.GNUTime.restype = ctypes.c_double
        
                
        #hand net freer
        self.GNUfree = self.GNUballCLASS.free_pointer
        self.GNUfree.argtypes = [ctypes.c_int]
        self.GNUfree.restype = ctypes.c_int
                
        
        #PRINTER SETTINGS INITIAL LOL 
        self.printerGO = False; 
        self.uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
        self.ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.0) #2.69
        self.printer = self.ThermalPrinter(self.uart)
        
        
        
        
        
        
        
        
        
        
        
        
        #self.solver = "JackSolver"
        self.solver = "GNUsolver"
                
        #drag standards sourced form https://www.alternatewars.com/BBOW/Ballistics/Ext/Drag_Tables.htm
        self.g1_cd = [0.2629,0.2558,0.2487,0.2413,0.2344,0.2278,0.2214,0.2155,0.2104,0.2061,0.2032,0.2020,0.2034,0.2165,0.2230,0.2313,0.2417,0.2546,0.2706,0.2901,0.3136,0.3415,0.3734,0.4084,0.4448,0.4805,0.5136,0.5427,0.5677,0.5883,0.6053,0.6191,0.6393,0.6518,0.6589,0.6621,0.6625,0.6607,0.6573,0.6528,0.6474,0.6413,0.6347,0.6280,0.6210,0.6141,0.6072,0.6003,0.5934,0.5867,0.5804,0.5743,0.5685,0.5630,0.5577,0.5527,0.5481,0.5438,0.5397,0.5325,0.5264,0.5211,0.5168,0.5133,0.5105,0.5084,0.5067,0.5054,0.5040,0.5030,0.5022,0.5016,0.5010,0.5006,0.4998,0.4995,0.4992,0.4990,0.4988];
        self.g1_m = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.7,0.73,0.75,0.78,0.8,0.83,0.85,0.88,0.9,0.93,0.95,0.98,1,1.03,1.05,1.08,1.1,1.13,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.45,2.5,2.6,2.7,2.8,2.9,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.2,4.4,4.6,4.8,5];
        
        
        
        self.g7_cd = [0.1198,0.1197,0.1196,0.1194,0.1193,0.1194,0.1194,0.1194,0.1193,0.1193,0.1194,0.1193,0.1194,0.1197,0.1202,0.1207,0.1215,0.1226,0.1242,0.1266,0.1306,0.1368,0.1464,0.166,0.2054,0.2993,0.3803,0.4015,0.4043,0.4034,0.4014,0.3987,0.3955,0.3884,0.381,0.3732,0.3657,0.358,0.344,0.3376,0.3315,0.326,0.3209,0.316,0.3117,0.3078,0.3042,0.301,0.298,0.2951,0.2922,0.2892,0.2864,0.2835,0.2807,0.2779,0.2752,0.2725,0.2697,0.267,0.2643,0.2615,0.2588,0.2561,0.2533,0.2506,0.2479,0.2451,0.2424,0.2368,0.2313,0.2258,0.2205,0.2154,0.2106,0.206,0.2017,0.1975,0.1935,0.1861,0.1793,0.173,0.1672,0.1618];
        self.g7_m = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.73,0.75,0.78,0.8,0.83,0.85,0.88,0.9,0.93,0.95,0.98,1,1.03,1.05,1.08,1.1,1.13,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.45,2.5,2.55,2.6,2.65,2.7,2.75,2.8,2.85,2.9,2.95,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.2,4.4,4.6,4.8,5];
        
        self.bullet_weight_grain = 150; # 
        self.bullet_weight_lbs = self.bullet_weight_grain/7000;
        self.caliber = .308; #inches
        self.bc7_box = .242;
        self.Gsolver = 7;
        self.sectional_density = self.bullet_weight_lbs/(self.caliber*self.caliber);
        self.fps_box = 2600; #fps
        self.scope_height = 1.75; #inches
        self.zerodistance = 100 #yards  100 
        
        self.Atm_altitude = 4000.0; #feet 
        self.Atm_pressure  = 29.53 #hg bar 
        self.Atm_temperature = 59.0 #Farenheight 
        self.Atm_RelHumidity = 0.30 # percent
        
        self.gunSightangle = self.GNUscope(self.bc7_box,self.fps_box,self.scope_height,0,self.zerodistance,0,0,self.Gsolver,0,0,1,self.Atm_altitude,self.Atm_pressure,self.Atm_temperature,self.Atm_RelHumidity) #0.06846618652343749 #degrees.  TO be solved for later.... 
        
        self.alpha_ini= 4.2/60;  #4.2/60;  #Angle of rifle relative to scope (Super small) adjust to zero at a distance
        
        #Recoil Analysis
        self.powder_w = 42.3/7000;  #42.3 %from https://www.powderthrough.com/data/caliber/308win/
        self.gun_w = 10.5; #10.5lbs
        self.powder_v =  self.fps_box *1.75;
        self.bul_e = 0.5*self.bullet_weight_lbs*self.fps_box*self.fps_box / 32.2;
        self.bul_i = ((self.powder_w* self.powder_v) + (self.bullet_weight_lbs*self.fps_box) )/32.2;   #lb*sec
        
        self.something1 = (self.powder_w + self.bullet_weight_lbs)*self.fps_box/self.gun_w;
        self.gun_v =  ((self.powder_w* self.powder_v) + (self.bullet_weight_lbs*self.fps_box) ) / self.gun_w;
        self.gun_e = 0.5*self.gun_w*self.gun_v*self.gun_v / 32.2;
        self.gun_i = self.gun_w * self.gun_v /32.2 ;
        
        #print("*********RECOIL CALCULATOR***********")
        #print("*Bullet Weight:" + str(bullet_weight_grain) + " gr")
        #print("*Bullet Velocity:" + str(fps_box) + " fps")
        #print("*Powder Weight:" + str(powder_w*7000) + "  gr")
        #print("*Powder Velocity:" + str(powder_v) + " fps")
        #print("*Bullet Impulse:" + str(bul_i) + " lb*sec")
        #print("*Bullet Energy:" +  str(bul_e))
        #print("*Gun velocity:" + str(gun_v) + " fps")
        #print("*Gun Impulse est:" + str(gun_i) + " lbf*s")
        #print("****************************")
        #print("*Gun Energy:" + str(gun_e) + " ft*lbs")
        #print("****************************")
        #print("*************************************")
        #
        

        
        ##Aero Conditions
        self.MachSpeed  = 343; # #fps  #sqrt rho r 1.4
        self.rho=1.225; #Air density [kg/m3]  #1.225 sea level ,  1.056 longmont
        self.S=0.0000481; #Surface [m2]
        self.cd=1.6619e6; #Drag coefficient [-] 0.9271
        self.m=self.bullet_weight_grain * 6.47989e-5;                #0.00971984; %mass [kg]
        self.g=9.8065; #gravitational acceleration [m/s2]
        self.sim_max_time = 3 ; #(seconds)
        self.tf=self.sim_max_time; #Simulation final time [s] [0:0.001:2]
        self.stepsize= 100; # 0.01
        self.dingus= self.sim_max_time/self.stepsize; 
        
        self.t0=0;
        self.BC =  0.451 *.453592  / 0.0254/0.0254  ;  #lb/in2 to kg/m^2  %209  .415 my bullets
        
        #Initial conditions
        self.V0=self.fps_box*0.3048; #Initial speed [m/s]  822.95  860 728  908ammoinc
        self.angle = math.radians(90);
        self.x0=0; #Initial x [m]
        self.y0=2; #Initial y [m]
        #Vx0=V0*math.cos(alpha_ini);
        #Vy0=V0*math.sin(alpha_ini);
        
        
        
        #Formfactor (G7 only for now)
        self.formfactor = self.sectional_density / self.bc7_box;     ######Cacluate this!     ff_g7  =  SD / BC7_from_Box   #test origianlly 1.043.. why?  ff needs mach calcs
        self.myg7=np.array(self.g7_cd)*self.formfactor ;
        self.myg1=np.array(self.g1_cd)*self.formfactor ;
        
        self.one_MOA =  1.047/100; #inches per yard
        
        self.opz_aereo_y=1; #Consider or not the aerodynamic drag along y
        
        
        #Code here run BallisticCalc 
        self.x0in  = 0.0 
        self.y0in  = 0.0 
        self.Vx0in = 1
        self.Vy0in = 1 
        self.targetdistin  = 1 
        self.elevation0in  = 1 
        
        self.MafVal = 5 #for computuing fps 
        self.fpsaveout = 0
        
        
        self.facing = 10  
        self.windinput = 0
        
        #get these from the calling script :) 
        self.windspeed = 0 #mph 
        self.wind_head_deg = 0 #degrees 
        
        
        self.dt = 0.05 #normal mode 
        
        self.T = 3 #seconds max flight time 
        
        self.ScopeMode =0;  
        self.maxheight = 0;
        
        self.GNUxSender = np.array([50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1050,1100])
        #22 long,  [0 to 21]
        
        self.GNUySender = np.zeros(len(self.GNUxSender))
        self.Toftracker = np.zeros(len(self.GNUxSender))
        self.inchdropper = np.zeros(len(self.GNUxSender))
        self.moadropper = np.zeros(len(self.GNUxSender))

        
        
        
    def printResults(self, x, pmoa, pinch, ptime):
        
        #if connected to blah blah... 
        
        print('Feeding 2 lines ') 
        self.printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
        self.printer.feed(1)
    
        self.printer.bold = True
        self.printer.print('+++++ JackScope v0.1 ++++++')
        self.printer.print('+++++ By Jack Toth ++++++')
        self.printer.print('***Atmospheric Conditions***')
        self.printer.bold = False
        self.printer.print('Alt(kft)= ' + str("{:.3f}".format(self.Atm_altitude / 1000)) + '  P(inHg)= ' + str("{:.2f}".format(self.Atm_pressure)))
        self.printer.print('Temp(F)= ' + str(int(self.Atm_temperature)) + '  Hum(%)= ' + str(int(self.Atm_RelHumidity*100)))
        self.printer.print('Lat= ' + str(39.73555) + '  Long= ' + str(104.98972))
        self.printer.feed(1)       
        self.printer.bold = True
        self.printer.print('***Bullet Statistics***')
        self.printer.bold = False
        self.printer.print('Cal(in)= ' + str("{:.3f}".format(self.caliber)) + '  Wght(gr)= ' + str(int(self.bullet_weight_grain)))
        self.printer.print('Vmuz(fps)= ' + str("{:.1f}".format(self.fps_box)) + '  G Model= ' + str(self.Gsolver))
        self.printer.print('BC= ' + str("{:.3f}".format(self.bc7_box)) + '  ZeroDist(yd)= ' + str(int(self.zerodistance)))
        self.printer.feed(1)
        
        self.printer.bold = True
        self.printer.print('*** WIND Conditions ***')
        self.printer.bold = False
        self.printer.print('Vwind(mph)= ' + str("{:.1f}".format(self.windspeed)) + 'W Dir(deg)= ' + str(int(self.wind_head_deg)))
        self.printer.feed(1)
        
        self.printer.bold = True
        self.printer.print('*** Shot Angle ***')
        self.printer.bold = False
        self.printer.print('Elevation  (deg) = ' + str("{:.1f}".format(self.elevation0in)))
        self.printer.feed(1)
        
        self.printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
        self.printer.print('*** Shot TABLE ***')
        self.printer.print('Dist(yd) Drp(MoA) Drp(in) ToF(s)')
        self.printer.print('********************************')
        for i in range(len(x)): 
            self.printer.print(str("{:4.0f}".format(x[i])) + "   " + str("{:.1f}".format(-pmoa[i])) + "    " + str("{:.1f}".format(pinch[i])) + "   " + str("{:.3f}".format(ptime[i])))
            
         #Feed lines to make visible:
        self.printer.feed(2)

        
        
    def aero(self,t,y):
    
        wind=self.windinput;
        
        
        windv = y[6];

        Vx=y[2]; 
        Vy=y[3];
        
        Vz=y[5]+wind;
        
        angle_r =  math.atan(Vy/Vx);
        Vtotal  =  math.sqrt((Vy*Vy) + (Vx*Vx)+(Vz*Vz));
        
        angle_w = math.asin(Vz/Vtotal);
        
        mach = Vtotal / self.MachSpeed; # needed fro interpolation below of CD 
    
    
        q_air = 0.5*self.rho*Vtotal*Vtotal;
        #Cd = .308; 
        Cd = np.interp(mach, self.g7_m, self.myg7); ## Linear(g7_m, myg7, 84, mach,0); #to be linear interp eventuall interp1(g7_m,myg7,mach,'linear') ..needs mach and shit //test with .308 constant
        Fdrag = q_air*Cd*self.S;
    
        Faereo_x=-Fdrag*math.cos(angle_r)*math.cos(angle_w);
        
        Faereo_z = -Fdrag*math.cos(angle_r)*math.sin(angle_w);
    
        Faereo_y = -Fdrag*math.sin(angle_r);
        
        Fgrav=-self.m*self.g;
    

        yout1=Vx;
        
        yout2=Vy;
        
        #ACCeleration calculated below 
        
        yout3=Faereo_x/self.m;
        yout4=(Faereo_y+Fgrav)/self.m;
        yout5=y[5];
        yout6=Faereo_z/self.m; 
        yout7=y[6];

        
        dy = [yout1,yout2,yout3,yout4, yout5,yout6, yout7];

        return np.array(dy) # function to be solved    
        
        
 
    def rk4(self,func,dt,t0,y0):
    
        
        f1 = func(t0,y0)
        f2 = func(t0 + dt / 2, y0 + (dt/2) *f1)
        f3 = func(t0 + dt / 2, y0 + (dt/2) *f2)
        f4 = func(t0 + dt, y0 + dt * f3)
        yout = y0 + (dt/6) * (f1 + (2*f2) + (2*f3) + f4)

        return yout
        
        
        
    def solveBallistics(self, x0,y0,Vx0,Vy0,dist_targ, elevation0, windinput , dt, T , scopermode):
    
    # Inputs
        y00 = [x0, y0, Vx0, Vy0, 0, 0, windinput]; #computed way abovelol
    
        #print("-----------RESULTS----------")
        #print(y0)
        
        # if (dist_targ>600):
        #     dt = 0.05;  #more accurate above 600 meters, longer to solve 
        # else:
        #     dt = 0.05;  #less accurate below 600 meters, faster solve 
        # 
         # T=3; #max time 
         
        num_time_pts = int(T/dt);
        t = np.linspace(0,T,num_time_pts+1);
        
        Y = np.zeros((7, num_time_pts))
        
        outputY = np.zeros((num_time_pts+1))           #both these were -1 
        outputDrop =  np.zeros((num_time_pts+1))
        outputheight = np.zeros((num_time_pts+1))        
        
        Y[:,0] = y00;
        yin = y00;
        
        start_time = time.time();
        
        yout = [0,0,0,0,0,0,0]
        j=0; 
        
        
        
        if (scopermode == 0):
            for i in range(num_time_pts -1):
            
                #stop calcing after we have gotten close to the target distance.... change to past, and interpolate. 
                # RK4 method call
                
                if (math.sqrt(yout[0]*yout[0]) + (yout[1]*yout[1]) <= dist_targ):
                    
                    yout =  self.rk4( self.aero, dt, t[i], yin)
                    Y[:, i+1] = yout;
                    yin = yout;
                    
                    
                    outputY[i+1]= yout[0]*1.09361
                    
                    outputheight[i+1]= yout[1]*1.09361 #yards 
                    
                    outputDrop[i+1]= (yout[1]-y0)*39.3701
                    
                    
                    
                    #if wnt wind plotter need to be here 
            
            #print(yout[3])
            #create a real time plot of the dots within a bounded area image 
            
            #print(yout)
            self.maxheight = np.max(outputheight)
            plot = grapher.plotme(outputY,outputDrop,dist_targ, 0);   

        if (scopermode == 1): #lobster mode! 
            for i in range(num_time_pts -1):
            
                #stop calcing after we have gotten close to the target distance.... change to past, and interpolate. 
                # RK4 method call
                
                if (yout[1] >= (y0-.1)):
                    
                    yout =  self.rk4( self.aero, dt, t[i], yin)
                    Y[:, i+1] = yout;
                    yin = yout;
                    
                    
                    outputY[i+1]= yout[0]*1.09361
                    
                    outputheight[i+1]= yout[1]*1.09361 #yards 
                    
                    outputDrop[i+1]= (yout[1]-y0)*39.3701
                    
                    #if wnt wind plotter need to be here 
            
        
            #create a real time plot of the dots within a bounded area image 
            
            #print(yout)
            
            self.maxheight = np.max(outputheight)
            plot = grapher.plotme(outputY,outputDrop,dist_targ, 1);  #big plot lol 
            
            
        if (scopermode == 2): #settings 
            time.sleep(0.3)  #do nothing while in the settings mode.
            self.gunSightangle = self.GNUscope(self.bc7_box,self.fps_box,self.scope_height,0,self.zerodistance,0,0,self.Gsolver,0,0,1,self.Atm_altitude,self.Atm_pressure,self.Atm_temperature,self.Atm_RelHumidity)    
            
            #debugging 
            print("  A:" +  str(self.Atm_altitude)+"  P:" +  str(self.Atm_pressure)+"  T:" +  str(self.Atm_temperature)+"  H:" +  str(self.Atm_RelHumidity))
            print(str(self.gunSightangle))

                    

        return yout, plot
        
            
            
    def run(self):
        #time.sleep(0.5)
        
        while True: 
            

            
            
            
            #Get a frame : 
            fpsave=0 
            
                  
            
            #moving Average Filter 
            for i in range (1,self.MafVal+1,1): 
            
            
                t_start = time.time()
                
                #Code here run BallisticCalc 
                x0 = self.x0in  
                y0 = self.y0in 
                Vx0 = self.Vx0in 
                Vy0 = self.Vy0in 
                targetdist = self.targetdistin
                elevation0 = self.elevation0in  
                

                #WIND! 
                
                windspeed_mps = self.windspeed * 0.44704;
                wind_head_deggies = (self.facing - self.wind_head_deg) 

                wind_head_rad = (self.facing - self.wind_head_deg) / 57.2958 #now radians  
                
                
                self.windinput = windspeed_mps * math.sin(wind_head_rad);  
                
             
                
                
                if  (self.solver == "GNUsolver"):
                
                    if (self.ScopeMode == 0 ):
                        #Solve with the GNU program.... C based. Compiled.
                        
                        #need solution to be  [distanceM, heightM, Vxmps, Vymps, windriftMeters, zspeed(notused), notused] 
                        #need solver to pass an array of trajectory if we want to plot it....   array? how... ? 
                        
                        #extra wind shit because algoritim....
                        
                        
                        speedofwind = (self.windspeed * math.sin(wind_head_rad)); #equals to the acrossness of wind input always exact 90. 
                        
                        
                        
                        #GNUball( double bc, double v, double sh,double angle, double zero,double windspeed, double windangle, int G , double zeroanglein, double targetDistance, int justangle)
                        dingusss = self.GNUball(self.bc7_box,self.fps_box,self.scope_height,elevation0,self.zerodistance,self.windspeed,wind_head_deggies,self.Gsolver,self.gunSightangle,targetdist,0,self.Atm_altitude,self.Atm_pressure,self.Atm_temperature,self.Atm_RelHumidity) #get results
                        
                        
                        position = self.GNUp(targetdist*1.09361) #roudns for us 
                        #Xposition at target dist
                        distancex  = self.GNUxdistance(position)
                        #Yposition at target dist               
                        distancey  = self.GNUydistance(position)
                        #Give back MOA at target dist               
                        MOAdroper = self.GNUdropMOA(position)
                        #Windage at target dist
                        Winddriffft = self.GNUdriftWind(position)
                        #WindageMOA
                        Windagemoaa = self.GNUWindageMOA(position)
                        #hand net Velocity
                        netV = self.GNUVnet(position)
                        #hand net HandMeTime
                        timesolveddist = self.GNUTime(position)
                        
                        
                        Windagemoaa = Winddriffft / (distancex *1.047 / 100);
                        
                        
                        
                        
                        self.solution = [distancex,distancey ,netV,Winddriffft,Windagemoaa,timesolveddist, -dingusss] #the c binary is not compiled yet to do th eright shit.... fukkk man 
    
                        for i in range (len(self.GNUxSender)):
                            #thisposition = self.GNUp(self.GNUxSender[i]*1.09361) #whats hapening here...?  #####
                            #self.GNUySender[i] = self.GNUydistance(thisposition)-distancey
                            thisposition = self.GNUp(self.GNUxSender[i]*1.09361) #whats hapening here...?  #####
                            self.GNUySender[i] = (math.tan(elevation0/57.2958)*self.GNUxSender[i]*36) +  self.GNUydistance(thisposition)-distancey
                        
                        
                        if (self.printerGO == True):
                            for i in range (len(self.GNUxSender)):
                                thisposition = self.GNUp(self.GNUxSender[i]) #yyards to position #whats hapening here...? 
                                self.moadropper[i] = self.GNUdropMOA(thisposition) #moa
                                self.inchdropper[i] = self.GNUydistance(thisposition) #in
                                self.Toftracker[i] = self.GNUTime(thisposition) #sec 
                                
                                 

                            self.printResults(self.GNUxSender,self.moadropper, self.inchdropper, self.Toftracker); #insert settings here... 
                            self.printerGO = False
                        


                        

                        #### FRee all memory because shitttt man you dont wanna burn out the ram overload
                        self.GNUfree(1)
                        # Fake Plot for now (small plot) 
                        self.plotter  =  plot = grapher.plotme(self.GNUxSender,self.GNUySender,targetdist, 0);  #mode 0 for regular solving 
                        

                        
                        
                        
                        time.sleep(0.05) #throttle CPU ussage
                        
                    elif(self.ScopeMode == 2 or self.ScopeMode == 4):
                        time.sleep(0.3)  #do nothing while in the settings mode.
                        self.gunSightangle = self.GNUscope(self.bc7_box,self.fps_box,self.scope_height,0,self.zerodistance,0,0,self.Gsolver,0,0,1,self.Atm_altitude,self.Atm_pressure,self.Atm_temperature,self.Atm_RelHumidity)    
                
                        #debugging 
                        print("  A:" +  str(self.Atm_altitude)+"  P:" +  str(self.Atm_pressure)+"  T:" +  str(self.Atm_temperature)+"  H:" +  str(self.Atm_RelHumidity))
                        print(str(self.gunSightangle))
                        
                    else:
                        time.sleep(0.5)
                        #do nothing else lol 
                        
                        
                    
                    
                    
                else:     #self.solver = "JackSolver"  
                    
                    self.solution , self.plotter =   self.solveBallistics(x0,y0,Vx0,Vy0,targetdist, elevation0, self.windinput, self.dt, self.T , self.ScopeMode)
                    
                    time.sleep(0.05) ###reallly controls display FPS ... needs throttle 0.05
              
                
                #outputs:
           
                t_end = time.time()
                fps = -1/(t_start - t_end)
                fpsave = fpsave + (fps/self.MafVal)
                
                #print(output_accZ)
                
                
                
            #fpsave = fpsave/20
            self.gunSightangle = self.GNUscope(self.bc7_box,self.fps_box,self.scope_height,0,self.zerodistance,0,0,self.Gsolver,0,0,1,self.Atm_altitude,self.Atm_pressure,self.Atm_temperature,self.Atm_RelHumidity) #0.06846618652343749 #degrees.  TO be solved for later.... 
        
            self.fpsaveout = fpsave
            

            
            

#def getFrame(obj): 
#    
#        image = thread.imageout
#    
#    
#    return image #send this to the main program 
#


            
thread = BallisticThread()
thread.start()

