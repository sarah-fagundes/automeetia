
import assemblyai as aai


def mp3_to_text(aai, filename, s_labels, s_expected, l_code):
    try:
        config = aai.TranscriptionConfig(
            speaker_labels=s_labels,  # Define se os rótulos dos falantes devem ser incluídos.
            speakers_expected=s_expected,  # Número esperado de falantes no áudio.
            language_code=l_code  # Define o código de idioma, como 'pt' para português.
        )

        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe(
            filename,
            config=config
        )

        return transcript

    except FileNotFoundError:
        print("Erro: o arquivo especificado não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")



if __name__ == "__main__":
    # chave da openia
    aai.settings.api_key = ""
    mp3_local_filename = "bf8ba8be1835427c8fcab928dc9c2a79.mp3"

    transcript = mp3_to_text(
        aai, 
        filename=mp3_local_filename, 
        s_labels=True,  # Habilita os rótulos dos falantes no resultado da transcrição.
        s_expected=2,   # Espera que o áudio contenha 2 falantes.
        l_code='pt'     # Define o idioma do áudio como português.
    )

    if transcript:
        for utterance in transcript.utterances:
            print(f"Speaker {utterance.speaker}: {utterance.text}")



