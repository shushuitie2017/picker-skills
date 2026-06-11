# tts-providers/gptsovits.sh — local GPT-SoVITS (api_v2.py) provider.
#
# High-quality zero-shot voice cloning, supports zh / en / ja. Requires a
# running GPT-SoVITS API and a REFERENCE voice clip (3–10s) + its transcript.
#
# Start the API first (on the GPT-SoVITS machine):
#   D:\GPT-SoVITS\start_api.bat        # api_v2.py on 127.0.0.1:9880
#
# Configure via env (the runner passes text + out_path; lang from PRESENTATION_LANG):
#   GSV_API        API base       (default http://127.0.0.1:9880)
#   GSV_REF_AUDIO  reference wav   (required, absolute path)
#   GSV_PROMPT_TEXT transcript of the reference clip (required)
#   GSV_PROMPT_LANG language of the reference clip   (default zh)
#   GSV_SPLIT      text_split_method (default cut0 — whole-sentence, smoothest)
#   PRESENTATION_LANG  zh | en | ja  → text_lang (default zh)
#
# Quality recipe (see references/GUJI-USE-CASES.md §7): v4 model + cut0 +
# speed 1.0 + one consistent reference. Switch to v4 once via:
#   curl "$GSV_API/set_gpt_weights?weights_path=GPT_SoVITS/pretrained_models/s1v3.ckpt"
#   curl "$GSV_API/set_sovits_weights?weights_path=GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth"
#
# NOTE: on Windows/Git Bash this project's `jq`/`ffmpeg`-on-PATH are flaky, so
# the sanen book drives synthesis with a pure-Python script (audiobooks/<id>/synth.py)
# instead of synthesize-audio.sh. This provider is the bash-runner equivalent.

GSV_API="${GSV_API:-http://127.0.0.1:9880}"
GSV_PROMPT_LANG="${GSV_PROMPT_LANG:-zh}"
GSV_SPLIT="${GSV_SPLIT:-cut0}"

_gsv_text_lang() {
  case "${PRESENTATION_LANG:-zh}" in
    en) echo "en" ;; ja) echo "ja" ;; *) echo "zh" ;;
  esac
}

tts_check() {
  command -v curl >/dev/null || { echo "✗ curl required" >&2; return 1; }
  command -v ffmpeg >/dev/null || { echo "✗ ffmpeg required (wav→mp3)" >&2; return 1; }
  [[ -n "${GSV_REF_AUDIO:-}" && -f "${GSV_REF_AUDIO:-/nonexistent}" ]] || { echo "✗ GSV_REF_AUDIO not set/missing" >&2; return 1; }
  [[ -n "${GSV_PROMPT_TEXT:-}" ]] || { echo "✗ GSV_PROMPT_TEXT (reference transcript) not set" >&2; return 1; }
  curl -s -o /dev/null --max-time 5 "$GSV_API/docs" 2>/dev/null || curl -s -o /dev/null --max-time 5 "$GSV_API/" 2>/dev/null \
    || { echo "✗ GPT-SoVITS API not reachable at $GSV_API (start start_api.bat)" >&2; return 1; }
  return 0
}

tts_install_help() {
  cat >&2 <<'EOF'
GPT-SoVITS provider setup:
  1) Start the API:   D:\GPT-SoVITS\start_api.bat   (api_v2.py @ 127.0.0.1:9880)
  2) Reference voice (3–10s clean single speaker) + transcript:
       export GSV_REF_AUDIO="/d/voices/narrator_zh.wav"
       export GSV_PROMPT_TEXT="参考音频里念的那句话"   GSV_PROMPT_LANG=zh
  3) export PRESENTATION_LANG=zh   # or en / ja
  4) PRESENTATION_TTS=gptsovits npm run synthesize-audio
EOF
}

# tts_synthesize <text> <out_path.mp3> [voice(unused)]
tts_synthesize() {
  local text="$1" out="$2" text_lang; text_lang="$(_gsv_text_lang)"
  local tmp_wav="${out%.mp3}.tmp.wav"
  local payload
  payload=$(jq -n --arg text "$text" --arg tl "$text_lang" \
    --arg ref "$GSV_REF_AUDIO" --arg pt "$GSV_PROMPT_TEXT" --arg pl "$GSV_PROMPT_LANG" --arg sp "$GSV_SPLIT" \
    '{text:$text, text_lang:$tl, ref_audio_path:$ref, prompt_text:$pt, prompt_lang:$pl,
      text_split_method:$sp, batch_size:1, media_type:"wav", streaming_mode:false, speed_factor:1.0}')
  local code
  code=$(curl -s -o "$tmp_wav" -w "%{http_code}" --max-time 300 \
    -X POST "$GSV_API/tts" -H "Content-Type: application/json" -d "$payload")
  if [[ "$code" != "200" ]]; then
    echo "    GPT-SoVITS API error (http $code): $(head -c 300 "$tmp_wav" 2>/dev/null)" >&2
    rm -f "$tmp_wav"; return 1
  fi
  # encode + trim head/tail silence (gapless transitions)
  ffmpeg -y -loglevel error -i "$tmp_wav" \
    -af "silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB,areverse" \
    -codec:a libmp3lame -q:a 3 "$out" </dev/null
  local rc=$?; rm -f "$tmp_wav"; return $rc
}
