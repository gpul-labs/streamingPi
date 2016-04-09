#encoding: utf-8
#
#Copyright (C) 2016 José Millán Soto <jmillan@kde-espana.org>
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

from django.conf import settings
from django.db import models

import os
import string
import uuid

class Network(models.Model):
    name = models.CharField(max_length=30)
    uuid = models.CharField(max_length=36, blank=True)
    use_dhcp = models.BooleanField()
    ip4_address = models.CharField(max_length=16, blank=True)
    ip4_netmask = models.CharField(max_length=16, blank=True)
    ip4_gateway = models.CharField(max_length=16, blank=True)
    ip4_dns1 = models.CharField(max_length=16, blank=True)
    ip4_dns2 = models.CharField(max_length=16, blank=True)

    fileName = models.CharField(max_length=256, blank=True)

    def generateConfig(self):
        config = {}
        config['connection'] = {}
        config['connection']['type'] = 'ethernet'
        config['connection']['id'] = self.name
        config['connection']['uuid'] = self.uuid
        config['connection']['permissions'] = ''
        config['ipv4'] = {}
        config['ipv4']['may-fail'] = 'false'
        if self.use_dhcp:
            config['ipv4']['method'] = 'auto'
        else:
            config['ipv4']['method'] = 'manual'
            config['ipv4']['address1'] = '%s/%s,%s' % (self.ip4_address, self.ip4_gateway, self.ip4_gateway)
            config['ipv4']['dns'] = ''
            for i in (self.ip4_dns1, self.ip4_dns2):
                if i:
                    config['ipv4']['dns'] += '%s;' %(i,)
        return config

    def writeFile(self):
        l = open(self.fileName, 'w')
        config = self.generateConfig()
        for i in config:
            l.write('[%s]\n' % (i,))
            for j in config[i]:
                l.write('%s=%s\n' % (j, config[i][j]))
            l.write('\n')
        l.close()

    def generateFileName(self):
        nm_dir = settings.NM_CONNETIONS_DIR
        files = os.listdir(nm_dir)
        base_name = ''.join(filter(lambda x: x in string.lowercase+string.uppercase+string.digits,
                                   self.name))
        base = os.path.join(nm_dir, base_name)
        suffix = 0
        name = base
        while name in files:
            name = base + str(suffix)
            suffix += 1
        return name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        self.writeFile()
        super(Network, self).save(*args, **kwargs)

class WireslessNetwork(Network):
    SECURITY_TYPE = (
      ('OP', 'Open'),
      ('WEP', 'WEP'),
      ('WPA', 'WPA')
    )

    def generateConfig(self):
        config = super(WireslessNetwork, self).generateConfig()
        config['connection']['type'] = 'wifi'
        config['wifi'] = {}
        config['wifi']['mode'] = 'infrastructure'
        config['wifi']['ssid'] = self.essid
        if self.security_type != 'OP':
          config['wifi-security'] = {}
          config['wifi-security']['key-mgmt'] = 'wpa-psk'
          config['wifi-security']['psk'] = self.password
        return config

    essid = models.CharField(max_length=128)
    security_type = models.CharField(max_length = 8, choices = SECURITY_TYPE)
    password = models.CharField(max_length=128, blank=True)
