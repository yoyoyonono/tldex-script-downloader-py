from dataclasses import dataclass
import datetime

@dataclass
class Message:
    """
    Contains message metadata.
    """
    name: str
    timestamp: datetime.datetime
    message: str

@dataclass
class VideoMeta:
    """
    Contains video metadata.
    """
    status: str
    start_actual: datetime.datetime
    available_at: datetime.datetime
    tl_and_count: dict[str, int]
