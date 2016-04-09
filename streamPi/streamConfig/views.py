#encoding: utf-8
#
#Copyright (C) 2016 Ruben Montero Vazquez <ruben39x2@live.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import render
from django.http import HttpResponse
from streamConfig.models import DarkiceConfig
import os

def index(request):
  # En caso de que haya llegado un POST, significa que quieren cambiar la configuracion
  if request.POST.has_key('server'):

    # Con esto obtenemos el HTML que vamos a imprimir
    page = getPagePost(request)

    # Aqui almacenamos la nueva config en la DB    
    # 1- Borramos la vieja
    if (len(DarkiceConfig.objects.all())>0):
      DarkiceConfig.objects.all()[0].delete()
    # 2- Creamos la nueva y la almacenamos
    newConfig = DarkiceConfig(bitrateMode=request.POST['bitrateMode'], bitrate=request.POST['bitrate'], format=request.POST['format'], server=request.POST['server'], port=request.POST['port'], password=request.POST['password'], mountPoint=request.POST['mountPoint'], name=request.POST['name'], description=request.POST['description'], url=request.POST['url'], genre=request.POST['genre'], public=request.POST['public'], localDumpFile='/home/pi/backup-streaming/dumpfile.ogg', device=request.POST['device'])
    newConfig.save()

    # Y ahora generamos el fichero darkice.cfg y lo guardamos
    saveDarkiceConfig("/home/pi/darkice.cfg", getDarkiceConfig(request))

    # Devolvemos el HTML
    return HttpResponse(page)

  # En caso de que sea un GET, mostramos el formulario para cambiar configuracion
  else:
    if (len(DarkiceConfig.objects.all())>0):
      currentConfig = DarkiceConfig.objects.all()[0]
      context = {'currentConfig':currentConfig}
      return render(request, 'streamConfig/index.html', context)
    else:
      return render(request, 'streamConfig/index.html')
  

def getPagePost(request):
    page = "<b>Bitrate Mode: </b>"
    page += request.POST['bitrateMode']
    page += "<BR>"
    page += "<b>Bitrate: </b>"
    page += request.POST['bitrate']
    page += "<BR>"
    page += "<b>Format: </b>"
    page += request.POST['format']
    page += "<BR>"
    page += "<b>Server: </b>"
    page += request.POST['server']
    page += "<BR>"
    page += "<b>Port: </b>"
    page += request.POST['port']
    page += "<BR>"
    page += "<b>Password: </b>"
    page += request.POST['password']
    page += "<BR>"
    page += "<b>Mount Point: </b>"
    page += request.POST['mountPoint']
    page += "<BR>"
    page += "<b>Name: </b>"
    page += request.POST['name']
    page += "<BR>"
    page += "<b>Description: </b>"
    page += request.POST['description']
    page += "<BR>"
    page += "<b>URL: </b>"
    page += request.POST['url']
    page += "<BR>"
    page += "<b>Genre: </b>"
    page += request.POST['genre']
    page += "<BR>"
    page += "<b>Public: </b>"
    page += request.POST['public']
    page += "<BR>"
    page += "<b>Device: </b>"
    page += request.POST['device']
    page += "<BR><BR><i>Los cambios han sido guardados</i>"

    return page

def getDarkiceConfig(request):
  config = """# ESTE FICHERO HA SIDO AUTOGENERADO POR DJANGO - STREAMING PI FOR THE WIN
# sample DarkIce configuration file, edit for your needs before using
# see the darkice.cfg man page for details

# this section describes general aspects of the live streaming session
[general]
duration        = 0        # duration of encoding, in seconds. 0 means fo$
bufferSecs      = 5         # size of internal slip buffer, in seconds
reconnect       = yes       # reconnect to the server(s) if disconnected
realtime        = yes       # run the encoder with POSIX realtime priority
rtprio          = 3         # scheduling priority for the realtime threads

# this section describes the audio input that will be streamed
[input]
device          = """+request.POST['device']+""" # OSS DSP soundcard device for the audio inp$
sampleRate      = 44100     # sample rate in Hz. try 11025, 22050 or 44100
bitsPerSample   = 16        # bits per sample. try 16
channel         = 2         # channels. 1 = mono, 2 = stereo

# this section describes a streaming connection to an IceCast2 server
# there may be up to 8 of these sections, named [icecast2-0] ... [icecast$
# these can be mixed with [icecast-x] and [shoutcast-x] sections
[icecast2-0]
bitrateMode     = """+request.POST['bitrateMode']+"""       # average bit rate
format          = """+request.POST['format']+"""    # format of the stream: ogg vorbis
bitrate         = """+request.POST['bitrate']+"""        # bitrate of the stream sent to the server
server          = """+request.POST['server']+"""   # host name of the server
port            = """+request.POST['port']+"""      # port of the IceCast2 server, usually 8000
password        = """+request.POST['password']+"""    # source password to the IceCast2 server
mountPoint      = """+request.POST['mountPoint']+"""  # mount point of this stream on the Ice$
name            = """+request.POST['name']+"""   # name of the stream
description     = """+request.POST['description']+"""   # description of the stream
url             = """+request.POST['url']+"""   # URL related to the stream
genre           = """+request.POST['genre']+"""     # genre of the stream
public          = """+request.POST['public']+"""       # advertise this stream?
localDumpFile   = /home/pi/backup-streaming/dumpfile.ogg  # local dump file"""

  return config

def saveDarkiceConfig(path, configFile):
  if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
  with open(path, "w") as f:
    f.write(configFile)
