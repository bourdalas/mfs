from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel


class AudioFile(BaseModel):
    path: Path
    size: int

    length: int
    sample_rate: int

    @property
    def duration(self) -> float:
        return self.length / self.sample_rate

    @property
    def extension(self) -> str:
        return self.path.suffix
    
    def __eq__(self, __value: object) -> bool:
        return self.size == __value.size and self.length == __value.length and self.sample_rate == __value.sample_rate

class AbletonAudioClip(BaseModel):
    id: int
    name: str
    relative_file_path: Path
    audio_file: AudioFile 
    
class AbletonAudioTrack(BaseModel):
    id: int
    name: str
    clips: Optional[List[AbletonAudioClip]]


class AbletonLiveSetHeader(BaseModel):
    MajorVersion: int
    MinorVersion: str
    SchemaChangeCount: int
    Creator: str
    Revision: str


class AbletonLiveSet(BaseModel):
    header: AbletonLiveSetHeader
    tracks: List[AbletonAudioTrack]



