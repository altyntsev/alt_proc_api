import alt_path
from _import import *
from _types.task import *
from _types.event import *
from _types.proc import *
from _types.script import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

class TaskRes(Task):
    n_events: Optional[int] = Field(
        None,
        title='Number of waiting events'
    )
    n_wait_procs: Optional[int] = Field(
        None,
        title='Number of waiting procs'
    )
    n_run_procs: Optional[int] = Field(
        None,
        title='Number of running procs'
    )
    n_success_procs: Optional[int] = Field(
        None,
        title='Number of successful procs for last day'
    )
    n_fatal_procs: Optional[int] = Field(
        None,
        title='Number of fatal and error procs for last day'
    )
    last_proc_status: Optional[Literal['WAIT', 'RUN', 'DONE', 'DELETED']] = Field(
        None,
        title='Status of last modified proc'
    )
    last_proc_result: Optional[Literal['SUCCESS', 'FATAL', 'ERRORS']] = Field(
        None,
        title='Last result of last modified proc'
    )
    scripts: Optional[List[Script]]

class Res(Strict):
    tasks: List[TaskRes]
    launcher_mtime: Optional[str] = Field(
        None,
        title='Launcher loop mtime',
        description='Updated once a minute. Serves as launcher alive flag.'
    )
    launcher_status: Optional[Literal['RUN', 'PAUSE', 'EXIT', 'FATAL']] = Field(
        None,
        title='Launcher status',
        description='''
            RUN: Normal run mode
            PAUSE: Launcher does not start new procs
            FATAL: Launcher was stopped because some fatal reason
            EXIT: Launcher was stopped manually by admin request
            '''
    )

@router.get(
    '/' + method,
    response_model=Res,
    summary='Status summary'
)
async def main(login=Depends(auth.get_login)):
    sql = """
            select t.*, p.status as last_proc_status, p.result as last_proc_result, 
                n_events, n_wait_procs, n_run_procs, n_success_procs, n_fatal_procs 
            from tasks t
            left join procs p on p.proc_id = t.last_proc_id
            left join (
                select task_id, count(event_id) as n_events from events  
                where status='WAIT' group by task_id
            ) e on e.task_id=t.task_id
            left join (
                select task_id, count(proc_id) as n_wait_procs 
                from procs p
                left join events e on e.event_id = p.event_id  
                where p.status='WAIT' group by task_id
            ) wp on wp.task_id=t.task_id
            left join (
                select task_id, count(proc_id) as n_run_procs 
                from procs p
                left join events e on e.event_id = p.event_id  
                where p.status='RUN' group by task_id
            ) rp on rp.task_id=t.task_id
            left join (
                select task_id, count(proc_id) as n_success_procs 
                from procs p
                left join events e on e.event_id = p.event_id  
                where p.status='DONE' and p.result='SUCCESS' and p.mtime>now() - interval '1 DAY'
                group by task_id
            ) sp on sp.task_id=t.task_id
            left join (
                select task_id, count(proc_id) as n_fatal_procs 
                from procs p
                left join events e on e.event_id = p.event_id  
                where p.status='DONE' and p.result in ('FATAL', 'ERRORS') and p.mtime>now() - interval '1 DAY'
                group by task_id
            ) fp on fp.task_id=t.task_id
            where t.status!='DELETED' 
            order by t.project, t.type desc, t.name
            """
    tasks = await _global.db.find(TaskRes, sql)

    proc_ids = ','.join([f'{task.last_proc_id}' for task in tasks if task.last_proc_id is not None])
    if proc_ids:
        sql = f"""
            select * from scripts where proc_id in ({proc_ids}) order by proc_id, iscript
            """
        print(sql)
        scripts = await _global.db.find(Script, sql)
        scripts_by_proc_id = defaultdict(list)
        for script in scripts:
            scripts_by_proc_id[script.proc_id].append(script)
        for task in tasks:
            task.scripts = scripts_by_proc_id.get(task.last_proc_id)

    sql = """
        select value from values where key='launcher_mtime'
        """
    rows = await _global.db.query(sql)
    launcher_mtime = rows[0]['value'][:19] if rows else None
    launcher_mtime = launcher_mtime + ' ' + alt_proc.time.diff(launcher_mtime)

    sql = """
        select value from values where key='launcher_status'
        """
    rows = await _global.db.query(sql)
    launcher_status = rows[0]['value'][:19] if rows else None

    return Res(tasks=tasks, launcher_mtime=launcher_mtime, launcher_status=launcher_status)
