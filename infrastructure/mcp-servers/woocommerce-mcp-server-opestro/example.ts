import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
const server = new McpServer({
  name: "Weather Service",
  version: "1.0.0",
});

import { z } from "zod";

server.tool(
  "getWeather",
  { city: z.string() },
  async ({ city }) => {
    return {
      content: [
        {
          type: "text",
          text: `The weather in ${city} is sunny!`,
        },
      ],
    };
  },
);


const transport = new StdioServerTransport();
await server.connect(transport);