import alt_path
from _import import *
import _global
from _types.task import *

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(Strict):
    status: Optional[Literal['RUN', 'PAUSE', 'EXIT', 'FATAL']]

class Res(Strict):
    pass


@router.post(
    '/' + method,
    response_model=Res,
    summary='Set launcher status'
)
async def main(params: Params = Body(...), login=Depends(auth.get_login)):
    sql = '''
        update values set value=:status where key='launcher_status'
        '''
    await _global.db.query(sql, params)

    return Res()
