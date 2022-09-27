# python-kandji

kandji is a Python client for [Kandji](https://www.kandji.io/)'s API.

Complete API endpoint documentation is available at https://api.kandji.io

## Installation
Install the latest release from [PyPI](https://pypi.org/project/kandji/):
```
pip install kandji
```

## Quickstart

1. [Generate an API token within your Kandji instance](https://support.kandji.io/api)

2. Start using kandji:
```python
from kandji import Kandji

kandji = Kandji(
    api_url="your-domain",
    api_token="your-key",
)

# List devices
devices = kandji.list_devices()

# Get device
device = kandji.get_device(id="2cfeb3ac-3b5d-423e-bcff-e2676a3a32da")

# Get device apps
apps = kandji.get_device_apps(id="2cfeb3ac-3b5d-423e-bcff-e2676a3a32da")

# Get device activity
activity = kandji.get_device_activity(id="2cfeb3ac-3b5d-423e-bcff-e2676a3a32da")

# List blueprints
devices = kandji.list_blueprints()

# Get blueprint
blueprint = kandji.get_blueprint(id="97e4e175-1631-43f6-a02b-33fd1c748ab8")
```
