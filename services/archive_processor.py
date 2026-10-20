from utilities.is_archive import is_archive

def process_archive(
    source,
    archive_name,
    pattern,
    parent_path="",
    depth=0
):
    archive_name = archive_name.lower()

    if not is_archive(archive_name):
        return []

    if archive_name.endswith(".zip"):
        from services.zip_processor import process_zip
        return process_zip(
            source,
            pattern,
            parent_path,
            depth
        )

    if archive_name.endswith(".tar"):
        from services.tar_processor import process_tar
        return process_tar(
            source,
            pattern,
            parent_path,
            depth
        )

    from services.tar_processor import process_tar
    return process_tar(
        source,
        pattern,
        parent_path,
        depth,
        "r:gz"
    )
