import alt_path
from _import import *
from _types.proc import *
from _types.task import *
from _types.script import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class ScriptRes(
    Script_proc_id,
    Script_iscript,
    Script_name,
    Script_status,
    Script_result
):
    pass


class ProcRes(
    Proc_event_id,
    Proc_proc_id,
    Proc_status,
    Proc_result
):
    task: Optional[str] = Field(
        None,
        title='Task name'
    )
    title: Optional[str] = Field(
        None,
        title='Event title'
    )
    scripts: Optional[List[ScriptRes]]


class Res(Strict):
    procs: List[ProcRes]


@router.post(
    '/' + method,
    response_model=Res,
    summary='Processing list'
)
async def main(
        limit: Optional[int] = Query(
            30,
            title='Tasks limit',
            description='Number of returned task rows'
        ),
        task: Optional[str] = Query(
            None,
            title='Task name',
            description='Filter by task name'
        ),
        status: Optional[str] = Query(
            None,
            title='Task status',
            description='Filter by task status'
        ),
        result: Optional[str] = Query(
            None,
            title='Task result',
            description='Filter by task result'
        ),
        event_ids: Optional[List[int]] = Query(
            None,
            title='Procs of event ids',
            description='Filter by event id'
        ),
        login=Depends(auth.get_login)
):
    where, values = ['true'], {'limit': limit}
    if task:
        where.append("t.name=:task")
        values['task'] = task
    if status:
        where.append("p.status=:status")
        values['status'] = status
    if result:
        where.append("p.result=:result")
        values['result'] = result
    if event_ids:
        event_ids_value = ','.join([str(event_id) for event_id in event_ids])
        where.append(f"e.event_id in ({event_ids_value})")

    sql = f"""
            select p.proc_id, p.status, p.result, t.name as task, e.title, p.event_id
            from alt_proc.procs p
            left join events e on p.event_id = e.event_id
            left join tasks t on e.task_id = t.task_id
            where {' and '.join(where)}
            order by proc_id desc
            limit :limit
            """
    procs: List[ProcRes] = await _global.db.find(ProcRes, sql, values)

    if procs:
        proc_ids = ','.join([f'{proc.proc_id}' for proc in procs])
        sql = f"""
            select proc_id, iscript, name, status, result
            from alt_proc.scripts  
            where proc_id in ({proc_ids})
            order by proc_id, iscript
            """
        scripts: List[ScriptRes] = await _global.db.find(ScriptRes, sql)
        scripts_by_proc_id = defaultdict(list)
        for script in scripts:
            scripts_by_proc_id[script.proc_id].append(script)

        for proc in procs:
            proc.scripts = sorted(scripts_by_proc_id[proc.proc_id], key=lambda script: script.iscript)

    return Res(procs=procs)
