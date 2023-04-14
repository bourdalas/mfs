# import pytest
# from mfs.core.ableton.abletonlivesetparser import AbletonLiveSetParser
# from mfs.core.ableton.abletonlivesetreader import AbletonLiveSetFileReader
# import zipfile

# @pytest.fixture()
# def als_file(tmp_path):
#     xml_data = '''
#         <?xml version="1.0" encoding="UTF-8"?>
#         <Ableton Live Set Version="1">
#             <Tracks>
#                 <AudioTrack Name="Track 1">
#                     <DeviceChain>
#                         <MainMixer>
#                             <AudioClip Name="Clip 1" Length="12345">
#                                 <SampleRef SamplePath="path/to/file.wav"/>
#                             </AudioClip>
#                         </MainMixer>
#                     </DeviceChain>
#                 </AudioTrack>
#             </Tracks>
#         </Ableton Live Set>
#     '''
#     xml_path = tmp_path / 'AbletonLiveSet.xml'
#     xml_path.write_text(xml_data)
#     with zipfile.ZipFile(tmp_path / 'test.als', 'w') as zip_file:
#         zip_file.write(xml_path, 'ProjectInfo/AbletonLiveSet.xml')
#     return tmp_path / 'test.als'


# @pytest.fixture()
# def reader():
#     return AbletonLiveSetFileReader()


# @pytest.fixture()
# def parser():
#     return AbletonLiveSetParser()
