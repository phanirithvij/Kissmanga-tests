import requests
import os


def download_img(url, outdir = "Downloads/", Manga_Name = "No_Name", Chapter_Name = "No_Name"):
    """

    Downloads Manga Image in the given outdir/Manga_Name/Chapter_Name/ directory

    """
    r = requests.get(url)
    file_path = os.path.join(outdir, Manga_Name, Chapter_Name)


    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    downloadheaders =  requests.head(url)
    header = downloadheaders.headers
    #print(header["filename"])
    print(header)

    file_path += "/file_name"

    #with open(file_path, "wb+") as f:
    #    f.write(r.content)
    print(file_path)

if __name__ == "__main__":

    url = "https://2.bp.blogspot.com/-4OvyILJGlgU/WwpuHuEOJjI/AAAAAAAHHQw/5cULwAW6R30Abvk4zNwphOQSNxUVe9MPACHMYCw/s0/000.jpeg"

    Manga_Name = "Some_Manga"
    Chapter_Name = "Some_Chapter"

    download_img(url, outdir="Downloads", Manga_Name=Manga_Name, Chapter_Name=Chapter_Name)