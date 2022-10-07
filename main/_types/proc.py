from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import Field
from alt_proc.types import Strict
from datetime import datetime


class Proc_proc_id(Strict):
    proc_id: Optional[int] = Field(
        None,
        title='Proc ID'
    )

class Proc_status(Strict):
    status: Optional[Literal['WAIT', 'RUN', 'DONE', 'DELETED']] = Field(
        None,
        title='Processing status',
        # language=YAML
        description='''
            WAIT: Processing is waiting
            RUN: Processing is running
            DONE: Processing is finished
            DELETED: Processing is deleted
        '''
    )

class Proc_result(Strict):
    result: Optional[Literal['SUCCESS', 'FATAL', 'ERRORS']] = Field(
        None,
        title='Res of the processing',
        # language=YAML
        description='''
            None: Processing is not finished yet
            SUCCESS: Processing is successful
            FATAL: Processing is failed
            ERRORS: Processing is finished with errors
        '''
    )

class Proc_event_id(Strict):
    event_id: Optional[int] = Field(
        None,
        title='Event ID'
    )

class Proc_ctime(Strict):
    ctime: Optional[datetime] = Field(
        None,
        title='Creation time'
    )

class Proc_stime(Strict):
    stime: Optional[datetime] = Field(
        None,
        title='Start time'
    )

class Proc_etime(Strict):
    etime: Optional[datetime] = Field(
        None,
        title='End time'
    )

class Proc_mtime(Strict):
    mtime: Optional[datetime] = Field(
        None,
        title='Modification time'
    )

class Proc_run_at(Strict):
    run_at: Optional[datetime] = Field(
        None,
        title='Time to run',
        # language=YAML
        description='''
            Processing will wait until specified time.
            Used for PERIODIC tasks and for processing restart on error. 
        '''
    )

class Proc_os_pid(Strict):
    os_pid: Optional[int] = Field(
        None,
        title='Processing operation system process PID',
        # language=YAML
        description='''
            Saved with every script run.
            Used to control run on abnormal termination and for killing run.
        '''
    )

class Proc_data(Strict):
    data: Optional[Any] = Field(
        None,
        title='User data',
        # language=YAML
        description='''
            Can be used to store some user data for exchange between scripts or processings.
        '''
    )

class Proc(
    Proc_proc_id,
    Proc_event_id,
    Proc_status,
    Proc_result,
    Proc_ctime,
    Proc_stime,
    Proc_etime,
    Proc_mtime,
    Proc_run_at,
    Proc_os_pid,
    Proc_data
):
    pass