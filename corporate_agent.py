import os
from docx import Document
from rule_config import RULES, PROCESS_REQUIREMENTS
from rag_engine import RAGEngine

# Document type keyword mapping
DOC_TYPE_KEYWORDS = {
    "Articles of Association": ["articles of association", "articles of incorporation", "aoa"],
    "Memorandum of Association": ["memorandum of association", "memorandum of understanding", "moa", "mou"],
    "Board Resolution": ["board resolution", "resolution of the board", "board of directors resolution"],
    "Shareholder Resolution": ["shareholder resolution", "resolution of the shareholders"],
    "Incorporation Application Form": ["incorporation application", "application for incorporation", "incorporation form"],
    "UBO Declaration Form": ["ubo declaration", "ultimate beneficial owner", "ubo"],
    "Register of Members and Directors": ["register of members", "register of directors", "register of members and directors"],
    "Change of Registered Address Notice": ["change of registered address", "registered address notice", "change of address notice"]
}

COMPANY_INCORP_REQUIRED = list(DOC_TYPE_KEYWORDS.keys())

def extract_text_from_docx(path):
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip() != ""]
    return "\n".join(paragraphs)

def detect_document_type(path):
    text = extract_text_from_docx(path).lower()
    matches = []
    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                matches.append((doc_type, kw))
                break
    if matches:
        detected = matches[0][0]
        matched_keywords = [m[1] for m in matches if m[0] == detected]
        return detected, matched_keywords
    else:
        return "Unknown", []

def detect_process_simple(uploaded_doc_types):
    uploaded_set = set(uploaded_doc_types)
    for process, required_docs in PROCESS_REQUIREMENTS.items():
        if set(required_docs).issubset(uploaded_set):
            return process

    if uploaded_set & set(COMPANY_INCORP_REQUIRED):
        return "Company Incorporation"
    return "Unknown"

def verify_checklist(uploaded_doc_types, process):
    if process in PROCESS_REQUIREMENTS:
        required = PROCESS_REQUIREMENTS[process]
    else:
        required = []
    uploaded = uploaded_doc_types
    missing = [d for d in required if d not in uploaded]
    return {
        "process": process,
        "required_documents": len(required),
        "documents_uploaded": len(uploaded),
        "missing_documents": missing
    }

def generate_report_simple(process, uploaded_doc_paths, issues=None, rag_engine=None):
    if issues is None:
        issues = []

    detected_details = []
    detected_doc_types = []
    for path in uploaded_doc_paths:
        doc_type, matched_keywords = detect_document_type(path)
        detected_doc_types.append(doc_type)
        detected_details.append({
            "file": os.path.basename(path),
            "detected_type": doc_type,
            "matched_keywords": matched_keywords
        })

    checklist_info = verify_checklist(detected_doc_types, process)
    missing_docs = checklist_info["missing_documents"]

    compliance_checklist = []
    for rule_id, rule_data in RULES.items():
        doc_type = rule_data.get("doc_type")
        status = "Compliant"
        citation = None
        citation_rule = None

        if doc_type in missing_docs:
            status = "Violation"
            if rag_engine:
                c = rag_engine.get_citation(rule_data.get("query_template", ""))
                if c:
                    citation = c.get("citation")
                    citation_rule = c.get("citation_rule")
            else:
                citation = rule_data.get("citation")
                citation_rule = rule_data.get("citation_rule")

        for issue in issues:
            if issue.get("rule_id") == rule_id:
                status = "Violation"
                citation = issue.get("citation") or rule_data.get("citation")
                citation_rule = issue.get("citation_rule") or rule_data.get("citation_rule")
                break

        compliance_checklist.append({
            "rule_id": rule_id,
            "doc_type": doc_type,
            "status": status,
            "severity": rule_data.get("severity"),
            "citation": citation,
            "citation_rule": citation_rule
        })

    return {
        "process": process,
        "documents_uploaded": checklist_info["documents_uploaded"],
        "required_documents": checklist_info["required_documents"],
        "missing_documents": checklist_info["missing_documents"],
        "detail_per_file": detected_details,
        "issues_found": issues,
        "compliance_checklist": compliance_checklist
    }
