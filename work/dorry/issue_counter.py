#!/usr/bin/env python
####################################
#author        terry.li
#date          18/11/2016
#version       1.0.0
#description   counting Dorryweb issues
#              and reporting to slack
####################################

import urllib2
import urllib
import json
import os
import datetime


def getData(type):
        index = 1
        baseurl = "https://api.github.com/repos/MatchboxDorry/dorry-web/issues?state={}&per_page=100&page={}"
        #print baseurl.format(type,index)
        response = urllib2.urlopen(baseurl.format(type,index))
        data = json.load(response)
        length = len(data)
        #print length
        while length == 100 :
                index = index + 1
                data = data.append(json.load(urllib2.urlopen(baseurl.format(type,index))))
                length = len(data)
        return data

def getPullRequestNum(data):
        index = 0
        for item in data:
                try:
                        item['pull_request']
                        index = index + 1
                except Exception as e:
                        pass
        return index

def getIssuesNum(data):
        return len(data) - getPullRequestNum(data)

def getFilterIssuesNum(data,labels):
        index = 0
        for item in data:
                try:
                        label_obj = item['labels']
                        item_labels = []
                        for label_item in label_obj:
                                item_labels.append(label_item['name'])
                        if set(labels).issubset(set(item_labels)):
                                index = index + 1
                        item_labels = []
                except Exception as e:
                        pass
        return index

def reportSlack(payload):
        webhook = "https://hooks.slack.com/services/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"
        content = "{\"text\" :\"" + payload + "\"}"
        #req = urllib2.Request(webhook, urllib.urlencode(content),headers)
        #f = urllib2.urlopen(req)
        #f.read()
        #f.close()
        command = "curl -X POST -k --data-urlencode \'payload="+content+"\' " + webhook
        os.system(command)


def main():
        open_data = getData('open')
        close_data = getData('closed')

        open_issue = getIssuesNum(open_data)
        close_issue = getIssuesNum(close_data)

        open_p0_issue = getFilterIssuesNum(open_data,['priority: 0 (critical)'])
        close_p0_issue = getFilterIssuesNum(close_data,['priority: 0 (critical)'])
        
        open_p1_issue = getFilterIssuesNum(open_data,['priority: 1 (urgent)'])
        close_p1_issue = getFilterIssuesNum(close_data,['priority: 1 (urgent)'])
        
        open_fixed_issue = getFilterIssuesNum(open_data,['flag: fixed'])
        close_fixed_issue = getFilterIssuesNum(close_data,['flag: fixed'])

        open_fixed_p0_issue = getFilterIssuesNum(open_data,['priority: 0 (critical)','flag: fixed'])
        close_fixed_p0_issue = getFilterIssuesNum(close_data,['priority: 0 (critical)','flag: fixed'])
        
        open_fixed_p1_issue = getFilterIssuesNum(open_data,['priority: 1 (urgent)','flag: fixed'])
        close_fixed_p1_issue = getFilterIssuesNum(close_data,['priority: 1 (urgent)','flag: fixed'])

        payload = "==========================================\n" + \
                  datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S') + \
                  "\n------------------open-----------------" + \
                  "\nopen              : " + str(open_issue) + \
                  "\nopen p0           : " + str(open_p0_issue) + \
                  "\nopen fixed        : " + str(open_fixed_issue) + \
                  "\nopen fixed p0     : " + str(open_fixed_p0_issue) + \
                  "\n-----------------closed----------------" + \
                  "\nclosed            : " + str(close_issue) + \
                  "\nclosed p0         : " + str(close_p0_issue) + \
                  "\nclosed fixed      : " + str(close_fixed_issue) + \
                  "\nclosed fixed p0   : " + str(close_fixed_p0_issue) + \
                  "\n=========================================="
        print payload

        reportSlack(payload)

if __name__ == "__main__":
	main()
