from app.workers.celery_app import celery_app

@celery_app.task
def refresh_market_data():
    return {"status": "ok", "task": "refresh_market_data"}

@celery_app.task
def run_strategy_cycle():
    return {"status": "ok", "task": "run_strategy_cycle"}
