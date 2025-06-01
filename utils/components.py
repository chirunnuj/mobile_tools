import xml.etree.ElementTree as ET

def get_all_exported_components(file):
    """
    Extracts all permissions from the AndroidManifest.xml file and categorizes them.

    Args:
        file (str): Path to the AndroidManifest.xml file.

    Returns:
        list: A list of dictionaries containing permission details.
    """

    exported_components = []

    try:
        tree = ET.parse(file)
        root = tree.getroot()
        
        android_ns = '{http://schemas.android.com/apk/res/android}'
        standard_permissions_prefix = 'android.permission.'

        # Collect all declared permissions
        # declared_permissions = set(
        #     permission.get(f"{android_ns}name") 
        #     for permission in root.findall(f".//permission")
        # )
        # print(declared_permissions)

        # Collect all used permissions
        uses_permissions = set(
            permission.get(f"{android_ns}name")
            for permission in root.findall(f".//uses-permission")
        )
        # print(used_permissions)

        #Iterate through application components
        for component_type in ['activity', 'service', 'receiver', 'provider']:
            for component in root.findall(f".//{component_type}"):
                exported = component.get(f"{android_ns}exported")
                if exported == 'true':
                    name = component.get(f"{android_ns}name")
                    permission = component.get(f"{android_ns}permission")
                    exported = component.get(f"{android_ns}exported", 'false')

                    # Process permission
                    permissions = []
                    if permission:                            
                        is_standard = 'y' if permission.startswith(standard_permissions_prefix) else 'n'
                        if is_standard == 'n':
                            is_declared = 'y' if permission in uses_permissions else 'n'
                        else:
                            is_declared = 'n'
                        permissions.append({
                            'permission': permission,
                            'is_standard': is_standard,
                            'is_declared': is_declared
                        })

                    intent_filters = []
                    for intent_filter in component.findall('intent-filter'):
                        actions = [action.get(f"{android_ns}name") for action in intent_filter.findall('action')]
                        categories = [category.get(f"{android_ns}name") for category in intent_filter.findall('category')]
                        data_elements = [
                            {
                                'scheme': data.get(f"{android_ns}scheme"),
                                'host': data.get(f"{android_ns}host"),
                                'path': data.get(f"{android_ns}path"),
                                'mimeType': data.get(f"{android_ns}mimeType")
                            }
                            for data in intent_filter.findall('data')
                        ]

                        # Filter out null items in data
                        data_elements = [
                            {key: value for key, value in data_item.items() if value is not None}
                            for data_item in data_elements 
                            if any(value is not None for value in data_item.values())
                        ]


                        intent_filters.append({
                            "actions": actions,
                            "categories": categories,
                            "data": data_elements
                        }) 

                    exported_components.append({
                        'type': component_type,
                        'name': name,
                        'exported': exported,
                        "permission": permissions,
                        "intent_filters": intent_filters
                    })
    except ET.parseError:
        print(f"Error parsing XML file: {file}")
    except FileNotFoundError:
        print(f"File not found: {file}")


    return exported_components