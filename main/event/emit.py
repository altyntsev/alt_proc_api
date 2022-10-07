import alt_path

import lib
from _import import *
import _global
from _types.task import *
from _types.event import *

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(Event_title, Event_params):
    task: str = Field(
        ...,
        title='Task name'
    )


class Res(Strict):
    event_id: int = Field(
        ...,
        title='Event ID of emitted event'
    )


@router.post(
    '/' + method,
    response_model=Res,
    summary='Emit event'
)
async def main(params: Params = Body(...), login=Depends(auth.get_login)):
    sql = '''
        select * from tasks where name=:task and status!='DELETED'
        '''
    task: Task = await _global.db.find_one(Task, sql, params)
    if not task:
        lib.fatal('Unknown task')

    sql = '''
        insert into events (task_id, title, params) values (:task_id, :title, :params)
        '''
    values = params.dict()
    values['task_id'] = task.task_id
    values['params'] = json.dumps(params.params if params.params else {})

    event_id = await _global.db.insert(sql, values, 'event_id')

    return Res(event_id=event_id)
