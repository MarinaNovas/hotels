import shutil

from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.tasks.tasks import resize_image, resize_imag_2

router = APIRouter(prefix='/images', tags=['Изображения отелей'])


@router.post('')
def upload_image(file: UploadFile):
    image_path = f'src/static/images/{file.filename}'
    with open(f'src/static/images/{file.filename}', 'wb+') as new_file:
        shutil.copyfileobj(file.file, new_file)
    resize_image.delay(image_path)


@router.post('/image')
def upload_image_2(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f'src/static/images/{file.filename}'
    with open(f'src/static/images/{file.filename}', 'wb+') as new_file:
        shutil.copyfileobj(file.file, new_file)
    background_tasks.add_task(resize_imag_2, image_path)
