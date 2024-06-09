import functools

import httpx
import pydantic


class Model(pydantic.BaseModel):
    id: str
    name: str
    description: str

    class Pricing(pydantic.BaseModel):
        prompt: float
        completion: float
        request: float
        image: float

    pricing: Pricing
    context_length: int


class Response(pydantic.BaseModel):
    data: list[Model]


@functools.cache
def get_models() -> list[Model]:
    response: httpx.Response = httpx.get("https://openrouter.ai/api/v1/models")
    response_json = Response(**response.json())
    models: list[Model] = response_json.data
    return models


@functools.lru_cache
def get_model(model_id: str) -> Model:
    models: list[Model] = get_models()
    for model in models:
        if model.id == model_id:
            return model
        if model.id.split("/")[-1] == model_id:
            return model
    msg: str = f"Model not found: {model_id}"
    raise ValueError(msg)
