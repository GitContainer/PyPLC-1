import xml.etree.ElementTree as etree
severitys = []
i, j, k = 0, 0, 0
tree = etree.parse('C:/Users/Burygin.vyacheslav/Desktop/tags_without_Data_types.xml')
root = tree.getroot()
for element in root.iter('Property'):
    if element.attrib.get('name') == "Severity":
        severity = element.text
        j += 1
        severitys.append(element)
    if element.attrib.get('name') == "displayPath":
        element.text = element.text + " § " + str(severity)
        k += 1
        if j != k:
            print(element.text)

print(j, " ", k)
for element in root.iter('Alarm'):
    element.remove(severitys[i])
    i += 1

tree.write('C:/Users/Burygin.vyacheslav/Desktop/tags_without_Data_types_Tomsk_2.xml', encoding='UTF-8')


