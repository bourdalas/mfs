# mfs
Music.Files.Sharing.System, in short MFS is a python app that offers complex audio file sharing functionalities among a set of users and their personal ableton live set projects or audio file collections.




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
