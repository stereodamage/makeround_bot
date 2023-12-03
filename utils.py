import ffmpeg


async def roundify(path: str):
    new_path = f"{path.split('.')[0]}_r.mp4"
    wdt, hgt = 0, 0

    video = ffmpeg.input(path)
    audio = video.audio
    probe = ffmpeg.probe(path)

    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']

    if height > width:
        hgt = (height - width) / 2
        size = width
    elif width > height:
        wdt = (width - height) / 2
        size = height
    else:
        size = height

    newvid = ffmpeg.filter(
        ffmpeg.crop(video, wdt, hgt, size, size),
        "scale", 400, -1)
    output = ffmpeg.output(audio, newvid, filename=new_path)
    ffmpeg.run(output)
    return new_path
