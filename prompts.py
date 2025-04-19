from langchain_core.prompts import PromptTemplate

BASE_PROMPT = PromptTemplate.from_template(
"""
Проведи экспертную оценку качества кода, написанного разработчиком с email:  {author_email}
Перед строками с его кодом идет соответствующий комментарий вида //by developer@email.com 
Эти комментарии сгенерированы для разметки кода, не учитывай их при оценке.
            
Код:

{code}

Проведи оценку по следующим критериям:

1. **Читаемость и стиль (0–2):**
   - Является ли стиль кода единообразным и читаемым?
   - Используются ли говорящие имена переменных и функций?
   - Соблюдены ли конвенции языка (например, отступы, оформление)?

2. **Использование паттернов и избегание анти-паттернов (0–2):**
   - Используются ли известные архитектурные паттерны?
   - Присутствуют ли анти-паттерны: дублирование, магические числа, "божественные объекты", длинные функции?

3. **Логика и архитектура (0–2):**
   - Разделена ли ответственность?
   - Следует ли код принципам KISS, DRY, YAGNI?
   - Насколько ясно выражена бизнес-логика?

4. **Надёжность и устойчивость (0–2):**
   - Есть ли проверки входных данных?
   - Обрабатываются ли ошибки?
   - Защищён ли код от типичных сбоев?

5. **Контекстная адекватность (0–2):**
   - Насколько органично код разработчика вписывается в остальной код файла?
   - Следует ли он существующим соглашениям проекта?
   - Переиспользуется ли существующий функционал?

Особые указания:
- Если код хороший, обязательно укажи, что именно в нём хорошо сделано — с примерами и пояснениями.
- Если в коде есть ошибки или недочёты, опиши их чётко и по существу, без лишней воды.
- Избегай общих фраз — давай конкретику.
- Ответ должен содержать только JSON — никаких вводных фраз, комментариев или пояснений вне структуры.

Важно:
- используй не более 500 слов
- пиши только на русском

Ответ предоставь строго в следующем JSON-формате

{{
  "summary": {{
    "total_score": 7.5,
    "max_score": 10
  }},
  "criteria": {{
    "readability_and_style": {{
      "score": 1.5,
      "comment": "Хорошая читаемость, но несоблюдение отступов в одном блоке. Переменные частично неинформативны."
    }},
    "patterns_and_anti_patterns": {{
      "score": 1.0,
      "comment": "Используется паттерн Builder, но присутствует дублирование логики и магические числа."
    }},
    "logic_and_architecture": {{
      "score": 2.0,
      "comment": "Функции чётко структурированы, соблюдены принципы SRP и KISS."
    }},
    "reliability_and_safety": {{
      "score": 1.0,
      "comment": "Есть базовые проверки, но отсутствует полноценная обработка ошибок."
    }},
    "contextual_fit": {{
      "score": 2.0,
      "comment": "Код органично вписан в файл, следует принятым соглашениям, нет дублирования."
    }}
  }}
}}
"""
)
