# Importing all needed modules
import multiprocessing
from multiprocessing.pool import ThreadPool
import time, timeit
import os
import subprocess

#pid = str(os.getpid()) #get the pid for this task
#cmd = "psrecord " + pid + " --log oceanMistClose.txt --interval 10 --plot oceanMistClose.png " #builds the string to run
#p = subprocess.Popen(cmd,shell=True) #launches subprocess
# Starting timer for Parent measurement
start_time = timeit.default_timer()

hou.hipFile.load("/home/tricecold/pythonTest/HoudiniWedger/HoudiniWedger.hiplc")
wedger =   hou.parm('/obj/geo1/popnet/source_first_input/seed')
cache = hou.node('/out/cacheme')
total_tasks = 24
max_number_processes = 8
fileRange =  abs(hou.evalParmTuple('/out/cacheme/f')[0] - hou.evalParmTuple('/out/cacheme/f')[1])
target_dir = os.path.dirname(hou.evalParm('/out/cacheme/sopoutput')) + "/"

# Define the function which will be executed within the ThreadPool
def cacheHoudini(wedge=total_tasks):
    wedger.set(wedge)
    cache.render(verbose=False)
    print('\tWorker maximum memory usage: %.2f (mb)' % (current_mem_usage()))
    
if __name__ == '__main__':
    
    pool = multiprocessing.Pool(max_number_processes)
    
    for wedge in range(0,total_tasks):
        pool.apply_async(cacheHoudini,args=(wedge,))
        
    #pool.apply_async(files,args=(target_dir,))    
    pool.close() # After all threads started we close the pool
    pool.join() # And wait until all threads are done
    del pool

print("Parent: this Process ran %s seconds" % str(timeit.default_timer() - start_time))

