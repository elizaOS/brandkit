import os
from pathlib import Path
import subprocess

# Supported image extensions for thumbnails
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".gif"}

def create_montage(image_paths, output_path, montage_size="200x200"):
    """
    Create a montage of images using ImageMagick.
    """
    try:
        subprocess.run([
            "montage",
            *image_paths,
            "-geometry", montage_size,  # Thumbnail size
            "-tile", "4x",  # Automatically adjust the number of columns
            output_path
        ], check=True)
        return True
    except Exception as e:
        print(f"Error creating montage: {e}")
        return False

def generate_readme(directory, output_file="README.md"):
    with open(output_file, "w") as readme:
        readme.write("# Media Assets\n\n")
        readme.write("This directory contains the following media assets:\n\n")

        for root, dirs, files in os.walk(directory):
            # Skip hidden directories (e.g., .git)
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            # Skip the root directory itself
            if root == directory:
                relative_path = ""
            else:
                relative_path = os.path.relpath(root, directory)
                readme.write(f"## {relative_path}\n\n")

            # Filter image files
            image_files = [
                f for f in files
                if Path(f).suffix.lower() in IMAGE_EXTENSIONS
            ]

            # Create a montage for folders with more than 8 images
            if len(image_files) > 8:
                montage_path = os.path.join(root, "montage.jpg")
                image_paths = [os.path.join(root, f) for f in image_files]

                if create_montage(image_paths, montage_path):
                    relative_montage_path = os.path.relpath(montage_path, directory)
                    readme.write(f"### Montage of {len(image_files)} images\n\n")
                    readme.write(f'<img src="{relative_montage_path}" alt="Montage" width="800" />\n\n')
                else:
                    readme.write("Failed to generate montage.\n\n")
            else:
                # Create a table for folders with 8 or fewer images
                if files:
                    readme.write("| File | Preview |\n")
                    readme.write("|------|---------|\n")

                    for file in files:
                        if file == output_file or file == "tree.txt":
                            continue  # Skip the README.md and tree.txt files

                        file_path = os.path.join(root, file)
                        relative_file_path = os.path.relpath(file_path, directory)
                        file_extension = Path(file).suffix.lower()

                        # Add a thumbnail preview for image files
                        if file_extension in IMAGE_EXTENSIONS:
                            preview = f'<img src="{relative_file_path}" alt="{file}" width="100" />'
                        else:
                            preview = "No preview available"

                        # Add a row to the table
                        readme.write(f"| [{file}]({relative_file_path}) | {preview} |\n")
                    readme.write("\n")

if __name__ == "__main__":
    current_directory = os.getcwd()
    generate_readme(current_directory)
