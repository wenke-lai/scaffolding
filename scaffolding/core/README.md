## Director

The director is responsible for creating the scaffold files, language environment, and git repository.

!! Note: When writing operations, respect and implement all existing configuration settings.

### Quick Start

```python
from managers import Uv
from builders import LanguageBuilder
from director import PythonDirector

FOLDER = Path("/tmp/scaffolding")

match package_manager_name:
    case 'uv':
        package_manager = Uv()
    case _:
        raise ValueError(f"Unsupported package manager: {package_manager_name}")

director = PythonDirector(builder=LanguageBuilder(package_manager))
director.create_scaffold_file(FOLDER, license_key="MIT")
match framework:
    case 'django':
        director.create_django_project(FOLDER)
    case 'flask':
        director.create_flask_project(FOLDER)
    case _:
        director.create_python_project(FOLDER)
director.create_git_repository(FOLDER)
```
