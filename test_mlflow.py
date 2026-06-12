import json

from config.constants import FINAL_FEATURES_JSON

with open(FINAL_FEATURES_JSON, "r") as f:

    data = json.load(f)

print(type(data))
print(data)




