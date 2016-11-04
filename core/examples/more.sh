#!/usr/bin/env bash

#Hippocampe: Intel aggregator
#@author 2015 CERT-BDF <cert@banque-france.fr>
#@see The GNU Public License (GPL)
#
#This file is part of Hippocampe.
#
#Hippocampe is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#Hippocampe is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License along
#with Hippocampe; if not, write to the Free Software Foundation, Inc.,
#59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#or see <http://www.gnu.org/licenses/>.
#

curl -i -H "Content-Type: application/json" -X POST -d '
{
	"http://www.mkpoytuyr.com/f/" : {"type" : "url"},
	"199.9.24.1" : {"type" : "ip"},
	"198.23.78.98" : {"type" : "ip"},
	"223.184.173.74" : {"type" : "ip"}
}' http://localhost:5000/hippocampe/api/v1.0/more


