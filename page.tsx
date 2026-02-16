"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, AlertCircle } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, userMsg],
        }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.content }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "❌ Error connecting to backend or MCP server." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col">
      <div className="border-b border-zinc-800 p-4 flex items-center gap-3">
        <div className="w-9 h-9 bg-orange-600 rounded-xl flex items-center justify-center">
          <span className="text-xl">🚨</span>
        </div>
        <div>
          <h1 className="text-2xl font-bold">PagerDuty MCP Chat</h1>
          <p className="text-zinc-500 text-sm">Local • Secure • Full tool access</p>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-6 space-y-8" style={{ maxHeight: "calc(100vh - 140px)" }}>
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="text-6xl mb-6">🚨</div>
            <h2 className="text-3xl font-semibold mb-2">Ask me anything about PagerDuty</h2>
            <p className="text-zinc-500 max-w-md">
              Create incidents, check on-call, list services, acknowledge alerts… all in natural language.
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-3xl rounded-2xl px-5 py-3 ${
                msg.role === "user"
                  ? "bg-orange-600 text-white"
                  : "bg-zinc-900 border border-zinc-800"
              }`}
            >
              <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-3 text-zinc-500">
            <Loader2 className="w-5 h-5 animate-spin" />
            Thinking + calling PagerDuty tools…
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      <div className="p-6 border-t border-zinc-800 bg-zinc-950">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Create a SEV-1 incident for the database outage..."
            className="flex-1 bg-zinc-900 border border-zinc-700 rounded-2xl px-6 py-4 focus:outline-none focus:border-orange-500 placeholder-zinc-500"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="bg-orange-600 hover:bg-orange-500 disabled:opacity-50 w-14 h-14 rounded-2xl flex items-center justify-center transition-all"
          >
            {isLoading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6" />}
          </button>
        </div>
        <p className="text-center text-zinc-600 text-xs mt-4">
          Runs 100% locally on your MacBook • Your org-approved custom UI
        </p>
      </div>
    </div>
  );
}