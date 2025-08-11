# ADGM Corporate Agent – Document Compliance Checker

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

Automate **corporate document compliance checks** for **Abu Dhabi Global Market (ADGM)** regulations.  
This tool uses **rule-based validation + citation mapping** to detect missing documents, compliance violations, and jurisdiction errors.


##  Features

- ** Document Type Detection** – Identifies corporate documents (AoA, MoA, Board Resolution, etc.) from `.docx` content.
- ** Process Recognition** – Automatically detects if the uploaded files are for *Company Incorporation*.
- ** Compliance Verification** – Checks against ADGM Companies Regulations 2020.
- ** Citations & Rule Mapping** – Links each issue to its exact regulation excerpt.
- ** Inline Review Output** – Option to insert comments/highlights into `.docx`.
- ** Structured JSON Reports** – Generates compliance summaries for downstream processing.

---

## Project Structure

```
adgm_corporate_agent/
│
├── app.py                              # Streamlit app entry point
├── corporate_agent.py                   # Core logic: detection, checklist, reporting
├── rule_config.py                       # Compliance rules mapping
├── adgm_companies_regulations_2020.txt  # Regulation excerpts
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```

---

## Installation

```bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
# Run the Streamlit app
streamlit run app.py
```

### Steps inside the app:
1. **Upload Corporate Documents** (`.docx`).
2. The system will:
   - Detect document type
   - Match against the incorporation checklist
   - Apply ADGM compliance rules
3. **View JSON Report** or download reviewed `.docx` with comments.

---

## Compliance Rules

The rules are stored in [`rule_config.py`](rule_config.py) and citations are linked to  
[`adgm_companies_regulations_2020.txt`](adgm_companies_regulations_2020.txt).

| Rule ID                          | Document Type                   | Severity | Description |
|----------------------------------|----------------------------------|----------|-------------|
| JURISDICTION_ADGM                | Articles of Association         | High     | Must specify ADGM jurisdiction |
| MISSING_SIGNATORY                | Memorandum of Association       | Medium   | Must include signatory section |
| REQ_ARTICLES_ASSOCIATION         | Articles of Association         | High     | Filing requirement |
| REQ_MEMORANDUM_ASSOCIATION       | Memorandum of Association       | High     | Filing requirement |
| REQ_BOARD_RESOLUTION             | Board Resolution                | High     | Mandatory corporate approval record |
| REQ_SHAREHOLDER_RESOLUTION       | Shareholder Resolution          | High     | Required for major decisions |
| REQ_INCORP_APP_FORM              | Incorporation Application Form  | High     | Mandatory form for incorporation |
| REQ_UBO_DECLARATION              | UBO Declaration Form            | High     | Beneficial ownership disclosure |
| REQ_REGISTER_MEMBERS_DIRECTORS   | Register of Members and Directors| High    | Corporate register requirement |
| REQ_CHANGE_ADDRESS_NOTICE        | Change of Registered Address Notice | High  | Notify Registrar of address changes |

---

## Output Example

**Sample JSON Report**
```json
{
  "process": "Company Incorporation",
  "documents_uploaded": 2,
  "required_documents": 8,
  "missing_documents": ["Board Resolution", "UBO Declaration Form"],
  "issues_found": [
    {
      "rule_id": "JURISDICTION_ADGM",
      "issue": "Jurisdiction clause does not specify ADGM",
      "severity": "High",
      "citation": "ADGM Companies Regulations 2020 — Article 6 – Jurisdiction..."
    }
  ]
}
```

---

## 📜 License
This project is released under the **MIT License** – free to use and modify.

---

## Contributing
Pull requests are welcome!  
If you have improvements for detection logic, rule accuracy, or regulation mapping, please submit an issue or PR.

---

**Author:** Abishyanth.S

---

## requirements.txt
```txt
streamlit
python-docx
pandas
tensorflow
torch
```