import json
# Script de prueba para una función Lambda que se activa
# por un evento de S3 (subida de archivo).

def mi_manejador(event, context):
    """
    Esta función se activa por un evento de S3 y registra
    el nombre del archivo subido.
    """
    print("Evento de S3 recibido:", json.dumps(event, indent=2))

    # Extraer el nombre del bucket y la clave (nombre del archivo) del evento
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    print(f"¡Se ha subido un nuevo archivo!")
    print(f"Bucket: {bucket_name}")
    print(f"Nombre del archivo: {file_key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Proceso completado exitosamente!')
    }