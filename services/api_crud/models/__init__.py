# config
from config import metadata_hic_cibus, metadata_bots

# Model templates
from .bot.models import createBotModel
from .hic_cibus.models import (
    createCompanyModel,
    createFarmModel,
    createWorkerModel,
    createSessionModel,
    createCropModel,
    createCropWorkerModel,
    createControlSystemModel,
    createSessionControlSystemModel,
    createActuatorModel,
    createSensorModel,
    createCrudUser,
)

# Bots
botModel = createBotModel(metadata_bots)

# Hic-cibus
crudUserModel = createCrudUser(metadata_hic_cibus)
companyModel = createCompanyModel(metadata_hic_cibus)
farmModel = createFarmModel(metadata_hic_cibus)
cropModel = createCropModel(metadata_hic_cibus)
workerModel = createWorkerModel(metadata_hic_cibus)
crop_workerModel = createCropWorkerModel(metadata_hic_cibus)
sessionModel = createSessionModel(metadata_hic_cibus)
controlSystemModel = createControlSystemModel(metadata_hic_cibus)
sessions_control_systemModel = createSessionControlSystemModel(metadata_hic_cibus)
actuatorModel = createActuatorModel(metadata_hic_cibus)
sensorModel = createSensorModel(metadata_hic_cibus)
