## Director

The director is responsible for creating the project, language, license, and git repository.

!! Note: When writing operations, respect and implement all existing configuration settings.

### Quick Start

```python
from core.director import Director
from core.factories.base import ProjectFactory
from core.blueprint import Blueprint

# create the blueprint
blueprint = Blueprint()

# create the factory
factory = ProjectFactory(blueprint)

# create the director and process the blueprint
director = Director(factory)
director.process()
```
