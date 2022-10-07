import alt_proc_path
from _import import *
from _types.user import User
import alt_proc.pg_async

app = None
main_dir = os.path.dirname(__file__) + '/'
cfg = alt_proc.cfg.read(f'{main_dir}_cfg/_main__uniq.cfg')

login_last_bad_dt = 0
users = {}
for user in cfg.users:
    users[user.login] = User(**user)

alt_proc_cfg = alt_proc.cfg.read(f'{main_dir}../../_cfg/alt_proc.cfg')
db = alt_proc.pg_async.DB(**alt_proc_cfg.db)

