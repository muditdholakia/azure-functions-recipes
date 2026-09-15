import hmac
import json
import logging
import os
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def parse_job(raw):
    if len(raw) > 65536:
        raise ValueError("Job exceeds 64 KiB")
    job = json.loads(raw)
    if not isinstance(job, dict) or not isinstance(job.get("job_id"), str) or not 1 <= len(job["job_id"]) <= 100:
        raise ValueError("Expected an object with a short string job_id")
    return job

@app.function_name(name="Hello")
@app.route(route="hello", methods=["GET"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "world")
    if len(name) > 80:
        return func.HttpResponse("Name too long", status_code=400)
    return func.HttpResponse(json.dumps({"message": f"Hello, {name}"}), mimetype="application/json")

@app.function_name(name="Heartbeat")
@app.timer_trigger(schedule="0 */15 * * * *", arg_name="timer", run_on_startup=False, use_monitor=True)
def heartbeat(timer: func.TimerRequest):
    logging.info("Heartbeat; past_due=%s", timer.past_due)

@app.function_name(name="QueueJob")
@app.queue_trigger(arg_name="message", queue_name="learning-jobs", connection="AzureWebJobsStorage")
def queue_job(message: func.QueueMessage):
    parse_job(message.get_body())
    logging.info("Validated queue job")

@app.function_name(name="GridEvent")
@app.event_grid_trigger(arg_name="event")
def grid_event(event: func.EventGridEvent):
    logging.info("Event Grid type=%s", event.event_type)

@app.function_name(name="ServiceBusJob")
@app.service_bus_queue_trigger(arg_name="message", queue_name="learning-jobs", connection="SERVICE_BUS_CONNECTION")
def service_bus_job(message: func.ServiceBusMessage):
    parse_job(message.get_body())
    logging.info("Validated Service Bus job")

@app.function_name(name="GraphNotifications")
@app.route(route="graph-notifications", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def graph_notifications(req: func.HttpRequest) -> func.HttpResponse:
    token = req.params.get("validationToken")
    if token is not None:
        return func.HttpResponse(token, mimetype="text/plain")
    expected = os.environ.get("GRAPH_CLIENT_STATE", "")
    if not expected or expected.startswith("REPLACE"):
        return func.HttpResponse("Webhook not configured", status_code=503)
    if len(req.get_body()) > 65536:
        return func.HttpResponse("Payload too large", status_code=413)
    try:
        payload = req.get_json()
        items = payload.get("value") if isinstance(payload, dict) else None
        if not isinstance(items, list) or not items or len(items) > 100:
            raise ValueError("Invalid notifications")
        for item in items:
            state = item.get("clientState") if isinstance(item, dict) else None
            if not isinstance(state, str) or not hmac.compare_digest(state.encode(), expected.encode()):
                return func.HttpResponse("Invalid client state", status_code=403)
    except (ValueError, TypeError):
        return func.HttpResponse("Invalid payload", status_code=400)
    logging.info("Validated %d Graph notifications; no data mutations", len(items))
    return func.HttpResponse(status_code=202)
