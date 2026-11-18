from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoginDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=100)

    @field_validator("username", mode="before")
    @classmethod
    def normalizar_username(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    username: str
    rol: str
