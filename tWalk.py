import os
import sys
import threading
import Queue

class walkThread(threading.Thread):
    workq = Queue.Queue()
    result = None # assignment states that user will initialize this
    resultLock = None # initialized in tWalk()

    def __init__(self, startdir):   # store current directory
        threading.Thread.__init__(self)
        self.startdir = startdir

    def classftn(cls, fl):  # class method to be overridden
        print "class"

    def run(self):
        while 1:
            try:
                work = walkThread.workq.get(False)
            except:
                break

            fullpath = os.path.join(os.path.abspath('.'), work)

            if(os.path.isdir(fullpath)): #if directory
                os.chdir(work)
                contains = os.listdir('.')
                if (contains): #if directory is not empty
                    for content in contains:
                        walkThread.workq.put(os.path.join(fullpath,content))

            else: # else task is a file
                # apply fxn to file (task)
                walkThread.resultLock.acquire()
                walkThread.classftn(work)
                walkThread.resultLock.release()

def twalk(startdir, fileftn, nthreads):
    threadList = []    # list of threads for j.join() later
    walkThread.classftn = classmethod(fileftn)  # dynamically creating a class method
    walkThread.resultLock = threading.Lock()
    walkThread.workq.put(startdir)

    for i in range(nthreads):
        walker = walkThread(startdir)
        walker.start()
        threadList.append(walker)

    for thread in threadList:
        thread.join()
