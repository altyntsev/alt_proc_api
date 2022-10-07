import alt_path
from _import import *
from _types.task import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(Strict):
    pass


class Res(Strict):
    tasks: List[Task]


@router.get(
    '/' + method,
    response_model=Res,
    summary='Task list'
)
async def main(login=Depends(auth.get_login)):
    sql = f"""
            select *
            from alt_proc.tasks
            order by project 
            """

    tasks = await _global.db.find(Task, sql)

    return Res(tasks=tasks)
