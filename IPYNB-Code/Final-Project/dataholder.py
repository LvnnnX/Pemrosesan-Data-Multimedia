from library import Path, BASE, Image, IMGDIR, os,TMPDIR

def get_images(name) -> Image:
    image = Image.open(f'{IMGDIR}/{name}.jpg')
    return image

def save_file(sound_file) -> str:
    with open(os.path.join(TMPDIR, sound_file.name), 'wb') as f:
        f.write(sound_file.getbuffer())
    return sound_file.name

def delfile(path:os.PathLike) -> None:
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))