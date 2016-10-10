#!/usr/bin/python
import re

#Let's create some string to reference
strContent = 'this is the string I would like to search SEP123ABC456DEE'

#I'd like to search for anything that starts with SEP followed by 12 characters matching any letter A-Z or number 0-9
reSearch = re.search(r'SEP[A-Z0-9]{12}', strContent)

#Reference the group to pull the match out as a string
reMatch = reSearch.group(0)
