import logging
import random
import time

import fastapi

app = fastapi.FastAPI()

main_logger = logging.getLogger("main_logger")
main_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
handler.setFormatter(formatter)
main_logger.addHandler(handler)


def make_log(
    logger: logging.Logger,
    data: dict,
    level: str = "info",
) -> None:
    log_method = getattr(logger, level, logger.info)
    log_method(data)


TIMEOUT_CHANCE = 0.25
DELAY_CHANCE = 0.5

CORS_HEADERS = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Origin": "http://localhost:3000",
}

RESPONSE = {
    "status": "success",
}


@app.get("/endpoint")
def get_order(response: fastapi.Response) -> fastapi.Response:
    random_value = random.random()

    if random_value < TIMEOUT_CHANCE:
        make_log(
            main_logger,
            {
                "msg": "Timeout expected",
            },
            level="info",
        )
        time.sleep(60)
        return fastapi.Response(
            status_code=529,
            content="<html><body><h1>Server is busy. Please try again later.</h1></body></html>",
        )
    if random_value < TIMEOUT_CHANCE + DELAY_CHANCE:
        sleep_time = random.randint(5, 30)
        make_log(
            main_logger,
            {
                "msg": "Artificial delay",
                "delay_seconds": sleep_time,
            },
            level="info",
        )
        time.sleep(sleep_time)
    else:
        make_log(
            main_logger,
            {
                "msg": "Normal operation",
            },
            level="info",
        )

    for key, value in CORS_HEADERS.items():
        response.headers.append(key, value)

    return RESPONSE  # type: ignore


@app.options("/endpoint")
def options_order_by_id(
    response: fastapi.Response,  # noqa: ARG001
) -> fastapi.Response:
    return fastapi.Response(
        status_code=204,
        headers=CORS_HEADERS.copy(),
    )
