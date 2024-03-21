import os
import base64
import csv

def add_images_to_csv(image_dir, csv_file):
    # Read the existing CSV file into a list of dictionaries
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Add the image data
    for row in data:
        bib_no = row['Bib No']
        image_file = os.path.join(image_dir, f'{bib_no}.jpg')
        # Check if the image file is jpg
        if image_file.endswith('.jpg'):
            image_file = os.path.join(image_dir, f'{bib_no}.jpeg')

        if os.path.isfile(image_file):
            with open(image_file, 'rb') as f:
                encoded_string = base64.b64encode(f.read()).decode()
                row['Image'] = encoded_string

    # Write the data back to the CSV file
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['Country', 'Bib No', 'Athlete', 'LastName', 'Gender', 'DOB', 'Classification', 'Image']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print(f'Images {image_dir} have been added to {csv_file} at row {bib_no}')


if __name__ == "__main__":
    image_dir = 'images'
    csv_file = 'athlete_images.csv'
    add_images_to_csv(image_dir, csv_file)
    print(f'Images in {image_dir} have been converted to {csv_file}')
    print('Done!')
# Output:
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f'{row["Bib No"]}: {row["Image"][:50]}...')  # Print the first 50 characters of the image data