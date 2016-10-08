import requests
from xml.etree import ElementTree

#get the response
r = requests.post(uri, data={"xml": parameters}, headers=headers)
#load the response into a tree
tree = ElementTree.fromstring(r.content)
#ask for the data back in string format from the tree (in this example I removed the tags with [12:-14]
WHATYOUWANT = ElementTree.tostring(tree[0][0][0])[12:-14]
