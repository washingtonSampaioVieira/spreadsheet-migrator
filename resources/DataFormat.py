from config import DatabaseField


class DataFormat:
    def __init__(self, custom_format):
        self.custom_format = custom_format

    def format_db(self, data):
        formatted_obj = {}

        for value in self.custom_format.items():
            key = value[0]
            format_function = value[1][1]

            data_value = data[key]
            new_data = format_function(data_value)
            print(new_data)

    def format(self, obj_id, data):
        formatted_obj = {DatabaseField.ID: obj_id}

        for value in self.custom_format.items():
            obj_key = value[0]
            data_properties = value[1]

            data_key = data_properties[0]
            treatment_function = data_properties[1]

            if not callable(data_key):
                data_value = treatment_function(data[data_key])
            else:
                data_value = data_key(data, treatment_function)

            formatted_obj[obj_key] = data_value

        return formatted_obj
