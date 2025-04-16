# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
from os import path as osp

from defusedxml import ElementTree as ET
from PIL import Image


def is_image(file_path):
    """
    Check if the given file path points to a valid image file.

    This function attempts to open the file as an image using the PIL library.
    If the file is not a valid image, it then checks if the file is a valid SVG file
    by parsing it as an XML document and verifying the root tag.

    Args:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file is a valid image or SVG file, False otherwise.
    """

    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError):
        # Check if it's a valid SVG file
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            if root.tag.endswith("svg"):
                return True
        except ET.ParseError:
            return False
    return False


def create_media_symbolic_links(source_folder: str, destination_folder: str):
    """
    Creates symbolic links for image files from the source folder to the destination folder.

    Args:
        source_folder (str): The path to the source folder containing image files.
        destination_folder (str): The path to the destination folder where symbolic links will be created.

    Raises:
        FileNotFoundError: If the source folder does not exist.
        NotADirectoryError: If the source folder is not a directory.

    Notes:
        - Only files identified as images by the `is_image` function will have symbolic links created.
        - The destination folder will be created if it does not exist.
        - Existing symbolic links in the destination folder will not be overwritten.
    """

    if osp.exists(source_folder) and osp.isdir(source_folder):
        # get image files
        image_files = [
            osp.join(source_folder, file)
            for file in os.listdir(source_folder)
            if osp.isfile(osp.join(source_folder, file)) and is_image(osp.join(source_folder, file))
        ]
        # create symbolic links
        os.makedirs(destination_folder, exist_ok=True)
        for file in image_files:
            symbolic_link_path = osp.join(destination_folder, osp.basename(file))
            if not osp.exists(symbolic_link_path):
                os.symlink(file, symbolic_link_path)
