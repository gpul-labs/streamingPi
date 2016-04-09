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

from django.db import models

class Network(models.Model):
    name = models.CharField(max_length = 30)
    use_dhcp = models.BooleanField()
    ip4_address = models.CharField(max_length=16)
    ip4_netmask = models.CharField(max_length=16)
    ip4_gateway = models.CharField(max_length=16)
    ip4_dns1 = models.CharField(max_length=16)
    ip4_dns2 = models.CharField(max_length=16)

class WireslessNetwork(Network):
    SECURITY_TYPE = (
      ('OP', 'Open'),
      ('WEP', 'WEP'),
      ('WPA', 'WPA')
    )
    essid = models.CharField(max_length=128)
    security_type = models.CharField(max_length = 8, choices = SECURITY_TYPE)
    password = models.CharField(max_length=128)
