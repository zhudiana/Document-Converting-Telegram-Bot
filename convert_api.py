import os
from pprint import pprint
from dotenv import load_dotenv
import cloudmersive_convert_api_client
from cloudmersive_convert_api_client.rest import ApiException

load_dotenv()
API_KEY = os.getenv("CLOUDMERSIVE_API_KEY")

# Configure API key authorization: Apikey
configuration = cloudmersive_convert_api_client.Configuration()
configuration.api_key['Apikey'] = API_KEY

# create an instance of the API class
api_instance = cloudmersive_convert_api_client.ConvertDocumentApi(
    cloudmersive_convert_api_client.ApiClient(configuration))

conversion_map = {
    # DOC conversions
    ("doc", "pdf"): api_instance.convert_document_doc_to_pdf,
    ("doc", "docx"): api_instance.convert_document_doc_to_docx,
    ("doc", "txt"): api_instance.convert_document_doc_to_txt,

    # DOCX conversions
    ("docx", "pdf"): api_instance.convert_document_docx_to_pdf,
    ("docx", "txt"): api_instance.convert_document_docx_to_txt,
    ("docx", "doc"): api_instance.convert_document_docx_to_doc,
    ("docx", "html"): api_instance.convert_document_docx_to_html,

    # ODT conversions
    ("odt", "pdf"): api_instance.convert_document_odt_to_pdf,
    ("odt", "docx"): api_instance.convert_document_odt_to_docx,

    # PDF conversions
    ("pdf", "docx"): api_instance.convert_document_pdf_to_docx,
    ("pdf", "pptx"): api_instance.convert_document_pdf_to_pptx,
    ("pdf", "txt"): api_instance.convert_document_pdf_to_txt,

    # PPT conversions
    ("ppt", "pdf"): api_instance.convert_document_ppt_to_pdf,
    ("ppt", "pptx"): api_instance.convert_document_ppt_to_pptx,

    # PPTX conversions
    ("pptx", "pdf"): api_instance.convert_document_pptx_to_pdf,
    ("pptx", "ppt"): api_instance.convert_document_pptx_to_ppt,
    ("pptx", "txt"): api_instance.convert_document_pptx_to_txt,

    # ODP conversions
    ("odp", "pdf"): api_instance.convert_document_odp_to_pdf,
    ("odp", "pptx"): api_instance.convert_document_odp_to_pptx,

    # XLS conversions
    ("xls", "pdf"): api_instance.convert_document_xls_to_pdf,
    ("xls", "xlsx"): api_instance.convert_document_xls_to_xlsx,
    ("xls", "csv"): api_instance.convert_document_xls_to_csv,

    # XLSX conversions
    ("xlsx", "pdf"): api_instance.convert_document_xlsx_to_pdf,
    ("xlsx", "csv"): api_instance.convert_document_xlsx_to_csv,
    ("xlsx", "txt"): api_instance.convert_document_xlsx_to_txt,
    ("xlsx", "xls"): api_instance.convert_document_xlsx_to_xls,
    ("xlsx", "html"): api_instance.convert_document_xlsx_to_html,

    # ODS conversions
    ("ods", "pdf"): api_instance.convert_document_ods_to_pdf,
    ("ods", "xlsx"): api_instance.convert_document_ods_to_xlsx,

    # KEY conversions
    ("key", "pdf"): api_instance.convert_document_keynote_to_pdf,
    ("key", "pptx"): api_instance.convert_document_keynote_to_pptx,
}



def convert_file(file_path: str, source_ext: str, target_ext: str):
    key = (source_ext.lower(), target_ext.lower())
    conversion_func = conversion_map.get(key)

    if not conversion_func:
        print(f"❌ No conversion function for {source_ext} → {target_ext}")
        return None

    try:
        result = conversion_func(file_path)
        return result
    except ApiException as e:
        print(f"❌ Cloudmersive API error: {e}")
        return None
