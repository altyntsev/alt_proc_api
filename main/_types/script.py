from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import Field
from alt_proc.types import Strict
from datetime import datetime


class Script_script_id(Strict):
    script_id: Optional[int] = Field(
        None,
        title='Script ID'
    )

class Script_proc_id(Strict):
    proc_id: Optional[int] = Field(
        None,
        title='Proc ID'
    )

class Script_iscript(Strict):
    iscript: Optional[int] = Field(
        None,
        title='Serial script number in processing',
        # language=YAML
        description='''
            Starting with 0.
        '''
    )

class Script_script(Strict):
    script: Optional[str] = Field(
        None,
        title='Relative script path',
        # language=YAML
        description='''
            Relative to main dir
        '''
    )

class Script_name(Strict):
    name: Optional[str] = Field(
        None,
        title='Name label',
        # language=YAML
        description='''
            Used for labeling script in GUI and working dir
        '''
    )

class Script_status(Strict):
    status: Optional[Literal['WAIT', 'NEXT', 'RUN', 'DONE']] = Field(
        None,
        title='',
        # language=YAML
        description='''
            WAIT: waiting to start
            NEXT: waiting until previous scripts will be done
            DONE: script finished
        '''
    )

class Script_result(Strict):
    result: Optional[Literal['SUCCESS', 'FATAL', 'ERRORS']] = Field(
        None,
        title='',
        # language=YAML
        description='''
            None: Script is not finished yet
            SUCCESS: Script is successful
            FATAL: Script failed
            ERRORS: Script is finished with errors
        '''
    )

class Script_last_run_id(Strict):
    last_run_id: Optional[int] = Field(
        None,
        title='Last Run ID',
        # language=YAML
        description='''
            ID of last script execution 
        '''
    )

class Script_resources(Strict):
    resources: Optional[Any] = Field(
        None,
        title='Resourses occupied by script',
        # language=YAML
        description='''
            Dictionary 
                key: arbitrary resourse name
                value: arbitrary occupied resourse value 
        ''',
        example = {'access': 2}
    )

class Script_stime(Strict):
    stime: Optional[datetime] = Field(
        None,
        title='Start time'
    )

class Script_etime(Strict):
    etime: Optional[datetime] = Field(
        None,
        title='End time'
    )

class Script_n_runs(Strict):
    n_runs: Optional[int] = Field(
        None,
        title='Script execution count'
    )



class Script(
    Script_n_runs,
    Script_etime,
    Script_stime,
    Script_resources,
    Script_result,
    Script_status,
    Script_name,
    Script_script,
    Script_iscript,
    Script_proc_id,
    Script_script_id
):
    pass