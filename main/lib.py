import alt_proc_path
from _import import *

def fatal(msg):

    print('Fatal:', msg)
    raise HTTPException(status_code=461, detail=msg)

