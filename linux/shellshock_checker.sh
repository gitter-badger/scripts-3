#!/bin/bash

env CVE_2014_6271="() { echo 'FUCK';}; echo 'Has CVE_2014_6271'" bash -c CVE_2014_6271

env CVE_2014_7169='() { (a)=>\' bash -c "echo Has CVE_2014_7169"; cat echo
