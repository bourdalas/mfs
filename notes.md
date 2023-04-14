

## Requirements Scope 


SQL DB Tables:

    Users

    AbletonAudioClips

    AbletonAudioTracks

    AbletonProjects

    AbletonAudioFiles

    AudioFiles

Data Models:

    AudioFile 

    AbletonAudioFile(AudioFile)

    AbletonClip

    AbletonMidiClip(AbletonClip)

    AbletonAudioClip(AbletonClip)

    AbletonTrack

    AbletonMidiTrack(AbletonTrack)

    AbletonAudioTrack(AbletonTrack)

    AbletonLiveSet


AbletonLiveSetFileReader:
  
    read_als_file(Path) -> XMLStruct

    _decompress_als_file(Path)

    _read_xml_file() -> XMLStruct


AbletonLiveSetParser:

    parse_als_xml_struct(XMLStruct) -> AbletonLiveSet

    _parse_audio_tracks() -> List[AbletonAudioTracks]

    _parse_audio_track() -> AbletonAudioTrack
    
    _parse_audio_clip() -> AbletonAudioClip
