from pydantic import BaseModel
from typing import List


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


class ComparisonResult(BaseModel):
    only_in_p10: List[Package]
    only_in_sisyphus: List[Package]
    higher_in_sisyphus: List[Package]
