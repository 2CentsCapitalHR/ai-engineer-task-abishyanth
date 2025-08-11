import os
import json
import io
import warnings
import streamlit as st
import time

# --- Suppress noisy logs ---
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", message=".*torch.classes.*")
warnings.filterwarnings("ignore", message=".*reset_default_graph.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Local imports ---
from corporate_agent import detect_document_type, detect_process_simple, generate_report_simple, verify_checklist
from red_flags import detect_red_flags, insert_inline_comments
from rule_config import RULES

# Optional RAG engine
try:
    from rag_engine import RAGEngine
    rag = RAGEngine(ref_dir="legal_refs")
except Exception as e:
    rag = None
    st.warning(f"RAG Engine failed to initialize: {e}")

st.set_page_config(page_title="ADGM Corporate Agent", layout="wide")
st.title("ADGM Corporate Agent")

# Ensure legal_refs folder exists
if not os.path.exists("legal_refs"):
    os.makedirs("legal_refs")

# Quick UI hint about legal refs
if not any(f.endswith((".txt", ".md")) for f in os.listdir("legal_refs")):
    st.warning("No ADGM legal reference files found in 'legal_refs/'. Add .txt/.md files to enable RAG citations.")

uploaded_files = st.file_uploader(
    "Upload .docx files (multiple allowed)", type=["docx"], accept_multiple_files=True
)

if uploaded_files:
    saved_paths = []
    all_issues = []

    st.write("Uploaded files:")
    for up in uploaded_files:
        # Create unique filename to avoid overwrites
        base_name, ext = os.path.splitext(up.name)
        safe_name = f"{base_name}_{int(time.time())}{ext}"
        save_path = os.path.join("uploads", safe_name)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(up.getbuffer())
        saved_paths.append(save_path)
        st.write(f"- {safe_name}")

        # 1) detect red flags using rules (with RAG if available)
        file_issues = detect_red_flags(save_path, rag_engine=rag)
        all_issues.extend(file_issues)

        # 2) produce reviewed docx with inline highlights & appended summary
        reviewed_path = os.path.join("uploads", f"reviewed_{safe_name}")
        insert_inline_comments(save_path, file_issues, reviewed_path)

        # 3) button to download reviewed docx
        with open(reviewed_path, "rb") as reviewed_file:
            st.download_button(
                f"Download reviewed file for {safe_name}",
                data=reviewed_file,
                file_name=f"reviewed_{safe_name}"
            )

    # 4) check process and missing docs
    detected_types = [detect_document_type(p)[0] for p in saved_paths]
    process = detect_process_simple(detected_types)
    checklist = verify_checklist(detected_types, process)

    # 5) For any missing required documents, add an "issue" with citation if possible
    for missing_doc in checklist["missing_documents"]:
        # find matching rule from RULES (doc_type)
        for rule_id, info in RULES.items():
            if info.get("doc_type") == missing_doc:
                issue = {
                    "rule_id": rule_id,
                    "document": None,
                    "section": "N/A",
                    "issue": f"Missing required document: {missing_doc}",
                    "severity": info.get("severity", "High"),
                    "suggestion": f"Provide the '{missing_doc}' as per ADGM requirements.",
                    "citation": None,
                    "citation_rule": None
                }
                if rag is not None:
                    c = rag.get_citation(info.get("query_template", ""))
                    if c:
                        issue["citation"] = c.get("citation")
                        issue["citation_rule"] = c.get("citation_rule")
                all_issues.append(issue)
                break

    # 6) Generate final JSON report
    report = generate_report_simple(process, saved_paths, issues=all_issues)

    # 7) UI: show report and checklist
    st.subheader("Structured Report (JSON)")
    st.json(report)

    st.subheader("Compliance Checklist")
    if "compliance_checklist" in report:
        st.table(report["compliance_checklist"])
    else:
        st.write("No compliance checklist available.")

    # 8) Save & prepare report for download without writing to disk
    report_json = json.dumps(report, indent=2, ensure_ascii=False)
    st.download_button(
        "Download structured report (JSON)",
        data=report_json,
        file_name="report.json",
        mime="application/json"
    )

    # 9) Summary message
    issue_count = len(all_issues)
    if issue_count > 0:
        st.error(f"Processing completed with {issue_count} issue(s) found.")
    else:
        st.success("Processing completed with no issues found.")

else:
    st.info("Upload one or more .docx files to run the full pipeline: detection → RAG citation → inline comments → final JSON.")