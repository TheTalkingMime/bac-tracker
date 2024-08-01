import os

def rename_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate through each file
    for filename in files:
        # Create the new filename with the specified prefix
        new_filename = filename[:-4] + 'png'
        
        # Construct the full paths
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_path, new_path)
        
        print(f'Renamed: {filename} -> {new_filename}')

# Example usage
folder_path = 'C:\\Users\\Andrew\\Downloads\\horses'
prefix = '1_'  # Change this to the desired prefix

rename_files(folder_path)
