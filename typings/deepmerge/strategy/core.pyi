from typing import Any
from typing import List
from typing import Union
from typing import Callable
from typing import Optional

_StringOrFunction = Union[str, Callable[..., Any]]
STRATEGY_END: object = ...

class StrategyList:
    NAME: Optional[str] = ...
    def __init__(
        self, strategy_list: Union[_StringOrFunction, List[_StringOrFunction]]
    ) -> None: ...
    @classmethod
    def _expand_strategy(cls, strategy: _StringOrFunction) -> _StringOrFunction: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
