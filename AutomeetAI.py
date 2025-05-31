import streamlit as st
import uuid
import assemblyai as aai
from openai import OpenAI

from mp4_to_mp3 import mp4_to_mp3
from mp3_to_text import mp3_to_text
from chat_com_openai import generate_response

from annotated_text import annotated_text


aai_api_key = st.secrets["assemblyai"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]


language_codes = {
	"Portuguese": "pt",		  # Key: Portuguese, Value: 'pt'
	"Global English": "en",	  # Key: Global English, Value: 'en'
	"Australian English": "en_au", # Key: Australian English, Value: 'en_au'
	"British English": "en_uk",  # Key: British English, Value: 'en_uk'
	"Spanish": "es",			 # Key: Spanish, Value: 'es'
	"US English": "en_us",	   # Key: US English, Value: 'en_us'
	"French": "fr",			  # Key: French, Value: 'fr'
	"German": "de",			  # Key: German, Value: 'de'
	"Italian": "it",			 # Key: Italian, Value: 'it'
	"Dutch": "nl",			   # Key: Dutch, Value: 'nl'
	"Hindi": "hi",			   # Key: Hindi, Value: 'hi'
	"Japanese": "ja",			# Key: Japanese, Value: 'ja'
	"Chinese": "zh",			 # Key: Chinese, Value: 'zh'
	"Finnish": "fi",			 # Key: Finnish, Value: 'fi'
	"Korean": "ko",			  # Key: Korean, Value: 'ko'
	"Polish": "pl",			  # Key: Polish, Value: 'pl'
	"Russian": "ru",			 # Key: Russian, Value: 'ru'
	"Turkish": "tr",			 # Key: Turkish, Value: 'tr'
	"Ukrainian": "uk",		   # Key: Ukrainian, Value: 'uk'
	"Vietnamese": "vi"		   # Key: Vietnamese, Value: 'vi'
}




st.title('🤖 AutomeetAI')

prompt_system = st.text_area("Forneça instruções gerais ou estabeleça o tom para o \"assistente\" de IA:", "Você é um ótimo gerente de projetos com grandes capacidades de criação de atas de reunião.")

prompt_text = st.text_area("O que o usuário deseja que o assistente faça?", """Em uma redação de nível especializado, resuma as notas da reunião em um único parágrafo.
Em seguida, escreva uma lista de cada um de seus pontos-chaves tratados na reunião.
Por fim, liste as próximas etapas ou itens de ação sugeridos pelos palestrantes, se houver.""")

st.divider()


col21, col22 = st.columns(2)


with col21:
	speakers_expected = st.number_input("Total de pessoas falantes:", 1, 15)

with col22:
	language = st.selectbox("Selecione o idioma falado:", tuple(language_codes.keys()))


uploaded_file = st.file_uploader("Selecione o seu arquivo", accept_multiple_files=False, type=['mp4'])


st.divider()




if uploaded_file:

	with st.spinner('Convertendo de mp4 para mp3...'):
		mp4_filename = uploaded_file.name
		mp3_filename = '{nome_arquivo}.mp3'.format(nome_arquivo=uuid.uuid4().hex)

		tempfile = open(mp4_filename, 'wb')
		tempfile.write(uploaded_file.read())

		mp4_to_mp3(mp4_filename, mp3_filename)

	st.success("Conversão de MP4 para MP3 realizada!")



	with st.spinner('Convertendo de mp3 para texto...'):

		aai.settings.api_key = aai_api_key

		transcript = mp3_to_text(
			aai, 
			filename=mp3_filename,
			s_labels=True,  # Ativa os rótulos para falantes.
			s_expected=speakers_expected,
			l_code=language_codes[language]
		)

		st.success("Transcrição de áudio para texto realizada!")

		texto_transcrito = ''
		texto_anotado = []

		if transcript:
			for utterance in transcript.utterances:
				texto_transcrito += f"Speaker {utterance.speaker}: {utterance.text}"
				texto_transcrito += '\n'

				texto_anotado.append((utterance.text, f"Speaker {utterance.speaker}"))




	with st.spinner('Gerando ata de reunião...'):

		client = OpenAI(api_key=openai_api_key)

		prompt_text += '\n===========\n'
		prompt_text += texto_transcrito

		texto_retorno = generate_response(client, prompt_system, prompt_text)

		st.success("Ata gerada com sucesso!")


	st.subheader('Transcrição original')

	annotated_text(texto_anotado)

	st.subheader('Ata gerada')
	st.markdown(texto_retorno)

	# deletar_arquivo_se_existir(mp3_filename)
