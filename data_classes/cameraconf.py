__author__ = "Eolus"

# Standard libraries
from dataclasses import dataclass, field, asdict
import os
import yaml
import typing
# Third party libraries
# Custom libraries


@dataclass
class CameraConf:
    name: str = field(init=False, repr=True, default="")
    address: str = field(init=False, repr=True, default="")
    frames_per_minute: int = field(init=False, repr=True, default=1)
    store_path: str = field(init=False, repr=True, default="")

    def __init__(self, conf_path: str):
        with open(os.path.normpath(conf_path)) as f:
            camera_conf = yaml.load(f, Loader=yaml.FullLoader)

        self.name = camera_conf['name']
        self.address = camera_conf['address']
        self.frames_per_minute = camera_conf['frames_per_minute']
        self.store_path = camera_conf['store_path']

        self.__type_check()

    def __type_check(self):
        attributes_and_types = typing.get_type_hints(CameraConf)
        current_class_asdict = asdict(self)
        for i in range(len(attributes_and_types)):
            key = list(attributes_and_types.keys())[i]
            if isinstance(attributes_and_types[key], type(current_class_asdict[key])):
                raise TypeError(f"Camera conf {key} incorrect type.")
