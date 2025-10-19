def abs_path_from_project(relative_path: str):
    import resources
    from pathlib import Path

    return (
    Path (resources.__file__).
    parent.parent. joinpath(relative_path).
    absolute().
    __str__()
    )