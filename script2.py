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


def remove_tag_from_xml_file(root, tags):

    # find all corresponding elements
    deleted_elements = []
    for tag in tags:
        deleted_elements += root.findall(tag)

    # remove elements
    for x in deleted_elements:
        root.remove(x)

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

    full_txt = "".join(lines)
    with open(file_path, "w") as file_:
        file_.write(full_txt)

def modif_xml_file(xml_file_path:str, old_model_:str, new_model_:str, removed_elements, removed_attrib):

    # enlever les balises modifications
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    remove_tag_from_xml_file(root, removed_elements)

    # Save xml file with current modification
    new_xml_path = f"{output_folder}/{xml_file_path.replace(old_model_, new_model_)}"
    with open(new_xml_path, "wb") as output_xml:
        output_xml.write(ET.tostring(root))

    # remove attributes
    remove_attributes_from_file(new_xml_path, removed_attrib)
    replace_text_in_file(new_xml_path, old_model, new_model)

if __name__ == "__main__":

    # TODO: modify with necessary values
    entry_folder = "./"
    output_folder = "./output"
    old_model = 'E6666Y'
    new_model = 'E10000Y'
    attributes_to_be_removed = ["updateNumberId", "barreDeRev"]
    elements_to_be_removed = ["modifications"]

    create_folder(output_folder)

    for file in os.scandir(entry_folder):
        if file.is_file() and file.name.endswith(".xml"):
            modif_xml_file(file.path, old_model, new_model, elements_to_be_removed, attributes_to_be_removed)