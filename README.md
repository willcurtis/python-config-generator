# Config Generator Script

This Python script generates configuration files from a template and a CSV file. It's designed to be flexible and supports tagged placeholders within both the template and CSV headers.

## 📦 Features

- Uses template files with placeholders like `[hostname]`, `[ip]`, etc.
- Reads CSV files where headers are also enclosed in square brackets (e.g., `[hostname]`)
- Output directory defaults to `./configs` (created if it doesn't exist)
- Logs all output actions to `configs/generation.log`
- Supports creating a `.zip` archive of all generated files

---

## 🚀 Usage

```bash
python3 config_generator.py -t <TEMPLATE_FILE> -c <CSV_FILE> -f <FILENAME_COLUMN> [-o <OUTPUT_DIR>] [-z]
```

### Parameters

| Short | Long             | Required | Description                                                    |
|-------|------------------|----------|----------------------------------------------------------------|
| `-t`  | `--template`     | Yes      | Path to the text file used as the template                     |
| `-c`  | `--csv`          | Yes      | Path to the CSV file containing data values                    |
| `-f`  | `--filename-column` | Yes   | Name of the CSV column (without brackets) to use for filenames |
| `-o`  | `--output-dir`   | No       | Directory for saving output files (default: `./configs`)       |
| `-z`  | `--zip`          | No       | Archive the generated config files into a `configs.zip` file   |

---

## 🧩 Example Template

```text
interface GigabitEthernet0/0
 ip address [ip] 255.255.255.0
 description [hostname]
```

---

## 📄 Example CSV

```csv
[hostname],[ip],[thirdoctet]
router1,192.168.1.1,1
router2,192.168.2.1,2
```

---

## 🗂 Example Output

```
configs/
├── router1.txt
├── router2.txt
├── configs.zip      # (only if --zip is used)
└── generation.log   # records success/failure per file
```

---

## 🛠 Notes

- All placeholders in the template must exactly match the headers in the CSV (including square brackets).
- The `--filename-column` should be provided without brackets.

---

## 🧑‍💻 Author

Will Curtis - The Tech Shed - thetechshed.dev
