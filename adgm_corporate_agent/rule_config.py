"""
Central rule and process configuration.
Each rule has a rule_id, a human readable name, a severity, and a query_template used by RAG.
"""
PROCESS_REQUIREMENTS = {
    "Company Incorporation": [
        "Articles of Association",
        "Memorandum of Association",
        "Board Resolution",
        "Shareholder Resolution",
        "Incorporation Application Form",
        "UBO Declaration Form",
        "Register of Members and Directors",
        "Change of Registered Address Notice"
    ]
}

RULES = {
    "JURISDICTION_ADGM": {
        "doc_type": "Articles of Association",
        "severity": "High",
        "query_template": "Part 6 – Jurisdiction_ADGM",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "MISSING_SIGNATORY": {
        "doc_type": "Memorandum of Association",
        "severity": "Medium",
        "query_template": "Part 33 – Signatory Requirements",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_ARTICLES_ASSOCIATION": {
        "doc_type": "Articles of Association",
        "severity": "High",
        "query_template": "Part 10 – Articles of Association",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_MEMORANDUM_ASSOCIATION": {
        "doc_type": "Memorandum of Association",
        "severity": "High",
        "query_template": "Part 11 – Memorandum of Association",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_BOARD_RESOLUTION": {
        "doc_type": "Board Resolution",
        "severity": "High",
        "query_template": "Part 15 – Board Resolution",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_SHAREHOLDER_RESOLUTION": {
        "doc_type": "Shareholder Resolution",
        "severity": "High",
        "query_template": "Part 16 – Shareholder Resolution",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_INCORP_APP_FORM": {
        "doc_type": "Incorporation Application Form",
        "severity": "High",
        "query_template": "Part 20 – Incorporation Application Form",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_UBO_DECLARATION": {
        "doc_type": "UBO Declaration Form",
        "severity": "High",
        "query_template": "Part 21 – Ultimate Beneficial Owner (UBO) Declaration Form",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_REGISTER_MEMBERS_DIRECTORS": {
        "doc_type": "Register of Members and Directors",
        "severity": "High",
        "query_template": "Part 22 – Register of Members and Directors",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    },
    "REQ_CHANGE_ADDRESS_NOTICE": {
        "doc_type": "Change of Registered Address Notice",
        "severity": "High",
        "query_template": "Part 23 – Change of Registered Address Notice",
        "citation_rule": "adgm_companies_regulations_2020.txt"
    }
}