import alt_path
from _import import *
from _types.event import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Res(Event):
    pass

@router.get(
    '/' + method,
    response_model=Res,
    summary='Event info'
)
async def main(
        event_id: int = Query(
            ...,
            title='Event ID'
        ),
        login=Depends(auth.get_login)
):
    sql = """
            select * from events where event_id=:event_id
            """
    event: Event = await _global.db.find_one(Event, sql, {'event_id': event_id})

    return event
