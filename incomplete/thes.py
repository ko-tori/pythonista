# coding: utf-8
import urllib,urllib2
import xml.etree.ElementTree as ET
key='f0fbc629-85bb-4653-be36-bd329fa3629e'

def grab_xml_definition (word, ref, key):
	#args = urllib.urlencode({})
	uri = "http://www.dictionaryapi.com/api/v1/references/"+urllib.quote_plus(ref)+"/xml/"+urllib.quote_plus(word)+"?key="+urllib.quote_plus(key);
	return urllib2.urlopen(uri)
		
test = ET.fromstring(grab_xml_definition("test", "thesaurus", key).read())