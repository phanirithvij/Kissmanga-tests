import requests
import os, json, sys

from reportlab.pdfgen import canvas
from PIL import Image


def write_json(data, dir_name, file_name):
    """
    Write a json file by giving data, path(dir_name) and file_name
    """
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    with open(os.path.join(dir_name, '%s.json' % file_name), 'w') as f:
        f.write(json.dumps(data, indent=2))


def create_pdf(images, dir_name, file_name):
    """
    Creates a pdf from given images list and saves at dir_name/file_name.pdf
    """
    c = canvas.Canvas(os.path.join(dir_name, file_name) + '.pdf')
    c.setTitle(file_name)
    for imgPath in images:
        with Image.open(imgPath) as loadedImage:
            w, h = loadedImage.size
        c.setPageSize((w, h))
        c.drawImage(imgPath, x = 0, y = 0)
        c.showPage()
    c.save()


def download_images_and_create_pdf(images, dir_name, file_name):
    """
    Downloads images and creates a pdf from the downloaded_images
    """

    if os.path.exists(os.path.join(dir_name, file_name+'.pdf')):
        print(('Already exists: ', os.path.join(dir_name, file_name+'.pdf')))
        return

    try:
        new_img_list = []
        for image_url in images:
            img_name = image_url.split("/")[-1]

            if not os.path.exists(os.path.join(dir_name, img_name)):
                print(('downloading image: ', image_url))
                img_data = requests.get(image_url).content
                with open(os.path.join(dir_name, img_name), 'wb+') as f:
                    f.write(img_data)

            new_img_list.append(
                os.path.abspath(os.path.join(dir_name, img_name))
            )
        create_pdf(
            images=new_img_list,
            dir_name=dir_name,
            file_name=file_name
        )
        print(('Success: ', os.path.join(dir_name, file_name)))
        return True
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
    return False


if __name__ == "__main__":
    pass