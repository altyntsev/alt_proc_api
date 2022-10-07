from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import Field
from alt_proc.types import Strict
from datetime import datetime


class Task_task_id(Strict):
    task_id: Union[int, Literal['new']] = Field(
        None,
        title='Task ID'
    )


class Task_type(Strict):
    type: Optional[Literal['EVENT', 'PERIODIC']] = Field(
        None,
        title='Task type',
        # language=YAML
        description='''
        EVENT: Processing is raised from event
        PERIODIC: Processing is raised periodically
        '''
    )


class Task_project(Strict):
    project: Optional[str] = Field(
        None,
        title='Project name',
        # language=YAML
        description='''
        All project code must be in /alt_proc/projects/{project}/main folder. 
    ''')


class Task_name(Strict):
    name: Optional[str] = Field(
        None,
        title='Unique task name',
        # language=YAML
        description='''
        Task config must be in file:
        /alt_proc/projects/{project}/main/_cfg/{name}.task
    ''')


class Task_status(Strict):
    status: Optional[Literal['ACTIVE', 'PAUSE', 'FATAL', 'DELETED', 'DEBUG']] = Field(
        None,
        title='Task status',
        # language=YAML
        description='''
        ACTIVE: Task active
        PAUSE: Task paused (scripts not started)
        FATAL: Task was stopped because exceeding max fatal limit
        DELETED: Task was deleted (still in DB)
        DEBUG: Task was stopped because of debugging was detected  
    ''')


class Task_period(Strict):
    period: Optional[int] = Field(
        None,
        title='Period for periodic task (minutes)',
        # language=YAML
        description='''
        Time Period between processing starts of periodic task.
        min: 1 minute
    ''')


class Task_priority(Strict):
    priority: Optional[int] = Field(
        None,
        title='Task priority',
        # language=YAML
        description='''
            Processings with higher priority done in first order.
            Not influence on periodic tasks.
        ''')


class Task_n_fatals(Strict):
    n_fatals: Optional[int] = Field(
        None,
        title='Max number of fatal processing in a row.',
        # language=YAML
        description='''
            Task get status FATAL after exceeding this limit.
        ''')


class Task_n_runs(Strict):
    n_runs: Optional[int] = Field(
        None,
        title='Max number of simultanious processing',
        # language=YAML
        description='''

    ''')


class Task_deleted(Strict):
    deleted: Optional[bool] = Field(
        False,
        title='Task masked as deleted',
        # language=YAML
        description='''
            Task row not deleted from table. Only marks as deleted
        ''')


class Task_last_proc_id(Strict):
    last_proc_id: Optional[int] = Field(
        None,
        title='Last modified processing ID')


class Task(
    Task_last_proc_id,
    Task_deleted,
    Task_n_runs,
    Task_n_fatals,
    Task_priority,
    Task_period,
    Task_status,
    Task_name,
    Task_project,
    Task_type,
    Task_task_id,
):
    pass