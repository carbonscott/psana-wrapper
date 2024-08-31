import numpy as np
from enum import Enum
from typing import Union, Iterable, Optional
from abc import ABC, abstractmethod
from psana import DataSource, Detector, MPIDataSource

class ImageRetrievalMode(str, Enum):
    raw   = "raw"
    calib = "calib"
    image = "image"
    mask  = "mask"

class BasePsanaWrapper(ABC):
    def __init__(self, exp: str, run: int, detector_name: str):
        self.exp = exp
        self.run = run
        self.detector_name = detector_name
        self.detector = Detector(detector_name)
        self.read = {
            "raw"  : self.detector.raw,
            "calib": self.detector.calib,
            "image": self.detector.image,
            "mask" : self.detector.mask,
        }

    def create_bad_pixel_mask(self) -> np.ndarray:
        return self.read["mask"](self.run_current, calib=True, status=True, edges=True,
                                 central=True, unbond=True, unbondnbrs=True, unbondnbrs8=False).astype(np.uint16)

class PsanaWrapperIdx(BasePsanaWrapper):
    def __init__(self, exp: str, run: int, detector_name: str):
        super().__init__(exp, run, detector_name)
        self.datasource_id = f"exp={exp}:run={run}:idx"
        self.datasource    = DataSource(self.datasource_id)
        self.run_current   = next(self.datasource.runs())
        self.events        = self.run_current.times()

    def __len__(self) -> int:
        return len(self.events)

    def get_event(self, event_num: int):
        if event_num is None:
            raise ValueError("event_num must be provided for idx mode")
        timestamp = self.events[event_num]
        return self.run_current.event(timestamp)

    def get(self, event_num: int, id_panel: Optional[int] = None,
            mode: ImageRetrievalMode = ImageRetrievalMode.calib) -> np.ndarray:
        event = self.get_event(event_num)
        data = self.read[mode](event)
        return data[id_panel] if id_panel is not None else data

    def assemble(self, multipanel: bool = None, mode: ImageRetrievalMode = ImageRetrievalMode.image,
                 event_num: int) -> np.ndarray:
        event = self.get_event(event_num)
        return self.read[mode](event, multipanel)

class PsanaWrapperSmd(BasePsanaWrapper):
    def __init__(self, exp: str, run: int, detector_name: str):
        super().__init__(exp, run, detector_name)
        self.datasource_id = f"exp={exp}:run={run}:smd"
        self.datasource    = MPIDataSource(self.datasource_id)
        self.run_current   = next(self.datasource.runs())

    def iter_events(self, mode: ImageRetrievalMode = ImageRetrievalMode.calib,
                    id_panel: Optional[int] = None) -> Iterable[np.ndarray]:
        for event in self.run_current.events():
            data = self.read[mode](event)
            yield data[id_panel] if id_panel is not None else data

    def assemble(self, multipanel: bool = None, mode: ImageRetrievalMode = ImageRetrievalMode.image) -> np.ndarray:
        event = next(self.run_current.events())
        return self.read[mode](event, multipanel)
