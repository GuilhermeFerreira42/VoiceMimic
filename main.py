from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import Literal
from TTS.api import TTS 

import numpy as np
import soundfile as sf
import torch
import io
import tempfile
import os  # Adicionado para lidar com a exclusão do arquivo temporário

app = FastAPI()

@app.post("/create-audio")
def create_audio(
    text: str, 
    # Linguagem padrão definida como "pt" (Português)
    language: Literal["en", "pt", "es"] = "pt", 
    voice_to_be_cloned: UploadFile = File()
):
    """
    Endpoint para criar um áudio Text-to-Speech com clonagem de voz.
    - text: O texto a ser convertido em áudio.
    - language: A linguagem do texto ("en", "pt", ou "es").
    - voice_to_be_cloned: O arquivo de áudio da voz base para clonagem.
    """
    
    # 1. Obter dispositivo (GPU ou CPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 2. Inicializar o modelo TTS
    # O modelo usado no vídeo é 'tts_models/multilingual/multi-dataset/your_tts'
    tts = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)

    # 3. Criar e preencher um arquivo temporário com a voz para ser clonada
    # No Windows, precisamos fechar explicitamente o arquivo temporário para que o TTS possa acessá-lo
    # O bloco 'with' original causava problema de permissão no Windows
    temp_clone_voice = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        # Ler o conteúdo do arquivo enviado e escrever no arquivo temporário
        temp_clone_voice.write(voice_to_be_cloned.file.read())
        # Obter o caminho completo do arquivo temporário
        temp_clone_voice_path = temp_clone_voice.name
        # Fechar explicitamente o arquivo para liberar o bloqueio no Windows
        temp_clone_voice.close()

        # 4. Mapear "pt" para "pt-br" (compatibilidade com o modelo your_tts)
        tts_language = "pt-br" if language == "pt" else language

        # 5. Converter texto para áudio usando a voz clonada
        audio = tts.tts(
            text=text,
            speaker_wav=temp_clone_voice_path,
            language=tts_language
        )
    finally:
        # Garantir que o arquivo temporário seja excluído no final
        # Mesmo se ocorrer um erro durante o processamento
        try:
            os.unlink(temp_clone_voice_path)
        except:
            pass
    
    # 6. Converter a saída da IA (lista de floats) para um array numpy
    audio_array = np.array(audio, dtype=np.float32)
    
    # 7. Criar um stream binário em memória (sem salvar no disco)
    audio_stream = io.BytesIO()
    
    # 8. Escrever o array de áudio no stream, formatando como WAV
    sf.write(audio_stream, audio_array, samplerate=22050, format='WAV')
    
    # 9. Resetar o ponteiro do stream para o início (necessário para a leitura do StreamingResponse)
    audio_stream.seek(0)

    # 10. Retornar o áudio como uma resposta de streaming
    return StreamingResponse(
        audio_stream,
        media_type="audio/wav",
        headers={
            # Garante que o arquivo seja baixado com o nome "output.wav"
            "Content-Disposition": 'attachment; filename="output.wav"'
        }
    )