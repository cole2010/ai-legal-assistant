export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const { text, action } = await request.json();

    if (!text || typeof text !== "string") {
      return new Response(JSON.stringify({ error: "Missing or invalid 'text' field" }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    if (!env.HF_TOKEN) {
      return new Response(JSON.stringify({ error: "HF_TOKEN not set in environment variables" }), {
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Use a larger, more capable model
    const MODEL = "gpt2-large";
    const prompt = action === "summarize"
      ? `Summarize this legal clause:\n\n${text}`
      : `Explain this legal clause in plain English. Highlight risks:\n\n${text}`;

    const response = await fetch(
      `https://api-inference.huggingface.co/models/${MODEL}`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          inputs: prompt,
          parameters: {
            max_new_tokens: 120,
            temperature: 0.7,
            return_full_text: false
          }
        })
      }
    );

    if (!response.ok) {
      let errorMsg;
      try {
        const errorData = await response.json();
        errorMsg = errorData.error || "HF API error";
      } catch {
        errorMsg = `HF API error (status ${response.status})`;
      }
      return new Response(JSON.stringify({ error: errorMsg }), {
        status: response.status,
        headers: { "Content-Type": "application/json" }
      });
    }

    let data;
    try {
      data = await response.json();
    } catch {
      return new Response(JSON.stringify({ error: "Invalid response from HF API" }), {
        status: 502,
        headers: { "Content-Type": "application/json" }
      });
    }

    const result = data[0]?.generated_text || "No response.";
    return new Response(JSON.stringify({ result }), {
      headers: { "Content-Type": "application/json" }
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message || "Internal server error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
