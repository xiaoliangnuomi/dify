from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class OpenDALStorageConfig(BaseSettings):
    OPENDAL_SCHEME: Optional[str] = Field(
        default="fs",
        description="OpenDAL scheme.",
    )
