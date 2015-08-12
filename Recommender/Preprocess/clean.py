import os
import re
import json 
import pickle
import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from rdp import RDP

workouts_dir = "/share/work/shenh1/Dataset/Endomondo/"
sports_stat_file = "../../mapAndNode/result/sports_stat.txt"

Test = False

def loadWorkout(workout_f, gps_data=False):
    """
    Parse one workout file into a dict
    ----------------------------------
    All the distance are in meters
    All the time are in seconds
    pace is seconds/km 
    """
    print "parse", workout_f
    workout = {}
    workout['fname'] = workout_f
    workout['wid'] = workout_f[workout_f.find("_")+1:workout_f.find(".")]
    with open(workout_f) as f:
        rdata = f.read()
        data = rdata.replace("'","")
        data = data.replace('"','')
        lines = data.split("\n")
        for line in lines:
            key, value = line[0:line.find(':')],line[(line.find(':')+1):]
            # convert different value to correct type
            if key == 'name':
                workout[key] = value
            if key == "distance":  # in meters
                if value.strip() == '-':
                    return None
                else:
                    dis, unit = value.strip().split(' ')
                    dis = float(dis)
                    if unit == 'mi':
                        workout['mile'] = True
                        dis = dis*1.60934
                    else:
                        workout['mile'] = False
                    workout[key] = dis*1000
            if key == "duration":
                time = 0
                hours = re.findall('([\d]*)h:',value)
                mins = re.findall('([\d]*)m:',value)
                secs = re.findall('([\d]*)s',value)
                if hours:
                    time += float(hours[0])*3600
                if mins:
                    time += float(mins[0])*60
                if secs:
                    time += float(secs[0])
                workout[key] = time
            if key == 'avg. pace':
                if value.strip() == '-':
                    workout[key] = '-'
                else:
                    pace, unit = value.strip().split(' ')
                    time = 0
                    if len(pace.split(':')) == 2:
                        mins, secs = pace.split(':')
                        time = time + float(mins)*60 + float(secs)
                        workout[key] = time
                    if len(pace.split(':')) == 3:
                        hours, mins, secs = pace.split(':')
                        time = time + float(hours)*3600 + float(mins)*60 + float(secs)
                        workout[key] = time
            if key == 'calories':
                if value.strip() == '-':
                    workout[key] = '-'
                else:
                    kcal, unit = value.strip().split(' ')                
                    workout[key] = float(kcal)
            if key == 'min. altitude':
                alt, unit = value.strip().split(' ')
                workout[key] = float(alt)
            if key == 'max. altitude':
                alt, unit = value.strip().split(' ')
                workout[key] = float(alt)
            if key == 'total ascent':
                alt, unit = value.strip().split(' ')
                workout[key] = float(alt)
            if key == 'total descent':
                alt, unit = value.strip().split(' ')
                workout[key] = float(alt)
        if gps_data:
            gps = rdata.split('\n')[-1][9:-2].strip()
            if not gps:
                return None
            else:
                gdata = json.loads(rdata.split('\n')[-1][9:-2])
                for point in gdata:
                    if 'lng' not in point or 'lat' not in point:
                        return None
                workout['gps'] = gdata 
    return workout

def getWorkoutFiles(sport):
    """Get all the workouts file for sport(Running, Cycling)"""
    with open(sports_stat_file) as f:
        data = f.read()
        lines = data.split("\n")
        for line in lines:
            count, workouts = line[line.find(':')+2:].split(' ')
            sports_type = line[0:line.find(':')]
            if sports_type.find(sport) != -1:
                workouts = workouts.split(",")
                break
        return [workouts_dir+ wo for wo in workouts]

def getSportsWorkouts(sport, gps_data = False):
    """Get all the parsed workout for sport(Running, Cycling)"""
    with open(sports_stat_file) as f:
        data = f.read()
        lines = data.split("\n")
        for line in lines:
            count, workouts = line[line.find(':')+2:].split(' ')
            sports_type = line[0:line.find(':')]
            if sports_type.find(sport) != -1:
                workouts = workouts.split(",")
                break

    all_workouts = []
    count = 0
    for workout in workouts:
        wo = loadWorkout(workouts_dir + workout, gps_data = gps_data)
        if Test:
            if count >= 2000:
                break
        if not wo: 
            continue
        all_workouts.append(wo)
        count += 1
    return all_workouts


        
def countUserWorkouts(sport):
    """Count for each user, how many workouts has been done"""
#    workout_parsed_file = "%s_parsed_workouts.data" % sport
#    if os.path.exists(workout_parsed_file):
#        with open(workout_parsed_file,'rb') as handle:
#            all_workouts = pickle.load(handle)
#    else:
#    with open(workout_parsed_file,'wb') as handle:
#        workouts = pickle.dump(all_workouts, handle)

    all_workouts = getSportsWorkouts(sport)
    n_workouts = len(all_workouts)
    print "%d %s workouts" % (n_workouts, sport)

    res = {}
    for wo in all_workouts:
        if wo['name'] in res:
            print wo['name'], 
            res[wo['name']] += 1
        else:
            res[wo['name']] = 1
    counts = sorted(res.values(), reverse=True)
    
    with PdfPages('%s_workout_counts.pdf' % sport) as pdf:
        plt.plot(range(len(counts)),counts,color='b',marker='o')
        plt.xlabel('user')
        plt.ylabel('Workout counts')
        plt.xscale('log')
        plt.title("%s %d users, %d workouts" % (sport, len(res), n_workouts))
        pdf.savefig()

def plotAllWorkouts(workouts, username, simple=False):
    """Plot all the workouts for one user"""
    if simple:
        fname = '%s_all_workouts_simple.pdf' % username.strip()
    else:
        fname = '%s_all_workouts.pdf' % username.strip()
    with PdfPages(fname) as pdf:
        for wo in workouts:
            print username, wo['fname']
            cordinates = []
            if len(wo['gps']) < 10:
                continue
            for point in wo['gps']:
                cordinates.append([point['lng'],point['lat']])
            if simple:
                cordinates = RDP(cordinates, 0.001)
            x = [point[0] for point in cordinates]
            y = [point[1] for point in cordinates]
            plt.plot(x,y)
        plt.title("%s %d workouts" % (username,len(workouts)))
        plt.xlabel('lng')
        plt.ylabel('lat')
        pdf.savefig()
        plt.clf()

def computeWorkoutsDis(a, b):
    """Compute workouts distance"""
    
    m, n = len(a['gps']),len(b['gps'])
    if abs(m - n) > 0.2*min(m, n):
        return 1

    cordia = np.zeros((m,2))
    count = 0
    for point in a['gps']:
        cordia[count,0],cordia[count,1] = point['lng'],point['lat']
        count +=1
    cordib = np.zeros((n,2))
    count = 0
    for point in b['gps']:
        cordib[count,0],cordib[count,1] = point['lng'],point['lat']
        count +=1

    if m > n:
        dis = np.linalg.norm(cordia[0:n,:] - cordib)
    else:
        dis = np.linalg.norm(cordia - cordib[0:m,:])
    return dis

def groupWorkouts(workouts):
    """Put same or similar workouts into one group"""
    n_workouts = len(workouts)
    if n_workouts == 1:
        return [workouts]

    groups = []
    avail = [True]*n_workouts
    for i in xrange(n_workouts):
        if avail[i]:
            group = [workouts[i]]
            avail[i] = False
        else:
            continue
        for j in xrange(i+1, n_workouts):
            if avail[j]:
                dis = computeWorkoutsDis(workouts[i], workouts[j])
                if dis < 0.1:
                    group.append(workouts[j])
                    avail[j] = False
        groups.append(group)
    return groups
                    
                
def countUserUniqueWorkouts(sport):
    """Count for each user, how many unique workouts has been done"""
    all_workouts = getSportsWorkouts(sport, gps_data = True)
    n_workouts = len(all_workouts)
    print "%d %s workouts" % (n_workouts, sport)
    
    # count workouts per user
    res = {}
    for wo in all_workouts:
        if wo['name'] in res:
            res[wo['name']].append(wo)
        else:
            res[wo['name']] = [wo]
    sorted_res = sorted(res.items(), key = lambda kv: len(kv[1]), reverse=True)

    # count unique workouts for each user
    counts_unique_workouts = []
    counts = []
    for name, workouts in sorted_res:
        #print name, len(workouts)
        # plot for hint
        #plotAllWorkouts(workouts, name, simple=True)
        groups = groupWorkouts(workouts)
        #print sorted([len(g) for g in groups],reverse=True)
        counts_unique_workouts.append(len(groups))
        counts.append(len(workouts))

    with PdfPages('%s_workout_counts.pdf' % sport) as pdf:
        plt.plot(range(len(counts)),counts,color='b',marker='o',label='# of workouts')
        plt.plot(range(len(counts)),counts_unique_workouts,color='r',marker='o',label='# of unique workouts')
        plt.xlabel('user')
        plt.ylabel('Workout counts')
        plt.xscale('log')
        plt.title("%s %d users, %d workouts" % (sport, len(res), n_workouts))
        plt.legend()
        pdf.savefig()

if __name__ == "__main__":
    #countUserWorkouts("Cycling")
    #countUserWorkouts("Running")
    #countUserUniqueWorkouts("Running")
    #countUserUniqueWorkouts("Cycling")
    pass
