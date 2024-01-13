
from pymongo import MongoClient
from bson.binary import Binary
import io
from PIL import Image


class MongoDBModule:
    def __init__(self, db_url_, db_name_):
        # Specify SSL options
        # ssl_options = {
        #     'ssl': False,
        #     # 'ssl_ca_certs': 'path/to/ca_certificate.pem',  # Update with your CA certificate path
        # }

        self.client = MongoClient(db_url_, ssl_options=ssl_options)
        self.db_name = db_name_
        self.db = self.client[self.db_name]
        if self.db_name not in self.client.list_database_names():
            self.client.admin.command('copydb', fromdb='admin', todb=self.db_name)

    def get_all_collections(self):
        return self.db.list_collection_names()

    def create_collection(self, collection_name):
        if collection_name not in self.get_all_collections():
            self.db.create_collection(collection_name)
            return f"Collection '{collection_name}' created successfully."
        else:
            return f"Collection '{collection_name}' already exists."

    def add_record(self, collection_name, data, image=None):
        collection = self.db[collection_name]

        record = {'data': data}

        if image:
            image_binary = self._convert_image_to_binary(image)
            record['image'] = Binary(image_binary)

        return collection.insert_one(record).inserted_id

    def get_all_records(self, collection_name):
        collection = self.db[collection_name]
        result = []
        _records = collection.find()
        for record in _records:
            data = record['data']
            image = self._get_image_from_binary(record.get('image', None))
            result.append({'data': data, 'image': image})

        return result

    @staticmethod
    def _convert_image_to_binary(image):
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        return img_byte_array.getvalue()

    @staticmethod
    def _get_image_from_binary(image_binary):
        if image_binary:
            return Image.open(io.BytesIO(image_binary))
        else:
            return None


# Example Usage:
if __name__ == "__main__":
    db_user_name = "MongoDBAtlasUser"
    db_password = "MongoDBAtlas2018"
    db_url = f'mongodb+srv://{db_user_name}:{db_password}@causeforbettersociety0.mys1ch6.mongodb.net/'
    db_name = 'sample_check_local'

    mongo_module = MongoDBModule(db_url, db_name)

    # Example: Get all collections
    print(mongo_module.get_all_collections())

    # Example: Create a new collection
    print(mongo_module.create_collection('new_collection'))

    # Example: Add a record with data and image to a collection
    sample_image = Image.open('sample_image.png')  # Replace with the path to your sample image
    record_id = mongo_module.add_record('new_collection', 'sample_data', sample_image)
    print(f"Record added with ID: {record_id}")

    # Example: Get all records from a collection
    records = mongo_module.get_all_records('new_collection')
    print(records)
