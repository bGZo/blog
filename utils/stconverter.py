import argparse
import opencc
import os

def convert_file_to_target_language(file, option):
    converter = opencc.OpenCC(option)
    with open(file, 'r') as f:
        file_content = f.read()
    target_content = converter.convert(file_content)
    
    with open(file, 'w') as f:
        f.write(target_content)

def convert_fils_in_directory(directory, option):
    for root,dirs,files in os.walk(directory):
        for file in files:
            current_dir = root
            current_file = os.path.join(root, file)
            convert_file_to_target_language(current_file, option)
            print("Process " + file + " successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', action = 'store',
                        help='Type in your directory')
    parser.add_argument('-t','--TraditionalChinese', action = 'store_true',
                        help='Convert to Simplied Chinese')
    parser.add_argument('-s','--SimpliedChinese', action = 'store_true',
                        help='Convert to Simplied Chinese')
    args = parser.parse_args()

    if args.TraditionalChinese is True:
        convert_fils_in_directory(args.directory, 's2t.json')
    if args.SimpliedChinese is True:
        convert_fils_in_directory(args.directory, 't2s.json')
