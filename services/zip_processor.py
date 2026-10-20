import zipfile, io
from fnmatch import fnmatch
from utilities.is_archive import is_archive

def process_zip(
    source,
    pattern,
    parent_path="",
    depth=0
):
    matches = []

    with zipfile.ZipFile(source, "r") as z:
        for entry in z.infolist():
            if entry.is_dir():
                continue

            file_name = entry.filename
            full_path = (
                f"{parent_path}/{file_name}"
                if parent_path
                else file_name
            )

            if fnmatch(file_name, pattern):

                matches.append({
                    "full_path": full_path,
                    "file_name": file_name.split("/")[-1],
                    "file_size": entry.file_size,
                    "nesting_depth": depth,
                    "source_archive": parent_path or "root"
                })

            if is_archive(file_name):
                try:
                    nested_data = z.read(file_name)
                    
                    from services.archive_processor import process_archive
                    
                    matches.extend(
                        process_archive(
                            io.BytesIO(nested_data),
                            file_name,
                            pattern,
                            full_path,
                            depth + 1
                        )
                    )
                except Exception as e:
                    print(e)

    return matches
