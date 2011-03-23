#!/bin/bash

for i in *; do if [ -d $i/.git ]; then echo -n "$i: "; cd $i; git pull ; cd ..; fi; done

