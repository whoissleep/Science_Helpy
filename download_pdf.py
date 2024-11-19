import os 
import requests

def download_all_papers():
    """
    Download all papers from file `papers.txt` to directory `pdfs/`

    The file `papers.txt` should contain a list of links to PDFs,
    one link per line. The links should be direct links to PDFs,
    without any redirects.

    The function will download all PDFs from `papers.txt` to `pdfs/`
    directory. If the PDF is already downloaded, it will be skipped.
    """
    with open("/home/whoissleep/Документы/VS_CODE/proj/papers.txt", "r") as f:
        file = [line.strip() for line in f]
    print(file)


    for i, name_of_pdf in enumerate(file):
        path = f"/home/whoissleep/Документы/VS_CODE/proj/pdfs/{i + 1}.pdf"

        if not os.path.exists(path):
            print(f"[INFO] We don't have this file, downloading...")
            
            url = name_of_pdf
            filename = path
            
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(response.content)
                    print(f"File downloaded in path {filename} as {i + 1}")
            else:
                print(f"Can't download. Status code: {response.status_code}")
                continue
        else:
            print(f"[INFO] File {i} in path: {path} is downloaded!")


###TEST PLACE
###DONT USE THIS CODE IF IT DONT HAVE "DONE AND READY FOR PROD"