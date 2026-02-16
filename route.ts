import { NextRequest } from "next/server";
import OpenAI from "openai";
import { getMCPClient, callMCPTool } from "@/lib/mcp";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_API_BASE,
});

export async function POST(req: NextRequest) {
  const { messages } = await req.json();

  const { tools } = await getMCPClient();

  const toolSchemas = tools.map((tool) => ({
    type: "function" as const,
    function: {
      name: tool.name,
      description: tool.description,
      parameters: tool.inputSchema,
    },
  }));

  let currentMessages = [...messages];
  let finalResponse = "";

  // Tool-calling loop (handles multiple rounds)
  while (true) {
    const response = await openai.chat.completions.create({
      model: process.env.OPENAI_MODEL!,
      messages: currentMessages,
      tools: toolSchemas,
      tool_choice: "auto",
      temperature: 0.7,
    });

    const message = response.choices[0].message;
    currentMessages.push(message);

    if (!message.tool_calls || message.tool_calls.length === 0) {
      finalResponse = message.content || "No response.";
      break;
    }

    // Execute all tool calls
    for (const toolCall of message.tool_calls) {
      const toolName = toolCall.function.name;
      const toolArgs = JSON.parse(toolCall.function.arguments);

      try {
        const result = await callMCPTool(toolName, toolArgs);

        currentMessages.push({
          role: "tool",
          tool_call_id: toolCall.id,
          content: JSON.stringify(result.content),
        });
      } catch (err: any) {
        currentMessages.push({
          role: "tool",
          tool_call_id: toolCall.id,
          content: `Error: ${err.message}`,
        });
      }
    }
  }

  return Response.json({ content: finalResponse });
}