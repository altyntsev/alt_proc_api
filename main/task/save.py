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
    Task_n_runs,
    Task_n_fatals,
    Task_priority,
    Task_period,
    Task_project,
    Task_name,
    Task_type,
    Task_task_id
):
    pass


class Res(Strict):
    pass


@router.post(
    '/' + method,
    response_model=Res,
    summary='Save task',
    # language=YAML
    description='''
        Mandatory attrs for different tasks:
            New task: type, name, project
            Existing task: task_id
            EVENT: priority, n_fatals, n_runs
            PERIODIC: period
    '''
)
async def main(params: Params = Body(...), login=Depends(auth.get_login)):

    if (params.task_id == 'new'):
        if not params.name:
            lib.fatal('Task name is empty')
        if not params.project:
            lib.fatal('Project is empty')
        project_dir = alt_proc.cfg.user_projects_dir() + params.project + '/'
        if not os.path.exists(project_dir):
            lib.fatal(f'Project not exists: {project_dir}')
        task_file = f'{project_dir}main/_cfg/{params.name}.task'
        if not os.path.exists(task_file):
            lib.fatal(f'Task file not exists: {task_file}')
        sql = "select task_id from tasks where name=:name and status!='DELETED'"
        existing_tasks = await _global.db.query(sql, {'name': params.name})
        if existing_tasks:
            lib.fatal('Existing task with the same name')
        if not params.type:
            lib.fatal('Task type empty')
    else:
        sql = 'select * from alt_proc.tasks where task_id=:task_id'
        task = await _global.db.query(sql, {'task_id': params.task_id})
        if not task:
            lib.fatal('Task not exists')

    if params.task_id == 'new':
        sql = '''
            insert into alt_proc.tasks 
            (type, name, project, priority, period, n_fatals, n_runs)
            values (:type, :name, :project, :priority, :period, :n_fatals, :n_runs)
            '''
        await _global.db.insert(sql, params)
    else:
        sql = '''
            update alt_proc.tasks 
            set priority = :priority, period = :period, n_fatals = :n_fatals, n_runs = :n_runs
            where task_id=:task_id
            '''
        await _global.db.query(sql, params)

    return Res()
