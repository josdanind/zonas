from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    MetaData,
    DateTime,
    func,
    Boolean,
)

from sqlalchemy.dialects.postgresql import JSON, ARRAY, TEXT, BYTEA

# from geoalchemy2 import Geography


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
        Column("created_at", DateTime, default=func.now()),
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
        Column("location", JSON),
        Column("categories", ARRAY(String), nullable=False),
        Column("variety", String(100), nullable=False),
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
        Column("farm_id", Integer, ForeignKey("farms.id")),
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
        Column("device", String(100), nullable=False),
        Column("description", TEXT),
        Column("categories", ARRAY(String), nullable=False),
        Column("control_type", String(100), nullable=False),
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
        Column("device", String(100), nullable=False),
        Column("description", TEXT),
        Column("categories", ARRAY(String), nullable=False),
        Column("control_type", String(100), nullable=False),
        Column("data", JSON),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )
