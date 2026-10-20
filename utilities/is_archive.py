def is_archive(file_name):

    file_name = file_name.lower()

    return (
        file_name.endswith(".zip")
        or file_name.endswith(".tar")
        or file_name.endswith(".tar.gz")
        or file_name.endswith(".tgz")
    )
