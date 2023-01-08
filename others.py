
from PIL import Image
import configparser

import os
import json

# image = Image.open("4.png")

# print(image.size)

# out = image.resize((360, 203))

# out.save("4_new.png")

# image_new = Image.open("4_new.png")
# print(image_new.size)

# a = { list: [{'a':1}] }
# b = a['list']
# a.append({ 'a': 1 })
# print(b)
clock_list = {}

dir_path = r'setting'
json_path = r'setting/clock.json'
if os.path.exists(dir_path) == False:
    os.makedirs(dir_path)
if os.path.exists(json_path):
    with open(json_path) as f:
        clock_list = json.load(f)
    print('load')
else:
    print('dump')
    clock_list = {
        'list': []
    }
    with open(json_path, "w") as outfile:
        json.dump(clock_list, outfile)
print(clock_list)
print(clock_list['list'])
clock_list['list'].append({
    "a":1
})
print(clock_list)
# config = configparser.ConfigParser()
# config.read("config.ini")
# try:
#     config.add_section("Delete")
#     config.set("Delete", "Tip", "False")
#     config.set("Delete", "ToAsh", "False")
#     config.set("Delete", "Drop","True")
# except configparser.DuplicateOptionError:
#     print("exists")
# config.write(open("config.ini", "w"))