import alt_path
from _import import *
from _types.event import *
from _types.event import *
from _types.script import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

class EventRes(Event):
    task: str = Field(
        ...,
        title='Task name'
    )

class Res(Strict):
    events: List[EventRes]


@router.post(
    '/' + method,
    response_model=Res,
    summary='Waiting event list'
)
async def main(
        limit: Optional[int] = Query(
            30,
            title='Events limit',
            description='Number of returned events'
        ),
        task: Optional[str] = Query(
            None,
            title='Task name',
            description='Filter by task name'
        ),
        event_ids: Optional[List[int]] = Query(
            None,
            title='Event IDs',
            description='Filter by event id'
        ),
        login=Depends(auth.get_login)
):
    where, values = ['true'], {'limit': limit}
    if task:
        where.append("t.name=:task")
        values['task'] = task
    if event_ids:
        # todo security issue
        event_ids_value = ','.join([str(event_id) for event_id in event_ids])
        where.append(f"e.event_id in ({event_ids_value})")

    sql = f"""
            select e.*, t.name as task
            from alt_proc.events e
            left join tasks t on e.task_id = t.task_id
            where {' and '.join(where)}
            order by event_id desc
            limit :limit
            """
    events: List[EventRes] = await _global.db.find(EventRes, sql, values)

    return Res(events=events)
