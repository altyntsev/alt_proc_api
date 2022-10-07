import alt_path
from _import import *
import _global
from _types.task import *

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Res(Task):
    pass


@router.get(
    '/' + method,
    response_model=Res,
    summary='Task info'
)
async def main(
        task_id: int = Query(
            ...,
            title='task_id'
        ),
        login=Depends(auth.get_login)
):
    sql = f"""
            select *
            from alt_proc.tasks
            where task_id=:task_id 
            """

    task: Res = await _global.db.find_one(Task, sql, {'task_id': task_id})

    return task
