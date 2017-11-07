#!/bin/bash

cd $(dirname $0)

rm -rf logs/* work/*
rm -rf `find ./ -name '*.pyc'`
