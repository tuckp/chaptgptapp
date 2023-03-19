// Replace YOUR_API_KEY with your OpenAI API key
const apiKey = '';
const apiUrl = 'https://api.openai.com/v1/engines/davinci-codex/completions';

async function generateAnswer() {
  const question = document.getElementById('question').value;
  const prompt = `Q: ${question}\nA:`;

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        'prompt': prompt,
        'max_tokens': 100,
        'temperature': 0.7,
        'stop': ['\n']
      })
    });
    const data = await response.json();
    const answer = data.choices[0].text.trim();
    document.getElementById('answer').textContent = answer;
  } catch (error) {
    console.error(error);
  }
}
