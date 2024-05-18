# SQLAlchemist

## Joins
```py
worker_session_join = crud_manager.db_table.join(
    sessionModel, workerModel.c.id == sessionModel.c.worker_id
)

query = (
    select(
        [
            workerModel.c.id.label("worker_id"),
            workerModel.c.chat_id,
            workerModel.c.name,
            sessionModel.c.id.label("session_id"),
            sessionModel.c.main_message_id,
            sessionModel.c.current_action,
        ]
    )
    .select_from(worker_session_join)
    .where(workerModel.c.telegram_user == f"{username}")
)
```