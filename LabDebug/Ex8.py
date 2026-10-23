# Diagnosis: .replace() changes EVERY ".doc" anywhere in the name, not just the
# ending. So "notes.docx" becomes "notes.pdfx" and "my.docs.doc" gets mangled.
def update_extensions_bad(filenames):
    return [name.replace(".doc", ".pdf") for name in filenames]
 
# Fixed: only change the name if it really ends with ".doc"
def update_extensions(filenames):
    """Changes .doc extensions to .pdf"""
    new_names = []
    for name in filenames:
        if name.endswith(".doc"):
            name = name[:-4] + ".pdf"
        new_names.append(name)
    return new_names
 
print(update_extensions(["annual_report.doc"]))
print(update_extensions(["document.doc"]))
print(update_extensions(["doctor_visit.doc", "doc_holiday.doc"]))
# Extra tests where the old code fails
tests = ["notes.docx", "my.docs.doc", "doc", "photo.png"]
print(update_extensions_bad(tests))
print(update_extensions(tests))
