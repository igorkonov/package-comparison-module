from pydantic import BaseModel
from typing import List, Dict, Union


class Package(BaseModel):
    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int
    source: str


class BranchPackages(BaseModel):
    request_args: dict
    length: int
    packages: List[Package]


class PackageInfo(BaseModel):
    count_arches: int
    packages: List[Dict[str, Union[str, int]]]


class ComparisonResult(BaseModel):
    only_in_p10: Dict[str, Union[int, PackageInfo]]
    only_in_sisyphus: Dict[str, Union[int, PackageInfo]]
    higher_in_sisyphus: Dict[str, Union[int, PackageInfo]]
