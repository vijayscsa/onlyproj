import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

let mcpClient: Client | null = null;
let tools: any[] = [];

export async function getMCPClient() {
  if (mcpClient) return { client: mcpClient, tools };

  const transport = new StreamableHTTPClientTransport(
    new URL(process.env.MCP_SERVER_URL!)
  );

  mcpClient = new Client(
    {
      name: "pagerduty-chatbot",
      version: "1.0.0",
    },
    {
      capabilities: {},
    }
  );

  await mcpClient.connect(transport);

  const toolsResp = await mcpClient.listTools();
  tools = toolsResp.tools;

  console.log(`✅ Connected to PagerDuty MCP – ${tools.length} tools loaded`);
  return { client: mcpClient, tools };
}

export async function callMCPTool(name: string, args: any) {
  const { client } = await getMCPClient();
  return await client.callTool(name, args);
}