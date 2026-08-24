# FRIDAY Smart Text-to-Speech

A Python assistant that sends your input to Gemini for a smart response, then
converts that response into an MP3 file with
[gTTS](https://gtts.readthedocs.io/).

## Web UI

Launch the Streamlit interface:

```bash
streamlit run app.py --server.port 3000
```

The web UI provides a dark chat experience, conversation history, speech
language and speed controls, audio playback, and a download button for the
latest `friday.mp3`.

## Run it

Add `GEMINI_API_KEY` to the project's secrets, then run:

```bash
python main.py "What should I focus on today?"
```

FRIDAY prints Gemini's answer and saves it to `friday.mp3`. Both Gemini and
gTTS require an internet connection.

## Examples

Choose a language and output path:

```bash
python main.py \
  --text "Explain this simply: quantum computing" \
  --lang en \
  --output audio/explanation.mp3
```

Read text from a UTF-8 file:

```bash
python main.py --file prompt.txt --lang en --output audio/friday.mp3
```

Use slower speech for language practice:

```bash
python main.py "Help me practice Spanish" --lang es --slow
```

Use `--direct` to skip Gemini and convert input text directly to speech:

```bash
python main.py --direct "Read this exact text aloud" --output exact.mp3
```

Use `python main.py --help` to see all options. Language codes such as `en`,
`es`, `fr`, `hi`, and `ja` are accepted by gTTS; availability depends on
Google's supported languages. Running without an argument starts an
interactive chat. Each response is spoken and saved to `friday.mp3`,
replacing the previous response. Type `exit`, `quit`, or press Ctrl+C to end
the chat.