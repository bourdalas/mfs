# mfs
Music.Files.Sharing.System, in short MFS is a python app that offers complex audio file sharing functionalities among a set of users and their personal ableton live set projects or audio file collections. 

## Version 0.0: 

MFs currently assumes that the users have already made sure that they share the actual files in their local file system via external tools (eg. blend.io, google drive, soulseek, lp2p, etc).  

### Users should be able to:

* ingest the audio files metadata of local ableton live sets
* ingest audio files metadata of local directories 

* update existing ableton live sets
* update existing audio files

* delete existing ableton lives sets  
* delete existing audio files  

* query relative audio file paths


### Bonus:
* prepare selected audio files for berlin based dj set 
* play selected audio file locally   


## Version 0.1: 

MFs currently assumes that the users have already made sure that they share the actual files in their local file system via external tools (eg. blend.io, google drive, soulseek, lp2p, etc).  

### Users should be able to also:

* add,update,delete ableton live sets tags
* add,update,delete audio file tags

* perform tag based queries



---

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
