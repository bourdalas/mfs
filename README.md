# mfs
Music.Files.Sharing.System, in short MFS is a python app that offers complex audio file sharing functionalities among a set of users and their personal ableton live set projects or audio file collections. 

MFS currently assumes that the users have already made sure that they share the actual files in their local file system via external tools (eg. blend.io, external hard drive, google drive, soulseek, lp2p, etc).  

# Installation

``` bash 

poetry install 

```

# Run locally 

Start the fastapi backend in a terminal

``` bash 
 uvicorn mfs.backend.main:app --reload         
```
Start the streamlit app in a different terminal
``` bash 
streamlit run mfs/front_main.py 
```


## Version 0.1.0: 

### Users should be able to:

* Sign up / Log in / Log out 
* View public users list




## Version 0.2.0: 

### Users should be able to:

* ingest the audio files metadata of local ableton live sets
* ingest audio files metadata of local directories 

* update existing ableton live sets
* update existing audio files

* delete existing ableton lives sets  
* delete existing audio files  

* query relative audio file paths

## Version 0.3.0: 

### Users should be able to:
* play/preview selected audio files locally (eg. using ffmpeg)   
* copy selected audio files to local directory (eg. flash drive)
* transform selected audio files to RekordBox playlist XML (eg. berlin based dj set collections) 


## Version 0.2: 

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
