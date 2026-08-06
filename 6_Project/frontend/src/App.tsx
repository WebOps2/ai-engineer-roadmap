import { useState, type FormEvent } from "react";

type Source = {
  dataset: string;
  row: number | null;
};

type ChatResponse = {
  answer: string;
};

const API_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/v1";

function App() {
  const [question, setQuestion] = useState("");
  const [askedQuestion, setAskedQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const submittedQuestion = question.trim();
    if (!submittedQuestion || loading) return;

    setAskedQuestion(submittedQuestion);
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: submittedQuestion }),
      });

      if (!response.ok) {
        const body = (await response.json().catch(() => null)) as {
          detail?: string;
        } | null;
        throw new Error(body?.detail ?? "The request could not be completed.");
      }

      const data = (await response.json()) as ChatResponse;
      setAnswer(data.answer);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The backend could not be reached.",
      );
    } finally {
      setLoading(false);
    }
  }

  const hasResponse = loading || Boolean(answer) || Boolean(error);

  return (
    <main className="page">
      <section className={`chat-start ${hasResponse ? "has-response" : ""}`}>
        <p className="eyebrow">Premier League AI</p>
        <h1>What would you like to know?</h1>

        <form className="chat-box" onSubmit={handleSubmit}>
          <div className="ball-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="9" />
              <path d="m12 7 3 2.2-1.1 3.5h-3.8L9 9.2 12 7Z" />
              <path d="m12 3 .1 4M3.8 9l5.2.2M6.6 19l3.5-6.3M17.4 19l-3.5-6.3M20.2 9 15 9.2" />
            </svg>
          </div>

          <input
            aria-label="Ask a Premier League question"
            disabled={loading}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask anything about the Premier League"
            value={question}
          />

          <button
            aria-label="Send question"
            disabled={!question.trim() || loading}
            type="submit"
          >
            {loading ? (
              <span className="spinner" />
            ) : (
              <svg aria-hidden="true" viewBox="0 0 24 24">
                <path d="m22 2-7 20-4-9-9-4Z" />
                <path d="m22 2-11 11" />
              </svg>
            )}
          </button>
        </form>

        {hasResponse && (
          <div className="response-panel" aria-live="polite">
            <div className="question-row">
              <span>You</span>
              <p>{askedQuestion}</p>
            </div>

            {loading && (
              <div className="answer-row loading-row">
                <span>AI</span>
                <p>Searching the Premier League dataset…</p>
              </div>
            )}

            {error && (
              <div className="answer-row error-row">
                <span>AI</span>
                <p>{error}</p>
              </div>
            )}

            {answer && (
              <div className="answer-row">
                <span>AI</span>
                <div>
                  <p>{answer}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
