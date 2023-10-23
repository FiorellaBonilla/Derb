model_data = [
    {
        'model_name': 'Model1',
        'fields': [
            {
                'field_name': 'field1',
                'field_type': 'CharField'
            },
            {
                'field_name': 'field2',
                'field_type': 'IntegerField'
            }
        ]
    },
    {
        'model_name': 'Model2',
        'fields': [
            {
                'field_name': 'field1',
                'field_type': 'CharField'
            },
            {
                'field_name': 'field2',
                'field_type': 'BooleanField'
            }
        ]
    }
]

# Agregar un nuevo modelo y sus campos
def add_model_and_fields(model_name, fields):
    model_data.append({
        'model_name': model_name,
        'fields': fields
    })

# Eliminar un modelo y sus campos
def remove_model_and_fields(model_name):
    global model_data
    model_data = [model for model in model_data if model['model_name'] != model_name]

# Actualizar campos de un modelo
def update_model_fields(model_name, new_fields):
    for model in model_data:
        if model['model_name'] == model_name:
            model['fields'] = new_fields
            break

# Obtener información de un modelo específico
def get_model_info(model_name):
    for model in model_data:
        if model['model_name'] == model_name:
            return model
    return None
