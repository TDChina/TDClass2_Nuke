from multiprocessing.dummy import Pool
import os, shutil

source = "/Volumes/Seagate/vfxstorage/plate/td2/010/0010/plate/bg01/v001/fullres"
dest = "/Volumes/Seagate/vfxstorage/plate/td2/010/0010/plate_retime"
files = os.listdir(source)


def mapFunc(i):
    shutil.copy2(os.path.join(source, i), os.path.join(dest, i))


try:
    p = Pool(16)
    p.map(mapFunc, files)
    p.close()
    p.join()
    print "Finished!"
except:
    print "Wrong!"
