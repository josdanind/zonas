#!/bin/bash

REMOTE_SERVER="root@tu_dominio.com"

#  Ruta local de los archivos a enviar
FILE_PATHS=(
    ".env:/root/Zonas"
    "./db_init/bots/activate_bots.json:/root/Zonas/db_init/bots/"
    "./db_init/hic-cibus/company_farm.json:/root/Zonas/db_init/hic-cibus"
    "./db_init/hic-cibus/crops.json:/root/Zonas/db_init/hic-cibus"
    "./db_init/hic-cibus/workers.json:/root/Zonas/db_init/hic-cibus"
)

# Bucle para enviar los archivos uno por uno
for file in "${FILE_PATHS[@]}"; do
    # Obtener la ruta local y la ruta remota del archivo
    local_path="${file%%:*}"
    remote_path="${file#*:}"

    # Comprobar si el archivo existe localmente
    if [ ! -f "$local_path" ]; then
        echo "El archivo $local_path no existe."
        echo "Verificando la existencia del siguiente archivo."
        continue
    fi

    # Enviar el archivo al servidor remoto
    echo "Enviando archivo $local_path a $remote_path en el servidor remoto..."
    scp "$local_path" "$REMOTE_SERVER:$remote_path"

    # Comprobar el estado de salida del comando scp
    if [ $? -eq 0 ]; then
        echo "Archivo $local_path enviado exitosamente a $remote_path."
    else
        echo "Error al enviar el archivo $local_path a $remote_path."
        break
    fi
done