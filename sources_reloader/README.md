# Sources reloader

This class was written to se if python application could reload
source code pieces while running.
Purposes of usage:
* strange implementation of factory pattern;
* fix/change code while process is still running (I'd rather avoid using this on prod servers);
* self rebuilding program

## Usage

```python
import importlib

from sources_reloader import SourcesReloader


class Body(SourcesReloader):
    pass


body = Body()
body.brain = importlib.import_module('brain')
body.brain.do_math('2 + x = 5')  # solves linear equations
with open('brain.py', 'w') as brain:
    new_math_possibilities = body.brain.improve('math')
    brain.write(new_math_possibilities)

body.brain.do_math('x ^ 2 + 3 * x - 5 = 0')  # now solves quadratic equations
```
