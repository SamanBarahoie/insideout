import re
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


def load_srt_with_time(file_path):

    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split blocks by double newlines
    blocks = re.split(r"\n\s*\n", content)
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 2:
            # lines[0] is sequence number, lines[1] is timestamp
            timestamp = lines[1]
            m = re.match(r"(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})", timestamp)
            if not m:
                continue
            start_ts = m.group('start')
            # Convert to seconds
            h, m_, s_ms = start_ts.split(':')
            s, ms = s_ms.split(',')
            start_seconds = int(h)*3600 + int(m_)*60 + int(s) + int(ms)/1000.0
            # Remaining lines are text
            text = ' '.join(lines[2:]).strip()
            if text:
                entries.append((start_seconds, text))
    return entries


# لود مدل
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    return_all_scores=True
)


tuples = load_srt_with_time("inside.srt")  # مسیر زیرنویس

# ساخت دیتافریم
rows = []
for start_time, line in tuples:
    scores = classifier(line)[0]
    top = max(scores, key=lambda x: x['score'])
    rows.append({
        'time': start_time,
        'line': line,
        'emotion': top['label'],
        'score': top['score']
    })

df = pd.DataFrame(rows)
df.to_csv('emotion_results_with_time.csv', index=False)
print("Results saved to emotion_results_with_time.csv")
