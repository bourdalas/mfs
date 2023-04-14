import gzip
from typing import List

from xml.etree.ElementTree import parse, ElementTree
from pathlib import Path


class AbletonLiveSetFileReader:

    def read_als_file(self, path: Path) -> ElementTree:      
        with gzip.open(path, 'rb') as f:
            return parse(f)
            


    def get_audio_tracks(self, et: ElementTree) -> List[ElementTree]:
        return et.findall('.//AudioTrack')


