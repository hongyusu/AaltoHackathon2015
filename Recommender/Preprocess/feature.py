import numpy as np
import scipy.stats as ss

from clean import loadWorkout, getWorkoutFiles
from rdp import RDP


def movingAverage(values,window):
    if window == 0:
        return np.array(values)
    weigths = np.repeat(1.0, window)/window    
    smoothed = np.convolve(values, weigths, 'valid')
    return smoothed 

def getTripFeature(workout):
    if workout is None:
        return None
    gps = []
    duration = []
    distance = []
    if workout['mile']:
        for point in workout['gps']:
            gps.append([point['lng'],point['lat']])
            try:
                duration.append(point['values']['duration']/1000)        
                distance.append(point['values']['distance']*1.60934*1000)
            except KeyError:
                return None
    else:
        for point in workout['gps']:
            gps.append([point['lng'],point['lat']])
            try:
                duration.append(point['values']['duration']/1000)        
                distance.append(point['values']['distance']*1000)
            except KeyError:
                return None

    gpsSimple = RDP(gps, 0.001)


    #################
    # Routes features

    totalDistance = workout['distance']
    totalAscent = workout.get('total ascent', float('nan'))
    totalDescent = workout.get('total descent', float('nan'))
    minAltitude = workout.get('min. altitude',float('nan'))
    maxAltitude = workout.get('max. altitude',float('nan'))
    numTurns = len(gpsSimple)

    ##################################
    # Route Human interaction features
    # Use most of the code from
    # https://github.com/PrincipalComponent/AXA_Telematics/blob/master/ \
    # Features/modules_janto/featureFun.py

    # 1. Time
    totalTime = duration[-1]
    gps = np.array(gps)

    # 2.speed
    try:
        speed = map(lambda x,y: x*1.0/y, distance[1:], duration[1:])
    except ZeroDivisionError:
        return None

    # smooth speed, in our datasets is not necessary because the 15s interval
    smooth_speed =  movingAverage(speed,0)

    # compute speed statistics    
    mean_speed = smooth_speed.mean()
    min_speed = min(smooth_speed)
    max_speed = max(smooth_speed)
    std_speed = smooth_speed.std()

    # 3. acceleration
    smooth_accel = np.diff(smooth_speed)  
    accel_s = np.array(smooth_accel)
    # 3.1 get all negative acceleration values
    neg_accel = accel_s[accel_s<0]
    pos_accel = accel_s[accel_s>0]
    # 3.2 average breaking strength
    mean_breaking = neg_accel.mean()
    # 3.3 average accelaration strength
    mean_acceleration = pos_accel.mean()
    # summary statistics
    std_breaking = neg_accel.std()
    std_acceleration = pos_accel.std()     

    # 4. speed and accelaration quantiles
    speed_quantiles = ss.mstats.mquantiles(smooth_speed, 
                                           np.linspace(0.02,0.99,25)) 
    accel_quantiles = ss.mstats.mquantiles(smooth_accel,
                                           np.linspace(0.02,0.99,25))

    return np.concatenate((np.array([totalDistance, totalAscent, totalDescent,
                                    minAltitude, maxAltitude, numTurns,
                                    totalTime, mean_speed, min_speed, 
                                    max_speed, std_speed, mean_breaking,
                                    mean_acceleration, std_breaking, 
                                    std_acceleration]),
                           speed_quantiles, accel_quantiles))


    
if __name__ == "__main__":
    all_workouts = getWorkoutFiles("Running")
    usernames = []
    featmat = []
    for workout_f in all_workouts:
        workout = loadWorkout(workout_f, gps_data=True)
        feat = getTripFeature(workout)
        if feat is not None:
            usernames.append(workout['name'])
            featmat.append(feat)
    n_samples = len(usernames)
    featmat = np.array(featmat)
    usernames = np.array(usernames)
    np.savetxt('running_feature.txt',featmat)
    w = open('running_users.txt','w')
    w.write("\n".join(usernames))
    w.close()


    
