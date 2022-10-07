from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import Field
from alt_proc.types import Strict

class User(Strict):
    login: str
    md5: str
    roles: List[str]


