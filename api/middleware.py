import logging
import time
import uuid

logger = logging.getLogger("api")

class RequestLoggingMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        started = time.perf_counter()
        response = self.get_response(request)
        elapsed = (time.perf_counter() - started) * 1000
        response["X-Request-ID"] = request.request_id
        logger.info("%s %s -> %s (%.2fms) request_id=%s", request.method, request.path, response.status_code, elapsed, request.request_id)
        return response

