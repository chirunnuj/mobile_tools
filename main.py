from utils.components import get_all_exported_components
import json
import argparse

def list_exported_components(manifest_path):
    exported_components = get_all_exported_components(manifest_path)

    return exported_components

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract exported components from AndroidManifest.xml")
    parser.add_argument("-f", "--manifest_file", type=str, help="Path to the AndroidManifest.xml file")
    parser.add_argument("-o", "--output_file", default="output.json", type=str, help="Path to the output JSON file")
    args = parser.parse_args()

    manifest_path = args.manifest_file
    output_path = args.output_file


    exported_comp = list_exported_components(manifest_path)

    with open(output_path, 'w') as output_file:
        json.dump(exported_comp, output_file, indent=2)
    
    print(exported_comp)
    print(f"Exported components have been written to {output_path}")
