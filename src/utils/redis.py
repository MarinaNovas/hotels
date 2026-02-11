from fastapi import Request, Response

def facilities_key_builder(
    func,
    namespace: str,
    request: Request,
    response: Response,
    *args,
    **kwargs,
):
    # игнорируем db и прочие "служебные" зависимости
    # kwargs может содержать db
    kwargs.pop("db", None)

    # ключ на основе URL (путь + query)
    return f"{namespace}:{request.url.path}?{request.url.query}"