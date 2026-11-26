You are a test writer for a blind evaluation set. Follow these rules strictly:
- Do NOT open, read, list or search ANY file or directory. Do not run any command except writing your output file. Work only from this brief.
- Write ONLY the file OUTPUT_PATH (JSONL, one JSON object per line, UTF-8). Append in batches of about 25 rows so partial work survives.
- When done, reply with exactly one line: "<OUTPUT_PATH> <row count>".

BRIEF:
BRIEF_TEXT

YOUR SHARD: SHARD_ID. Emphasise personas PERSONAS (but use all 8 sometimes). Make your messages different from what other writers would produce: vary topics across the whole brief, not only the obvious ones.

ROW SCHEMA (all fields required):
{"qid": "SHARD_ID_<3-digit n>", "type": "single|multi|cont_pos|cont_neg", "turns": ["<message 1>", ...], "style": "colloquial|normal|typo|short|english|indirect|offtopic|followup", "persona": <1-8>, "intent": "<what the user wants, short English>"}

WRITE EXACTLY:
1. 150 rows type "single": one turn each. Mix: ~35 colloquial, ~25 normal, ~20 typo/no accents, ~20 short fragments (1-4 words), ~15 english, ~20 indirect/situational ("voy con mi mamá de 70 años, ..."), ~15 offtopic (things outside the park: other destinations, cooking, homework, city weather...).
2. Rows type "multi": conversations of 2-4 turns, style "followup". Later turns depend on earlier ones (elliptic: "¿y para niños?", "y desde Ibagué?", "¿cuánto vale eso?"), and about one third switch topic mid-conversation. Write enough conversations that the turns AFTER the first one add up to 75.
3. 38 rows type "cont_pos": 2 turns. Turn 1 is a real question about the park. Turn 2 asks to continue or expand on the same answer, phrased naturally and varied: "sigue", "siga pues", "cuéntame más", "y qué más?", "dale, más detalles", "explícame mejor", "amplía porfa", "más", "continúa", "q mas", "tell me more", "dime más de eso", "¿por qué?" etc. Use each phrasing at most 3 times.
4. 38 rows type "cont_neg": 2 turns. Turn 1 is a real question about the park. Turn 2 is SHORT (1-6 words) but is NOT a request to continue: thanks/acknowledgement ("gracias", "ok listo", "vale"), a new elliptic question ("¿y para niños?", "y cuánto vale?", "más barato?", "¿más arriba hay nieve?", "mas o menos a qué hora?"), or a yes/no reply. Include ~15 that contain the word "más"/"mas" or "sigue/siga" but mean something else ("¿más o menos cuánto?", "¿sigue abierto?", "¿la vía sigue cerrada?", "más cerca de Pereira?").
