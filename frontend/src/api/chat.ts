
export interface ChatSource {
  page_number: number;
  text: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
  sources: ChatSource[];
}

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function askQuestion(
  documentId: string,
  question: string,
  topK: number = 5,
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document_id: documentId,
      question,
      top_k: topK,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Unable to answer your question.",
    );
  }

  return data as ChatResponse;
}
