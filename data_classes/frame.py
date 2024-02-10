__author__ = "Eolus"

# Standard libraries
import datetime
from dataclasses import dataclass, field
import numpy as np
# Third party libraries
# Custom libraries


@dataclass
class Frame:
    values: np.array = field(init=True, repr=True)
    cam_name: str = field(init=True, repr=True)
    frame_number: int = field(default=None)

    time_stamp: datetime.datetime = field(init=False, repr=True)
    time_stamp_str: str = field(init=False, repr=True)

    horizontal_resolution: int = field(init=False, repr=True)
    vertical_resolution: int = field(init=False, repr=True)
    color_bands: int = field(init=False, repr=True)

    def __post_init__(self):
        """Initializes the class."""
        # Time stamp
        self.time_stamp = datetime.datetime.now()
        self.time_stamp_str = self.time_stamp.strftime("%y%m%d_%H%M%S")

        # Picture properties
        self.vertical_resolution, self.horizontal_resolution, self.color_bands = \
            self.values.shape
