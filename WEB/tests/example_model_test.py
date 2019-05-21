import json
from models import example_model

def test_model_has_parameter_called_Example():
  example_model.Example

def test_has_constructor_that_consumes_json():
  example_model.Example(json.dumps({}))

with open('../MANAGE/seeds/users.json') as seed:
      base_data = json.load(seed)
      # test_app.py 
       