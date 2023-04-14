from pathlib import Path
import pytest 
from hypothesis import given, strategies as st

from mfs.core.ableton.abletonlivesetparser import AbletonLiveSetParser
from mfs.core.ableton.abletonlivesetreader import AbletonLiveSetFileReader
import zipfile

@pytest.fixture()
def xml_data():
    return 

@pytest.fixture()
def als_file():
    # xml_data = '''
    #     <?xml version="1.0" encoding="UTF-8"?>
    #     <Ableton Live Set Version="1">
    #         <Tracks>
    #             <AudioTrack Name="Track 1">
    #                 <DeviceChain>
    #                     <MainMixer>
    #                         <AudioClip Name="Clip 1" Length="12345">
    #                             <SampleRef SamplePath="path/to/file.wav"/>
    #                         </AudioClip>
    #                     </MainMixer>
    #                 </DeviceChain>
    #             </AudioTrack>
    #         </Tracks>
    #     </Ableton Live Set>
    # '''
    # xml_path = tmp_path / 'AbletonLiveSet.xml'
    # xml_path.write_text(xml_data)
    # with zipfile.ZipFile(tmp_path / 'test.als', 'w') as zip_file:
    #     zip_file.write(xml_path, 'ProjectInfo/AbletonLiveSet.xml')
    return Path('tests/fixtures/test Project/test.als').resolve()


@pytest.fixture()
def reader():
    return AbletonLiveSetFileReader()


@pytest.fixture()
def parser():
    return AbletonLiveSetParser()


# @given(st.integers(min_value=1, max_value=10000))
# def test_audio_clip_length(audio_clip, length):
#     audio_clip.length = length
#     assert audio_clip.length == length


# def test_audio_clip_file_path(parser, als_file):
#     xml_struct = parser.read_als_file(als_file)
#     ableton_live_set = parser.parse_als_xml_struct(xml_struct)
#     assert ableton_live_set.tracks[0].clips[0].file_path == 'path/to/file.wav'


# def test_audio_track_name(parser, als_file):
#     xml_struct = parser.read_als_file(als_file)
#     ableton_live_set = parser.parse_als_xml_struct(xml_struct)
#     assert ableton_live_set.tracks[0].name == 'Track 1'


def test_audio_clip_name(reader, parser, als_file):
    xml_struct = reader.read_als_file(als_file)
    ableton_live_set = parser.parse_als_xml_struct(xml_struct)
    assert ableton_live_set.tracks[0].clips[0].name == 'Clip 1'
