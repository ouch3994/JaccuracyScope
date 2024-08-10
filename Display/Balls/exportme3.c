#include <stdio.h>
#include "ballistics.h"


double* sln;


double main( double bc, double v, double sh,double angle, double zero,double windspeed, double windangle, int G , double zeroanglein, double targetDistance, int justangle, double altitude, double pressure, double temperature, double relHum)
{
	int k=0;
	//double* sln;
	//gcc -fPIC -shared -o example.so example.c -lm to compile for python 
	// A pointer for receiving the ballistic solution.
	//double bc=0.242; // The ballistic coefficient for the projectile.
	//double v=2600; // Intial velocity, in ft/s
	//double sh=1.75; // The Sight height over bore, in inches.
	//double angle=0; // The shooting angle (uphill / downhill), in degrees.
	//double zero=100; // The zero range of the rifle, in yards.
	//double windspeed=0; // The wind speed in miles per hour.
	//double windangle=0; // The wind angle (0=headwind, 90=right to left, 180=tailwind, 270/-90=left to right)
	
	// If we wish to use the weather correction features, we need to 
	// Correct the BC for any weather conditions.  If we want standard conditions,
	// then we can just leave this commented out.
	
	bc=AtmCorrect(bc, altitude, pressure, temperature,relHum);
	
		
	
	if (justangle == 0) {
	if (G == 1) {

	
	
	// Now we have everything needed to generate a full solution.
	// So we do.  The solution is stored in the pointer "sln" passed as the last argument.
	// k has the number of yards the solution is valid for, also the number of rows in the solution.
	k=SolveAll(G1,bc,v,sh,angle,zeroanglein,windspeed,windangle,&sln);
	
	
	}
	
	else if(G == 7){

	
	// Now we have everything needed to generate a full solution.
	// So we do.  The solution is stored in the pointer "sln" passed as the last argument.
	// k has the number of yards the solution is valid for, also the number of rows in the solution.
	k=SolveAll(G7,bc,v,sh,angle,zeroanglein,windspeed,windangle,&sln);		
	
	}
	
	// Now print a simple chart of X / Y trajectory spaced at 10yd increments lets do every hmm
	int s=0;
	double dropresult = 0.0;
	double Yardageout[21];
	double MOAout[21];
	double OUTPUTresult[7];
	double targetDistanceYard;
	int Distdesired; 
	
	for(s=0;s<=100;s++){
		

		
		//Every 50 25 yards, plot a point to output vector y yard and    need OUTPUTY meters and OUTPUTdropMeters 
			
		if (s == 5 || s == 10 ||s == 15 ||s == 20 ||s == 25 ||	s == 30 ||s == 35 ||s == 40 ||s == 45 ||	s == 50 ||s == 55 ||s == 60 ||s == 65 ||	s == 70 ||s == 75 ||s == 80 ||s == 85 ||	s == 90 ||s == 95 || s == 100 ) 
		{
		Yardageout[(s/5)] = (GetRange(sln,s*10));
		MOAout[(s/5)] = (float)(GetPath(sln,s*10));
		}
		//printf("\nX: %.0f     Y: %.2f        MOA : %.2f",GetRange(sln,s*10), GetPath(sln,s*10), (GetPath(sln,s*10) / ((GetRange(sln,s*10)/100)*1.047)) );
		
		//Generate an array of results. and the result at the target distance. only as side return. 
		//need solution to be  [distanceM, heightM, Vxmps, Vymps, windriftMeters, zspeed(notused), notused]
	}	//loops 
		
		
		
		//At targetDistance, interpolate the results from MOAout 
		targetDistanceYard = targetDistance *1.09361; 
		//round to nearest 
		Distdesired =((int)(targetDistanceYard / 10 ) * 10)+10; // hehehe 
		
		if ((Distdesired - (int)targetDistanceYard) >= 5){
			Distdesired = Distdesired -10;
		} 
		
		
		
		
		OUTPUTresult[0]  =  (GetRange(sln,Distdesired) *0.9144);      //  yd 2 m distanceM   
		OUTPUTresult[1]  =  (GetPath(sln,Distdesired) *0.0254);       //   in to heightM
		OUTPUTresult[2]  =  (GetRange(sln,Distdesired) *0.3048);        // ft 2 m Vxmps
		OUTPUTresult[3]  =  (GetVy(sln,Distdesired) *0.3048);       //   ft 2 m Vymps
		OUTPUTresult[4]  =  (GetWindage(sln,Distdesired) *0.9144);       //   windriftMeters
		OUTPUTresult[5]  =  0  ;     //   zspeed(notused)
		OUTPUTresult[6]  =  (GetMOA(sln,Distdesired))  ;    //   notused  use for MOA actual 
		
		
		
		//(GetPath(sln,100*10) / ((GetRange(sln,100*10)/100)*1.047)); example results 
		
			
		
		
		// cant return OUTPUTresult , Yardageout, 	MOAout;  more than one outputlol 
	return  (GetMOA(sln,Distdesired)) ; //((double)Distdesired); //
	
	
	
	
	
	

		

	

	} // end of justangle == 0 


} //end main 











double SolveforAngler( double bc, double v, double sh,double angle, double zero,double windspeed, double windangle, int G , double zeroanglein, double targetDistance, int justangle, double altitude, double pressure, double temperature, double relHum)
{
	

	 //bc=AtmCorrect(bc, 0, 29.53, 59,.78);
	 bc=AtmCorrect(bc, altitude, pressure, temperature,relHum);
	
	// First find the angle of the bore relative to the sighting system.
	// We call this the "zero angle", since it is the angle required to 
	// achieve a zero at a particular yardage.  This value isn't very useful
	// to us, but is required for making a full ballistic solution.
	// It is left here to allow for zero-ing at altitudes (bc) different from the
	// final solution, or to allow for zero's other than 0" (ex: 3" high at 100 yds)
	double zeroangle=0;
	
	if (justangle == 1) {
		
		if (G == 1) {
			zeroangle=ZeroAngle(G1,bc,v,sh,zero,0);
	
	
			return zeroangle;
		}
		
		else {
			zeroangle=ZeroAngle(G7,bc,v,sh,zero,0);
	
	
			return zeroangle;
		}
	
	}

	
}



//Return Results Sepeartely to Pyhton... These have to be sepereated.... usefulshit tho.
//The ballistics must be solved prior to being able to retrieve any of these.... 

//Determine the position of solution to return. 
int getThePosition(double targetDistanceYard){
	
	
	//Rounds to 10 yard placements 
	//int distanceYards =((int)(targetDistanceYard / 10 ) * 10)+10; // hehehe 
	//	
	//	if ((distanceYards - (int)targetDistanceYard) >= 5){
	//		distanceYards = distanceYards -10;
	//	} 
	
	
	//Rounds to nearest yard placement 
	int distanceYards =(int)targetDistanceYard ;
	
	
	//fprintf("%.2f",targetDistanceYard)
	//printf("Buttholes!!    %.2f",targetDistanceYard);
	//printf("\nButtholes2!!    %i",distanceYards);
	
	return distanceYards; 
}




double HandMeXdistance(int pos){
	return (GetRange(sln,pos));
}


double HandMeYdistance(int pos){
	return (GetPath(sln,pos));
}


double HandMeMOA(int pos){
	return (GetMOA(sln,pos));
}


double HandMeWindage(int pos){
	return (GetWindage(sln,pos));
}


double HandMeWindageMOA(int pos){
	return (GetWindageMOA(sln,pos));
}


double HandMeVelocity(int pos){
	return (GetVelocity(sln,pos));
}

double HandMeTime(int pos){
	return (GetTime(sln,pos));
}

int free_pointer(int hi){
	
	free(sln);
	
	return 0; 
}

