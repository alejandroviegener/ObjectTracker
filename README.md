# Object Tracker

Application for multi object tracking, given initial bounding boxes.


## Requirements

This application requieres the following for its installation and usage:

* [git][git] 
* [Docker][docker]


[git]: https://git-scm.com/
[docker]: https://www.docker.com/   

## Installation

Download the soource repository to the desired location. From now on this directory will be refered to as $REPO_BASE_DIR: 

```bash
cd $REPO_BASE_DIR
git clone git@github.com:alejandroviegener/ObjectTracker.git
```

The application is dockerized, to build the Docker image follow these steps:

Change to the source directory in the repository and give permission to the installation script:

```bash
cd source
chmod +x install.sh
```

Execute the install script:

```bash
./install.sh
```

The script will create a docker image and an **inout** directory. This directory will be used as in and out entrypoint for the aplication. 

To confirm the creation of the image, execute:

```bash
docker image ls
```

A docker image tagged "deepvision-tracker" must be listed

## Usage

Change to the source directory in the repository:

```bash
cd $REPO_BASE_DIR/source
```

Give permissions to the application script:

```bash
chmod +x tracker.sh
```

Run the application:

```bash
./tracker.sh --help
```

Typical usage:

```bash
./tracker.sh input.mkv initial_conditions.json -v 1 -o output -l out.log
```

**Note**: The input video, the initial conditions file and the output of the application are managed trough the **inout** directory.


```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)