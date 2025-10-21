# --- INÍCIO DA CONFIGURAÇÃO CRÍTICA ---
import os
import sys

# Configurar variáveis de ambiente ANTES de importar torch
os.environ["TORCH_FORCE_WEIGHTS_ONLY_LOAD"] = "0"
os.environ["TORCH_WEIGHTS_ONLY_LOAD"] = "0"

# Importar torch
import torch
torch.serialization.DEFAULT_WEIGHTS_ONLY = False

# Monkey-patching para forçar weights_only=False
_original_torch_load = torch.load
def _safe_torch_load(f, *args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(f, *args, **kwargs)
torch.load = _safe_torch_load

# --- FIM DA CONFIGURAÇÃO CRÍTICA ---

# Restante das importações
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import Literal
import numpy as np
import soundfile as sf
import io
import tempfile
import os
import re
from num2words import num2words
import librosa

app = FastAPI()

def clean_text(text):
    text = re.sub(r'(\d+)', lambda m: num2words(m.group(1), lang='pt_BR'), text)
    text = text.replace('—', '-').replace('–', '-').replace('“', '"').replace('”', '"')
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    return text

@app.post("/create-audio")
def create_audio(
    text: str, 
    language: Literal["en", "pt", "es"] = "pt", 
    voice_to_be_cloned: UploadFile = File(...)
):
    from TTS.api import TTS
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(device)
    
    temp_clone_voice = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        temp_clone_voice.write(voice_to_be_cloned.file.read())
        temp_clone_voice_path = temp_clone_voice.name
        temp_clone_voice.close()
        
        data, samplerate = sf.read(temp_clone_voice_path)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        if samplerate != 16000:
            data = librosa.resample(data, orig_sr=samplerate, target_sr=16000)
            samplerate = 16000
        sf.write(temp_clone_voice_path, data, samplerate, 'PCM_16')
        
        cleaned_text = clean_text(text)
        lang_id = "pt" if language == "pt" else language
        
        output_path = tempfile.mktemp(suffix=".wav")
        tts.tts_to_file(
            text=cleaned_text,
            speaker_wav=temp_clone_voice_path,
            language=lang_id,
            file_path=output_path
        )
        
        with open(output_path, "rb") as f:
            audio_array = f.read()
        os.unlink(output_path)
        
    finally:
        try:
            os.unlink(temp_clone_voice_path)
        except:
            pass
    
    return StreamingResponse(
        io.BytesIO(audio_array),
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'attachment; filename="output.wav"'
        }
    )