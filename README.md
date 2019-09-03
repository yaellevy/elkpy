# Sushi - gRPC controller warpper #

A simple wrapper for controlling sushi over gRPC via a python script. 

### Prerequisites ###

To use this wrapper, [python3.5](https://www.python.org/downloads/) or greater need to be installed.

### Installation ###

Clone the repository using:
```console
$ git clone repositoryaddress
```
Copy the folder ELKpy to the directory where you want to run it from. 

_In the future a more automated install will be created._

### Usage ###

First import the sushicontroller package. An alias can be used to shorten the length of the code.
```python
from ELKpy import sushicontroller as sc
```
An instance of the sushicontroller object can be created using the following:
```python
controller = sc.SushiController()
```
The default gRPC address is `localhost:51051` if you want to connect to another address. You can pass it as an argument to the constructor of the controller on the form `ip-address:port`.

To use the controller simply use the methods of the controller object. For example:
```python
# Get a list of the tracks available in sushi
list_of_tracks = controller.get_tracks()

# Get the processors of the track with the id passed to the method
track_id = 0
list_of_processors = controller.get_track_processors(track_id)

# Send a note on message to a track in sushi
track_id = 0
channel = 0
note = 65
velocity = 0.8
controller.send_note_on(track_id, channel, note, velocity)
```

For a full documentation of the available methods. Use:
```console
$ pydoc3 ELKpy.sushicontroller.SushiController
```
from where the ELKpy folder is located.