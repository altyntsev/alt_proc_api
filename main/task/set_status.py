import alt_path
import lib
from _import import *
import _global
from _types.task import *

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(
    Task_status,
    Task_project,
    Task_task_id
):
    pass


class Res(Strict):
    pass


@router.post(
    '/' + method,
    response_model=Res,
    summary='Set task status',
    # language=YAML
    description='''
        Either task_id or project must be set
    '''
)
async def main(params: Params = Body(...), login=Depends(auth.get_login)):
    if params.project and params.task_id:
        lib.fatal('Either task_id or project must be set')
    if params.task_id:
        sql = '''
            update alt_proc.tasks set status=:status where task_id=:task_id
            '''
    else:
        sql = '''
            update alt_proc.tasks set status=:status where project=:project
            '''
    await _global.db.query(sql, params)

    return Res()
