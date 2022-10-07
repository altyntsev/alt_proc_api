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


class Res(Strict):
    task: Task
    event: Event
    proc: Proc
    scripts: List[Script]

@router.get(
    '/' + method,
    response_model=Res,
    summary='Processing info'
)
async def main(
        proc_id: int = Query(
            ...,
            title='Proc ID'
        ),
        login=Depends(auth.get_login)
):
    sql = """
            select * from procs where proc_id=:proc_id
            """
    proc = await _global.db.find_one(Proc, sql, {'proc_id': proc_id})

    sql = """
            select * from events where event_id=:event_id
            """
    event = await _global.db.find_one(Event, sql, {'event_id': proc.event_id})

    sql = """
            select * from tasks where task_id=:task_id
            """
    task = await _global.db.find_one(Task, sql, {'task_id': event.task_id})


    sql = """
            select * from scripts where proc_id=:proc_id order by iscript
            """
    scripts = await _global.db.find(Script, sql, {'proc_id': proc.proc_id})

    return Res(task=task, event=event, proc=proc, scripts=scripts)
