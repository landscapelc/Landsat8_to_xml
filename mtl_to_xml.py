# Convert Landsat MTL text files to .xml using standard ElementTree.
# Python 3.8

import fileinput
import xml.etree.ElementTree as etree

class MTLConverter:

    def target_mode(self, file_name):
        # Send a single file to the mtl_to_xml conversion method.
        mtl_dict = {file_name: file_name}
        self.mtl_to_xml(mtl_dict)

    def mtl_to_xml(self, mtl_dict):
        # Converts Landsat MTL metadata file to XML.
        # Output the XML in the same directory as the MTL

        for key in mtl_dict:
            try:
                with fileinput.input(files=key, mode='r') as f:
                    # Read first line of MTL as root Element.
                    first_line = f.readline().strip()
                    # For it's tree-like structure, MTL files are organized in 'Groups = Group_Name_Here'.
                    # We want to strip out 'Groups = ' and get only the Group name.
                    first_line = first_line[(first_line.index('=')) + 2:]
                    # Create the root of the ElementTree from the first Group in the MTL file.
                    root = etree.Element(first_line)
                    # Holding variable for storing current Element
                    current_group = ''

                    for line in f:
                        # Remove unneeded whitespace.
                        temp = line.strip()
                        # Remove unneeded double quotes.
                        temp = temp.replace("\"", "")

                        # Silently break when hitting end of MTL file.
                        if temp == 'END':
                            break

                        try:
                            # MTL is structured like a series of key:value pairs separated by an '='.
                            # pre gets the 'key' before the '='
                            # post get the 'value' after the '='
                            pre = temp[0:temp.index('=') - 1]
                            post = temp[temp.index('=') + 2:]
                        except Exception as e:
                            # A catch-all Exception block isn't a good idea.
                            # When we hit the end of the file, silently break.
                            print('Make sure you\'re using an un-edited MTL file.')
                            print(e)
                            break
                        # MTL files use End_Group to denote the end of an Element.
                        # When we hit the end of an element, silently continue.
                        if pre == 'END_GROUP':
                            continue
                        # MTL files use Group to denote the start of an Element.
                        elif pre == 'GROUP' in line:
                            # Add the Group to the ElementTree as a SubElement
                            etree.SubElement(root, post)
                            # This temp var points to the current MTL Group, and is used in the next elif statement.
                            current_group = post
                        elif '=' in line:
                            # From the root of the ElementTree, find the current_group and establish a new SubElement.
                            # Sets the key in key:value.
                            element = etree.SubElement(root.find(current_group), pre)
                            # Add text to the SubElement. Sets the value in key:value.
                            element.text = post

                    # Indent the new XML file for pretty print.
                    for element in root:
                        self.indent(element)

                    # New .xml file to be created
                    new_file = key.replace('.txt', '.xml')

                    # Build an ElementTree from the Elements and SubElements created above.
                    xml_tree = etree.ElementTree(root)

                    # Write out the ElementTree to the new .xml file.
                    xml_tree.write(new_file, encoding="us-ascii", xml_declaration=True)

            except FileNotFoundError:
                print('That file does not exist.')
            except Exception as e:
                print('Something went wrong.')
                print(e)

    def indent(self, elem, level=0):

        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

def main():
    # Fill in your file_name of the txt
    file_name = "file_name"
    conv = MTLConverter()
    conv.target_mode(file_name)

if __name__ == '__main__':
    main()
