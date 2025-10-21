# VoiceMimic - Sistema de Clonagem de Voz com IA

![VoiceMimic Logo](https://via.placeholder.com/150/92c952?text=VM) *Logo ilustrativo - substitua por uma imagem real*

## 📌 Visão Geral

VoiceMimic é um sistema de clonagem de voz baseado em IA que permite transformar texto em áudio usando uma voz de referência como base. O objetivo principal é permitir que usuários não técnicos possam clonar vozes com um sistema simples de "clicar e funcionar", executado localmente no Windows sem necessidade de conhecimento avançado de terminal.

O projeto foi especificamente desenvolvido para clonar a voz do Rick Sanchez (dublador brasileiro) com a maior fidelidade possível, alcançando atualmente cerca de 70% de similaridade com a voz original.

## 🚀 Recursos Principais

- **Interface Web Amigável**: Documentação automática com Swagger UI para testes rápidos
- **Clonagem de Voz de Alta Qualidade**: Utiliza o modelo XTTS v2 da biblioteca TTS
- **Suporte a Múltiplos Idiomas**: Incluindo português brasileiro, inglês e espanhol
- **Pré-processamento Inteligente**: 
  - Conversão de números para palavras
  - Limpeza de caracteres problemáticos
  - Padronização de áudio para 16kHz mono
- **Execução Local**: Funciona inteiramente no seu computador, sem necessidade de internet após a configuração inicial

## ⚠️ Status Atual

O sistema está funcionando com as seguintes características:

- **Qualidade da Voz**: ~70% de fidelidade com a voz do Rick Sanchez
- **Problemas Conhecidos**:
  - Entonação não totalmente característica do Rick Sanchez
  - Pausas inadequadas após pontuação (lê pontos como "ponto, ponto")
  - Falta de naturalidade nas transições entre frases
- **Pontos Positivos**:
  - Sistema estável após correções de compatibilidade com Windows
  - Interface web funcional e fácil de usar
  - Processamento adequado do áudio de referência

## 🛠️ Requisitos do Sistema

- Windows 10 ou superior
- Python 3.10+
- GPU NVIDIA recomendada (mas funciona em CPU)
- ~10GB de espaço livre (para modelos de IA)

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/VoiceMimic.git
   cd VoiceMimic
   ```

2. Execute o arquivo `start.bat` para configurar e iniciar o sistema automaticamente

## 🖥️ Utilização

1. Após executar `start.bat`, o sistema iniciará automaticamente
2. Acesse a interface web em: http://127.0.0.1:8085/docs
3. Use o endpoint `/create-audio` para clonar vozes:
   - Envie seu texto no campo `text`
   - Selecione o idioma (`pt` para português brasileiro)
   - Envie um arquivo WAV de referência com a voz que deseja clonar

### Dicas para Melhor Qualidade

- Use um arquivo WAV de **20-30 segundos** de áudio de referência
- Certifique-se de que o áudio está em **16kHz, mono**
- Inclua frases que capturem a entonação característica do Rick Sanchez:
  - "Wubba lubba dub dub"
  - "I'm Pickle Rick"
  - "Riiiiick!"
  - "That's right, Morty, I turned myself into a pickle"
- Evite ruído de fundo no áudio de referência

## ⚙️ Arquitetura Técnica

O sistema é composto por:

- **main.py**: Lógica principal do sistema com:
  - Configuração crítica do PyTorch para resolver problemas de compatibilidade
  - Pré-processamento avançado de texto e áudio
  - Endpoint para criação de áudio clonado
- **requirements.txt**: Dependências específicas do projeto
- **start.bat**: Script de inicialização para Windows

### Bibliotecas Principais

| Biblioteca | Versão | Papel no Sistema |
|------------|--------|------------------|
| **Python** | 3.10+ | Ambiente de execução |
| **TTS** | 0.22.0 | Motor de clonagem de voz |
| **torch** | 2.3.0 | Framework de aprendizado de máquina |
| **torchaudio** | 2.3.0 | Processamento de áudio |
| **FastAPI** | 0.119.1 | Interface web e endpoints |
| **soundfile** | 0.12.1 | Processamento de áudio |
| **librosa** | 0.11.0 | Resampling de áudio |
| **num2words** | 0.5.14 | Conversão de números para palavras |
| **transformers** | 4.33.0 | Modelos de linguagem |
| **numpy** | 1.26.4 | Computação numérica |

## 🔧 Solução de Problemas Conhecidos

### Problema: Entonação não característica do Rick Sanchez
**Solução**: Use um áudio de referência mais longo (20-30 segundos) que inclua frases com a entonação característica do Rick Sanchez.

### Problema: Pausas inadequadas após pontuação
**Solução Temporária**: Adicione pausas manualmente no texto usando `[PAUSE=0.5s]` onde deseja uma pausa mais longa.

### Problema: Qualidade da voz não ideal
**Solução**: 
1. Certifique-se de que o áudio de referência está em 16kHz mono
2. Remova ruídos de fundo do áudio de referência
3. Use frases que demonstrem a rouquidão característica da voz do Rick Sanchez

## 🌟 Possíveis Melhorias Futuras

1. **Melhoria na Entonação**:
   - Implementar ajuste automático de parâmetros para vozes masculinas
   - Adicionar reconhecimento de pontuação para pausas mais naturais

2. **Interface de Usuário Aprimorada**:
   - Adicionar pré-visualização do áudio gerado
   - Implementar ajustes de voz em tempo real

3. **Otimizações Técnicas**:
   - Implementar cache de modelos para carregamento mais rápido
   - Adicionar suporte para mais formatos de áudio de entrada

4. **Melhoria na Qualidade**:
   - Adicionar pós-processamento para realçar características vocais masculinas
   - Implementar técnicas de equalização específicas para vozes do Rick Sanchez

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## 📜 Licença

Este projeto está licenciado sob a CPML (Coqui Public Model License) - consulte o arquivo [LICENSE](LICENSE) para detalhes.