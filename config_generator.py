#!/usr/bin/env python3

import csv
import os
import argparse
import re
from datetime import datetime
import zipfile

def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()

def generate_config(template, row):
    config = template
    for key, value in row.items():
        config = config.replace(key, value)
    return config

def log_message(log_file, message):
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now().isoformat()} - {message}\n")

def zip_output_dir(output_dir, zip_filename):
    zip_path = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file != zip_filename and not file.endswith('.log'):
                    zipf.write(os.path.join(root, file), arcname=file)
    return zip_path

def main():
    parser = argparse.ArgumentParser(description="Generate configuration files from a template and CSV input.")
    parser.add_argument('-t', '--template', required=True, help='Path to the template file')
    parser.add_argument('-c', '--csv', required=True, help='Path to the CSV file containing values')
    parser.add_argument('-o', '--output-dir', default='configs', help='Directory to save the generated config files (default: ./configs)')
    parser.add_argument('-f', '--filename-column', required=True, help='Unbracketed column name to use for naming config files')
    parser.add_argument('-z', '--zip', action='store_true', help='Create a ZIP file of the generated configs')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    log_file_path = os.path.join(args.output_dir, "generation.log")
    template = load_template(args.template)

    try:
        with open(args.csv, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            cleaned_headers = [h.strip() for h in reader.fieldnames]
            reader.fieldnames = cleaned_headers

            bracketed_key = f"[{args.filename_column}]"
            if bracketed_key not in cleaned_headers:
                raise ValueError(f"Filename column '{bracketed_key}' not found in CSV headers: {cleaned_headers}")

            for row in reader:
                try:
                    config_text = generate_config(template, row)
                    safe_filename = re.sub(r'[^\w\-_\. ]', '_', row[bracketed_key]) + '.txt'
                    output_path = os.path.join(args.output_dir, safe_filename)

                    with open(output_path, 'w') as outfile:
                        outfile.write(config_text)

                    log_message(log_file_path, f"SUCCESS: Generated {output_path}")
                    print(f"Generated: {output_path}")
                except Exception as e:
                    log_message(log_file_path, f"FAILED: Could not generate file for row {row} - {e}")
                    print(f"Failed to generate config for row: {row} - Error: {e}")

            if args.zip:
                zip_path = zip_output_dir(args.output_dir, "configs.zip")
                log_message(log_file_path, f"ZIPPED: Output files archived to {zip_path}")
                print(f"Zipped output to: {zip_path}")

    except Exception as e:
        log_message(log_file_path, f"ERROR: Script failed - {e}")
        raise

if __name__ == '__main__':
    main()
