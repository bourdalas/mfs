# mfs
Music.Files.Sharing.System, in short MFS is a python app that offers complex audio file sharing functionalities among a set of users and their personal ableton live set projects or audio file collections. 

MFS currently assumes that the users have already made sure that they share the actual files in their local file system via external tools (eg. blend.io, external hard drive, google drive, soulseek, lp2p, etc).  

# Installation

Create and activate a new python 3.9.6 environment.

``` bash 
pip/conda install poetry 
```

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



