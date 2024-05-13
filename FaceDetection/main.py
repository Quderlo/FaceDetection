import asyncio

from camera import Camera
import cv2
from datetime import datetime
import project_settings as p_settings
from telegram_bot import Telegram_bot


async def send_data(image, descriptor):
    result, message, photo = telegram_bot.check_data(descriptor, image)
    if result is not None:
        await telegram_bot.send_data(image, photo, message)


async def main():
    if p_settings.rtsp:
        cam = Camera(p_settings.rtsp_path)
    else:
        cam = Camera(0)
    cv2.waitKey(2000)

    while True:
        image = cam.getFrame()  # Последний кадр

        if image is not None:

            if p_settings.rtsp:
                x = 1200  # обрезать слева
                y = 400  # обрезать сверху
                width = image.shape[1] - x
                height = image.shape[0] - y
                image = image[y:y + height, x:x + width]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            try:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            except cv2.error as cv2e:
                print(f"cv2 error in gray. {cv2e}")
                continue

            faces = p_settings.face_detector(gray)

            for i, face in enumerate(faces):
                landmarks = p_settings.shape_predictor(gray, face)
                face_descriptor = p_settings.face_recognizer.compute_face_descriptor(image, landmarks)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # для отправки данных в Telegram
                await send_data(image, face_descriptor)

            if p_settings.rtsp:
                cv2.putText(image, datetime.now().strftime('%H:%M:%S'), (image.shape[0], 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)
            else:
                cv2.putText(image, datetime.now().strftime('%H:%M:%S'), (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)

            cv2.imshow("rtsp", image)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    telegram_bot = Telegram_bot()
    asyncio.run(main())
