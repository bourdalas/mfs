

from mfs.core.ableton.models import AudioFile, AbletonAudioClip, AbletonAudioTrack, AbletonLiveSet, AbletonLiveSetHeader


from typing import List
from xml.etree.ElementTree import ElementTree, dump


class AbletonLiveSetParser:
    def parse_als_xml_struct(self, xml_struct: ElementTree) -> AbletonLiveSet:
        element = xml_struct.getroot()

        if xml_struct.find('.//Tracks'):
            tracks_tree = xml_struct.find('.//Tracks')
        elif xml_struct.find('.//.//Tracks'):
            tracks_tree = xml_struct.find('.//.//Tracks')

        return AbletonLiveSet(
            header = AbletonLiveSetHeader(
            MajorVersion=int(element.attrib["MajorVersion"]),
            MinorVersion=element.attrib["MinorVersion"],
            SchemaChangeCount=int(element.attrib["SchemaChangeCount"]),
            Creator=element.attrib["Creator"],
            Revision=element.attrib["Revision"],
        ),
            tracks=self._parse_audio_tracks(tracks_tree))
    
    def _parse_audio_tracks(self, tracks: ElementTree) -> List[AbletonAudioTrack]:
        audio_tracks = []
        for track in tracks.findall('.//AudioTrack'):
            
            audio_track = self._parse_audio_track(track)
            audio_tracks.append(audio_track)
        return audio_tracks
    
    def _parse_audio_track(self, track: ElementTree) -> AbletonAudioTrack:
        audio_track = AbletonAudioTrack(
            id=track.get("Id"),
            name=track.find("Name").find("EffectiveName").get("Value"),
            clips=self._parse_audio_clips(track.findall('.//AudioClip')))
        return audio_track
    
    def _parse_audio_clips(self, clips: List[ElementTree]) -> List[AbletonAudioClip]:
        audio_clips = []
        for clip in clips:
            audio_clip = AbletonAudioClip(
                id=clip.get("Id"),
                name=clip.find("Name").get("Value"), 
                relative_file_path=clip.find('.//SampleRef').find("FileRef").find("RelativePath").get("Value"),
                audio_file=AudioFile(
                    path=clip.find('.//SampleRef').find("FileRef").find("Path").get("Value"),
                    size=clip.find('.//SampleRef').find("FileRef").find("OriginalFileSize").get("Value"),
                    length=clip.find('.//SampleRef').find("DefaultDuration").get("Value"),
                    sample_rate=clip.find('.//SampleRef').find("DefaultSampleRate").get("Value")
                )
            )
            audio_clips.append(audio_clip)
        return audio_clips
