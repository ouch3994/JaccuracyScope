import ballistics_test as ballistic
import time 




startheight  = 2 #meters 
distance = 485.0
angle = 4/60  #minutes of angle degrees TBD





t_start = time.time()


solution = ballistic.solveBallistics(x0=0,y0=startheight,Vx0=795.0,Vy0=.05,dist_targ = distance) #takes lots of time . need paralell
dropmoa = ((solution[1]-startheight)*39) * 91.44 / (solution[0] * 1.047)  #returns moa drop 

t_end = time.time()

fps = -1/(t_start - t_end)

print(fps)