import os
import xml.etree.ElementTree as ET
import re

def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass
    except FileNotFoundError:
        parent_folder = "/".join(folder_path.split("/")[:-1])
        create_folder(parent_folder)
        create_folder(folder_path)

def remove_elements_from_xml_tree(tree, tags):

    # find all corresponding elements
    parent_map = {c: p for p in tree.iter() for c in p}
    deleted_elements = []
    for tag in tags:
        deleted_elements += tree.findall(f".//{tag}")

    # remove elements
    for x in deleted_elements:
        parent_map[x].remove(x)


def remove_attributes_from_tree(tree, attributes):
    for z in tree.iter():
        for attrib in attributes:
            if attrib in z.attrib:
                del z.attrib[attrib]

# deprecated (not used in script)
def remove_attributes_from_file(file_path, attributes):
    with open(file_path, "r") as file_:
        lines = file_.readlines()

    for idx, line in enumerate(lines):
        for attrib in attributes:
            line = re.sub(f'{attrib}.*=.*".*"', "", line)
        lines[idx] = line

    full_txt = "".join(lines)
    with open(file_path, "w") as file_:
        file_.write(full_txt)

def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, "r") as file_:
        lines = file_.readlines()

    for idx, line in enumerate(lines):
        lines[idx] = line.replace(old_text, new_text)

    with open(file_path, "w") as file_:
        file_.writelines(lines)

def modify_xml_file(xml_file, old_model_:str, new_model_:str, removed_elements, removed_attrib):

    tree = ET.parse(xml_file.path)

    remove_elements_from_xml_tree(tree, removed_elements)
    remove_attributes_from_tree(tree, removed_attrib)

    # Save xml file with current modification
    new_xml_path = f"{output_folder}/{xml_file.name.replace(old_model_, new_model_)}"
    with open(new_xml_path, "wb") as output_xml:
        tree.write(output_xml)

    # remove attributes
    replace_text_in_file(new_xml_path, old_model, new_model)

if __name__ == "__main__":

    # TODO: modify with necessary values
    entry_folder = "./test_files"
    output_folder = "./output"
    old_model = 'E6666Y'
    new_model = 'E10000Y'
    attributes_to_be_removed = ["updateNumberId", "barreDeRev"]
    elements_to_be_removed = ["modifications"]

    create_folder(output_folder)

    for file in os.scandir(entry_folder):
        if file.is_file() and file.name.endswith(".xml"):
            modify_xml_file(file, old_model, new_model, elements_to_be_removed, attributes_to_be_removed)
