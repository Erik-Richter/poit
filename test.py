import os
fuj = '[{"t": 1681669003.4505951, "x": 1, "y": -0.7568024953079282, "z": -0.6536436208636119}, {"t": 1681669005.458907, "x": 2, "y": -0.9589242746631385, "z": 0.28366218546322625}, {"t": 1681669007.4621482, "x": 3, "y": -0.27941549819892586, "z": 0.960170286650366}, {"t": 1681669009.4862456, "x": 4, "y": 0.6569865987187891, "z": 0.7539022543433046}, {"t": 1681669011.4880652, "x": 5, "y": 0.9893582466233818, "z": -0.14550003380861354}]'



# folder path
dir_path = r'/home/tms123/Downloads/flask9/static/files'
count = 0
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
fo = open("static/files/test"+str(count)+".txt","w")    
fo.write("%s\r\n" %fuj)
