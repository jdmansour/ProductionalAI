from basyx.aas import model



# Creating the AssetInformation object
asset_information = model.AssetInformation(asset_kind=model.AssetKind.INSTANCE, global_asset_id='IFW_AAS/Simple_Asset')

# Creating the AAS
identifier_aas = 'IFW_AAS/Simple_AAS'
aas = model.AssetAdministrationShell(id_=identifier_aas, asset_information=asset_information)

# Createing a simple submodel without submodel elements
identifier_submodel = 'IFW_AAS/Simple_Submodel'
submodel = model.Submodel(id_=identifier_submodel)

# Linking the submodel to the AAS
aas.submodel.add(model.ModelReference.from_referable(submodel))

# Creating a simple property and add it to the submodel
semantic_reference = model.ExternalReference(
    (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value='IFW_AAS/Properties/SimpleProperty'
    ),)
)

property_temp = model.Property(
    id_short='Temperature',
    value_type=model.datatypes.Float,
    value=27.3,
    semantic_id=semantic_reference
)
submodel.submodel_element.add(property_temp)


# Accessing the temperature property
print(f'\nOriginal AAS: {aas}')
for element in submodel.submodel_element:
    if isinstance(element, model.Property) and element.id_short == 'Temperature':
        print(f'Property ID: {element.id_short}')
        print(f'Value: {element.value}')


# Updating data in submodel
for element in submodel.submodel_element:
    if isinstance(element, model.Property) and element.id_short == 'Temperature':
        element.value = 30.5

# Verify the update
for element in submodel.submodel_element:
    if isinstance(element, model.Property) and element.id_short == 'Temperature':
        print(f'Updated value: {element.value}')


# Serializing and Saving the AAS
from basyx.aas.adapter.json import write_aas_json_file
store = model.DictObjectStore() # Create a DictObjectStore and add the AAS and Submodel
store.add(aas)
store.add(submodel)
with open('simple_aas.json', 'w') as json_file:
    write_aas_json_file(json_file, store)

# Loading a serialized AAS
from basyx.aas.adapter.json import read_aas_json_file
with open('simple_aas.json', 'r') as json_file:
    loaded_aas_collection = read_aas_json_file(json_file)


aas_temp = loaded_aas_collection.get(identifier_aas)
submodel_temp = loaded_aas_collection.get(identifier_submodel)
print(f'\nLoaded AAS: {aas_temp}')

for element in submodel_temp.submodel_element:
    if isinstance(element, model.Property) and element.id_short == 'Temperature':
        print(f'Property ID: {element.id_short}')
        print(f'Value: {element.value}')
