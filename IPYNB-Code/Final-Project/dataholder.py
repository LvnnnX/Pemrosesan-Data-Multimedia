from library import Path, BASE, Image, IMGDIR, os,TMPDIR

def get_images(name) -> Image:
    image = Image.open(f'{IMGDIR}/{name}.jpg')
    return image