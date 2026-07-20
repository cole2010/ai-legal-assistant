export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  try {
    const { text, action } = await request.json();

    const prompt = action === "summarize"
      ? `Summarize this legal clause:\n\n${text}`
      : `Explain this legal clause in plain English. Highlight risks:\n\n${text}`;

    const response = await fetch(
      "https://api-inference.huggingface.co/models/gpt2",
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          inputs: prompt,
          parameters: {
            max_new_tokens: 100,
            temperature: 0.7,
            return_full_text: false
          }
        })
      }
    );

    if (!response.ok) {
      const error = await response.json();
      return new Response(JSON.stringify({ error: error.error || "API error" }), {
        status: response.status,
        headers: { "Content-Type": "application/json" }
      });
    }

    const data = await response.json();
    const result = data[0]?.generated_text || "No response.";

    return new Response(JSON.stringify({ result }), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
