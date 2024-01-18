from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    MetaData,
    DateTime,
    Date,
    func,
    Boolean,
)

from sqlalchemy.dialects.postgresql import JSON, ARRAY, TEXT, BYTEA, UUID

# from geoalchemy2 import Geography


# *************
# * CRUD User *
# *************
def createCrudUser(metadata: MetaData) -> Table:
    return Table(
        "crud_users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String(100), unique=True, nullable=False),
        Column("email", String, nullable=False),
        Column("disabled", Boolean),
        Column("hashed_password", String, nullable=False),
        Column("data", JSON, nullable=False),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# ***********
# * Empresa *
# ***********
def createCompanyModel(metadata: MetaData) -> Table:
    return Table(
        "companies",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(100), unique=True, nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# **********
# * Granja *
# **********
def createFarmModel(metadata: MetaData) -> Table:
    return Table(
        "farms",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("company_id", Integer, ForeignKey("companies.id")),
        Column("name", String(100), unique=True, nullable=False),
        Column("location", JSON),
        Column("data", JSON),
        Column("created_at", Date, default=func.now()),
        Column("updated_at", DateTime),
    )


# ***********
# * Cultivo *
# ***********
def createCropModel(metadata: MetaData) -> Table:
    return Table(
        "crops",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("farm_id", Integer, ForeignKey("farms.id")),
        Column("crop", String(100), nullable=False),
        Column("crop_plot", String(50), nullable=False),
        Column("is_active", Boolean, default=True),
        Column("seedtime", Date),
        Column("harvest_dates", ARRAY(Date)),
        Column("end_of_crop", Date),
        Column("location", JSON),
        Column("categories", ARRAY(String), nullable=False),
        Column("varieties", JSON, nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# **************
# * Trabajador *
# **************
def createWorkerModel(metadata: MetaData) -> Table:
    return Table(
        "workers",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("farm_id", Integer, ForeignKey("farms.id")),
        Column("name", String(50), nullable=False),
        Column("telegram_user", String(50), nullable=False, unique=True),
        Column("chat_id", Integer, unique=True),
        Column("photography", BYTEA),
        Column("contact", String(100)),
        Column("is_active", Boolean, default=True),
        Column("position", ARRAY(String), nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# ************************
# * Cultivo - Trabajador *
# ************************
def createCropWorkerModel(metadata: MetaData) -> Table:
    return Table(
        "crops_workers",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("crop_id", Integer, ForeignKey("crops.id")),
        Column("worker_id", Integer, ForeignKey("workers.id")),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# **********
# * Sesion *
# **********
def createSessionModel(metadata: MetaData) -> Table:
    return Table(
        "sessions",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("worker_id", Integer, ForeignKey("workers.id")),
        Column("main_message_id", Integer),
        Column("current_action", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# **********************
# * Sistema de Control *
# **********************
def createControlSystemModel(metadata: MetaData) -> Table:
    return Table(
        "control_systems",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("crop_id", Integer, ForeignKey("crops.id")),
        Column("uuid", UUID, nullable=False, unique=True),
        Column("device", String(100), nullable=False),
        Column("description", TEXT),
        Column("categories", ARRAY(String), nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# *******************************
# * Sesion - Sistema de Control *
# *******************************
def createSessionControlSystemModel(metadata: MetaData) -> Table:
    return Table(
        "sessions_control_system",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("session_id", Integer, ForeignKey("sessions.id")),
        Column("control_system_id", Integer, ForeignKey("control_systems.id")),
    )


# ************
# * Actuador *
# ************
def createActuatorModel(metadata: MetaData) -> Table:
    return Table(
        "actuators",
        metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "control_system_id",
            Integer,
            ForeignKey("control_systems.id"),
        ),
        Column("uuid", String(10), nullable=False),
        Column("ref", String(100), nullable=False),
        Column("control_type", String(100), nullable=False),
        Column("description", TEXT),
        Column("categories", ARRAY(String), nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )


# **********
# * Sensor *
# **********
def createSensorModel(metadata: MetaData) -> Table:
    return Table(
        "sensors",
        metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "control_system_id",
            Integer,
            ForeignKey("control_systems.id"),
        ),
        Column("uuid", String(10), nullable=False),
        Column("ref", String(100), nullable=False),
        Column("control_type", String(100), nullable=False),
        Column("description", TEXT),
        Column("categories", ARRAY(String), nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )
