from configparser import ConfigParser
from pathlib import Path

fp = Path(__file__).absolute().parent.parent.joinpath("setup.cfg").as_posix()
cfp = ConfigParser()
cfp.read(fp)

NAME = cfp.get('metadata', 'description')
VERSION = cfp.get('metadata', 'version')
