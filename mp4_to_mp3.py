
from moviepy import AudioFileClip
import uuid

def mp4_to_mp3(mp4, mp3):
    try:
        filetoconvert = AudioFileClip(mp4)
        filetoconvert.write_audiofile(mp3)
        filetoconvert.close()

    except FileNotFoundError:
        print(f"Erro: O arquivo MP4 '{mp4}' não foi encontrado.")

    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {e}")



if __name__ == "__main__":
    mp4_local_filename = "entrevista de Boechat com Jô Soares curto.mp4"
    mp3_local_filename = f"{uuid.uuid4().hex}.mp3"
    
    mp4_to_mp3(mp4_local_filename, mp3_local_filename)
