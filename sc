#!/usr/bin/env python
"""Smart Container wrapper for docker

Usage: sc

Options:
    -h, --help     show help file
    -g, --genMeta  print raw json-ld metadata from docker container
    -r, --run      run docker image with cmd and generate a new container

Example:
    sc --genMeta <image>
    sc --genMeta <container label>
"""

import provmodified as prov
import collections
import docker
import json
from optparse import OptionParser
import subprocess
import sys
import os
from rdflib import plugin, BNode, Graph
from sarge import Command, Capture
import re


def usage():
    print __doc__


def main(argv):
    parser = OptionParser()
    parser.add_option('-g', '--genMeta', dest='image', help='Docker image name')
    parser.add_option('-c', '--create', dest='cmd', help='Docker run image cmd')
    try:
        (options, args) = parser.parse_args()
    except SystemExit:
        return

    if options.image:
        docker.bind_ns("test", "http://daspos.crc.nd.edu/test#")
        
        #p = Command('docker build --rm=false cvmfs-base', stdout=Capture(buffer_size=-1))
        #p.run(async=True)
        
        dlist=[]
        
        """
        
        while(True):
            line = p.stdout.readline().strip() 
            if line!="":
                print line
                if "Step" in line:
                        cmd = line.split(":", 1)
                        print cmd[1].strip()
                        dlist.append("cmd:"+cmd[1].strip())
                elif "---> Running in" in line:
                        container = line.split("---> Running in")
                        print container[1].strip()
                        dlist.append("container:"+container[1].strip())
                elif "--->" in line:
                        image = line.split("--->")
                        print image[1].strip()
                        if re.match("^[A-Za-z0-9_-]+$", image[1].strip()):
                                dlist.append("image:"+image[1].strip())
                elif "Successfully built" in line:
                        break
                else:
                        continue
        
        f = open('dlist-temp','wr')
        for each in dlist:
                f.write(each+'\n')
        f.close()
        
        
        """
        
        f = open('dlist-temp','r')
        for line in f:
                dlist.append(line.strip())
        f.close()
        
        for index in range(len(dlist)):
                if "cmd:FROM" in dlist[index]:
                        index+=1
                        if "image:" in dlist[index]:
                                baseimage = dlist[index].split("image:")[1].strip()
                                print baseimage
                        graph = initialGraph(baseimage)
                        print(docker.serialize(format="turtle"))
                        
        
        #print len(g2)
        #for each in g2:
        #        print each

        #qres = g2.query(
        #        """SELECT DISTINCT ?a ?b
        #        WHERE {
        #            ?a prov:hadDerivation ?b .
        #        }""")

        #for row in qres:
        #    print("%s wasDerivedFrom %s" % row)
        #

def initialGraph(imageid):

        parentid = docker.get_parentid(imageid)
        print "parentid = "+str(parentid)
 
        if str(parentid) != "None":
               currentimage = docker.Image(imageid)
               parentimage = initialGraph(parentid)
               currentimage.set_parent(parentimage)
        else:
               currentimage = docker.Image(imageid)
        
        return currentimage
     

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    main(sys.argv[1:])
