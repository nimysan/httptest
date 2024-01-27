import xml.etree.ElementTree as ET

tree = ET.parse("sample.mpd")  # 载入数据
# root = tree.getroot()
print(tree.getroot())
# segment = tree.find(".//SegmentTemplate")
# start_number = segment.get('startNumber')
els = tree.getroot().iterfind(".//ServiceDescription")
print(els)
for node in els:
    print("node", node['id'])
