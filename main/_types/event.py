from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import Field
from alt_proc.types import Strict
from datetime import datetime


class Event_event_id(Strict):
    event_id: Optional[int] = Field(
        None,
        title='Event ID'
    )

class Event_task_id(Strict):
    task_id: Optional[int] = Field(
        None,
        title='Task ID',
        # language=YAML
        description='''
        '''
    )

class Event_title(Strict):
    title: Optional[str] = Field(
        None,
        title='Title (label)',
        # language=YAML
        description='''
            Used for GUI only
        '''
    )

class Event_ctime(Strict):
    ctime: Optional[datetime] = Field(
        None,
        title='Creation time'
    )

class Event_status(Strict):
    status: Optional[Literal['WAIT', 'USED']] = Field(
        None,
        title='Event status',
        # language=YAML
        description='''
            WAIT: Event is waiting
            USED: Event is used for processing. 
        '''
    )

class Event_params(Strict):
    params: Optional[Any] = Field(
        None,
        title='Event parameters',
        # language=YAML
        description='''
            Parameters will be used by processing
        '''
    )

class Event(
    Event_params,
    Event_status,
    Event_ctime,
    Event_title,
    Event_task_id,
    Event_event_id
):
    pass