from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from models import LoadModelRequest, PredictRequest
from services import NLPService, get_nlp_service

router = APIRouter(prefix="", tags=["Model"])


@router.post("/load")
async def load_model(
    load_request: LoadModelRequest,
    nlp_service: Annotated[NLPService, Depends(get_nlp_service)],
) -> JSONResponse:
    await nlp_service.add_model(model_name=load_request.model)
    return JSONResponse(
        content={"message": "Model loaded successfully"}, status_code=200
    )


@router.get("/models")
async def get_models(
    nlp_service: Annotated[NLPService, Depends(get_nlp_service)],
) -> JSONResponse:
    models = await nlp_service.get_models()
    return JSONResponse(content={"models": models}, status_code=200)


@router.post("/predict")
async def predict(
    predict_request: PredictRequest,
    nlp_service: Annotated[NLPService, Depends(get_nlp_service)],
) -> JSONResponse:
    entities = await nlp_service.extract_entities(
        model_name=predict_request.model, text=predict_request.text
    )
    return JSONResponse(content=entities, status_code=200)


@router.delete("/models/{model_name}")
async def delete_model(
    model_name: str,
    nlp_service: Annotated[NLPService, Depends(get_nlp_service)],
) -> JSONResponse:
    await nlp_service.delete_model(model_name=model_name)
    return JSONResponse(
        content={"message": "Model deleted successfully"}, status_code=200
    )


@router.get("/list")
async def list_predictions(
    nlp_service: Annotated[NLPService, Depends(get_nlp_service)],
) -> JSONResponse:
    history = await nlp_service.history()
    return JSONResponse(content={"history": history}, status_code=200)
