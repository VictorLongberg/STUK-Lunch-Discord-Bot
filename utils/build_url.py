import datetime

# Builds the download url.
def build_url(base_url, restaurant, pdf_type, pdf):
    now = datetime.datetime.now()
    week = now.strftime("%U")
    year = now.year
    dynamic_url = f"&pdf={pdf}&pdfType={pdf_type}&restaurant={restaurant}&week={week}&year={year}"
    return base_url + dynamic_url
