import os
import shutil
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(".env")

src = os.getenv("SOURCE_PARENT")
print(f"Source: {src}")
dst = os.getenv("DESTINATION_PARENT")
print(f"Destination: {dst}")

def clean_destination(source, destination):
    # copy files from destination that are not in source to "IsDeleted" folder

    # Convert to Path objects for easier path manipulations
    source = Path(source)
    destination = Path(destination)

    if not destination.exists():
        # throw error
        print("Destination does not exist")
        return
    
    rawSource = source / "raw"
    rawDestination = destination / "raw"
    isDeletedFolder = destination / "IsDeleted"

    if not rawSource.exists():
        # throw error
        print("Source does not exist")
        return
    
    if not rawDestination.exists():
        # throw error
        print("Destination does not exist")
        return
    
    # Do a recursive loop through the rawDestination folder
    for root, dirs, files in os.walk(rawDestination):
        for file in files:
            item = Path(root) / file

            # Check if the item is a file
            if item.is_file():
                # Construct the corresponding path in the rawSource directory
                source_item = rawSource / item.relative_to(rawDestination)

                if source_item.exists():
                    logging.debug(f"Source item {source_item} exists")                    
                else:
                    # Check if the file is not present in the rawSource                
                    deleted_item = isDeletedFolder / item.relative_to(rawDestination)
                    if not deleted_item.parent.exists():
                        deleted_item.parent.mkdir(parents=True, exist_ok=True)
                    print(f"Moving {item} to {deleted_item}")
                    shutil.move(item, deleted_item)


def sync_directories(source, destination):
    # Convert to Path objects for easier path manipulations

    # Convert to Path objects for easier path manipulations
    source = Path(source)
    destination = Path(destination)

    if not destination.exists():
        # throw error
        print("Destination does not exist")
        return
    
    rawSource = source / "raw"
    rawDestination = destination / "raw"
    isDeletedFolder = destination / "IsDeleted"

    if not rawSource.exists():
        # throw error
        print("Source does not exist")
        return
    
    if not rawDestination.exists():
        # throw error
        print("Destination does not exist")
        return

    # Do a recursive loop through the rawDestination folder
    for root, dirs, files in os.walk(rawSource):
        for file in files:
            item = Path(root) / file

            # Check if the item is a file
            if item.is_file():
                # Construct the corresponding path in the rawSource directory
                destination_item = rawDestination / item.relative_to(rawSource)

                if destination_item.exists():
                    logging.debug(f"Source item {destination_item} exists")                    
                else:
                    # Copy the file to the destination
                    print(f"Copying {item} to {destination_item}")

                    if not destination_item.parent.exists():
                        destination_item.parent.mkdir(parents=True, exist_ok=True)

                    shutil.copy2(item, destination_item)


# Example usage
clean_destination(src, dst)
sync_directories(src, dst)
