Hippocampe: Intels aggregator
@author 2015 CERT-BDF <cert@banque-france.fr>
@see The GNU Public License (GPL)

This file is part of Hippocampe.

Hippocampe is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Hippocampe is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with Hippocampe; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
or see <http://www.gnu.org/licenses/>.


# Hippocampe
In the human brain, the hippocampus is the place of memory. 
With hippocampe, give your organisation a memory and let's remember all Intel you have met ;)

# What does it really do ?
Hippocampe aggregates feeds from internet in an elasticsearch cluster.
It has a REST-API which allows to search into its "memory".

# How does it work ?
It is based on a python script, who fetchs an url, parses it and index it.

#How do I use it ?
Well, just add a configuration file for your feed and run the script ;)

#Technical questions
For questions like:
 * How does it technically work ?
 * How do I request it ?
 * How do I fill in the configuration file ?
 
It would be a bit long to explain that here.. Take a look at the docs folder :)

#Roadmap
 * Extracting Intel from an email or a report 
 * Adding manually Intel
 * Improve the hipposcore by integrating MyWOT in the formula
 * Distinguish fields generate by Hippocampe and fields from the feed
 * Show related Intel (eg, when searching for an url, shows the domain as related if Hippocampe knows it)
 * Index Intel from Misp 

