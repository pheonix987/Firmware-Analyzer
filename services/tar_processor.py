import tarfile, io
from fnmatch import fnmatch
from services.archive_processor import process_archive
from utilities.is_archive import is_archive

def process_tar(
    source,
    pattern,
    parent_path="",
    depth=0,
    read_mode = "r:*"
):

    matches = []

    if isinstance(source, str):

        tar = tarfile.open(
            source,
            read_mode
        )

    else:

        tar = tarfile.open(
            fileobj=source,
            mode=read_mode
        )

    with tar:

        for member in tar.getmembers():

            if not member.isfile():
                continue

            file_name = member.name

            full_path = (
                f"{parent_path}/{file_name}"
                if parent_path
                else file_name
            )

            if fnmatch(file_name, pattern):

                matches.append({
                    "full_path": full_path,
                    "file_name": file_name.split("/")[-1],
                    "file_size": member.size,
                    "nesting_depth": depth,
                    "source_archive": parent_path or "root"
                })

            if is_archive(file_name):

                nested_file = tar.extractfile(member)

                if nested_file:

                    nested_bytes = nested_file.read()

                    matches.extend(
                        process_archive(
                            io.BytesIO(nested_bytes),
                            file_name,
                            pattern,
                            full_path,
                            depth + 1
                        )
                    )

    return matches
