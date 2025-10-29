#!/usr/bin/env node

/**
 * Custom MCP Server for Coding Assistant
 * A personal AI coding assistant with file operations, git integration, and code analysis
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,

} from "@modelcontextprotocol/sdk/types.js";
import { exec } from "child_process";
import { promisify } from "util";
import * as fs from "fs/promises";
import * as path from "path";

const execAsync = promisify(exec);

// Configuration
const WORKSPACE_ROOT = process.env.WORKSPACE_ROOT || process.cwd();

// Define available tools
const TOOLS = [
  {
    name: "read_file",
    description: "Read contents of a file in the workspace",
    inputSchema: {
      type: "object",
      properties: {
        filepath: {
          type: "string",
          description: "Path to the file relative to workspace root",
        },
      },
      required: ["filepath"],
    },
  },
  {
    name: "write_file",
    description: "Write or update a file in the workspace",
    inputSchema: {
      type: "object",
      properties: {
        filepath: {
          type: "string",
          description: "Path to the file relative to workspace root",
        },
        content: {
          type: "string",
          description: "Content to write to the file",
        },
      },
      required: ["filepath", "content"],
    },
  },
  {
    name: "list_directory",
    description: "List files and directories in a given path",
    inputSchema: {
      type: "object",
      properties: {
        dirpath: {
          type: "string",
          description: "Directory path relative to workspace root (default: root)",
        },
      },
    },
  },
  {
    name: "search_files",
    description: "Search for text patterns in files using grep",
    inputSchema: {
      type: "object",
      properties: {
        pattern: {
          type: "string",
          description: "Text pattern to search for",
        },
        file_pattern: {
          type: "string",
          description: "File pattern to search in (e.g., '*.js', '*.py')",
        },
      },
      required: ["pattern"],
    },
  },
  {
    name: "git_status",
    description: "Get current git repository status",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "git_diff",
    description: "Show git diff for staged or unstaged changes",
    inputSchema: {
      type: "object",
      properties: {
        staged: {
          type: "boolean",
          description: "Show staged changes (default: false)",
        },
        filepath: {
          type: "string",
          description: "Specific file to diff (optional)",
        },
      },
    },
  },
  {
    name: "git_commit",
    description: "Create a git commit with a message",
    inputSchema: {
      type: "object",
      properties: {
        message: {
          type: "string",
          description: "Commit message",
        },
        add_all: {
          type: "boolean",
          description: "Stage all changes before committing (default: false)",
        },
      },
      required: ["message"],
    },
  },
  {
    name: "git_log",
    description: "Show recent git commit history",
    inputSchema: {
      type: "object",
      properties: {
        limit: {
          type: "number",
          description: "Number of commits to show (default: 10)",
        },
      },
    },
  },
  {
    name: "run_command",
    description: "Execute a shell command in the workspace (use carefully)",
    inputSchema: {
      type: "object",
      properties: {
        command: {
          type: "string",
          description: "Shell command to execute",
        },
      },
      required: ["command"],
    },
  },
  {
    name: "analyze_code",
    description: "Analyze code structure and provide insights",
    inputSchema: {
      type: "object",
      properties: {
        filepath: {
          type: "string",
          description: "Path to the code file to analyze",
        },
      },
      required: ["filepath"],
    },
  },
  {
    name: "create_file_structure",
    description: "Create multiple files and directories at once",
    inputSchema: {
      type: "object",
      properties: {
        structure: {
          type: "object",
          description: "Object describing the file structure to create",
        },
      },
      required: ["structure"],
    },
  },
];

// Initialize MCP server
const server = new Server(
  {
    name: "coding-assistant-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Helper function to resolve paths safely
function resolvePath(relativePath) {
  const resolved = path.resolve(WORKSPACE_ROOT, relativePath);
  if (!resolved.startsWith(WORKSPACE_ROOT)) {
    throw new Error("Access denied: Path outside workspace");
  }
  return resolved;
}

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "read_file": {
        const filepath = resolvePath(args.filepath);
        const content = await fs.readFile(filepath, "utf-8");
        return {
          content: [{ type: "text", text: content }],
        };
      }

      case "write_file": {
        const filepath = resolvePath(args.filepath);
        await fs.mkdir(path.dirname(filepath), { recursive: true });
        await fs.writeFile(filepath, args.content, "utf-8");
        return {
          content: [
            { type: "text", text: `Successfully wrote to ${args.filepath}` },
          ],
        };
      }

      case "list_directory": {
        const dirpath = args.dirpath
          ? resolvePath(args.dirpath)
          : WORKSPACE_ROOT;
        const entries = await fs.readdir(dirpath, { withFileTypes: true });
        const formatted = entries
          .map((entry) => `${entry.isDirectory() ? "📁" : "📄"} ${entry.name}`)
          .join("\n");
        return {
          content: [{ type: "text", text: formatted }],
        };
      }

      case "search_files": {
        const pattern = args.pattern;
        const filePattern = args.file_pattern || "*";
        const { stdout } = await execAsync(
          `grep -r "${pattern}" --include="${filePattern}" .`,
          { cwd: WORKSPACE_ROOT }
        );
        return {
          content: [{ type: "text", text: stdout || "No matches found" }],
        };
      }

      case "git_status": {
        const { stdout } = await execAsync("git status", {
          cwd: WORKSPACE_ROOT,
        });
        return {
          content: [{ type: "text", text: stdout }],
        };
      }

      case "git_diff": {
        const staged = args.staged ? "--staged" : "";
        const filepath = args.filepath ? (args.filepath) : "";
        const { stdout } = await execAsync(`git diff ${staged} ${filepath}`, {
          cwd: WORKSPACE_ROOT,
        });
        return {
          content: [{ type: "text", text: stdout || "No changes to show" }],
        };
      }

      case "git_commit": {
        if (args.add_all) {
          await execAsync("git add -A", { cwd: WORKSPACE_ROOT });
        }
        const { stdout } = await execAsync(
          `git commit -m "${args.message}"`,
          { cwd: WORKSPACE_ROOT }
        );
        return {
          content: [{ type: "text", text: stdout }],
        };
      }

      case "git_log": {
        const limit = args.limit || 10;
        const { stdout } = await execAsync(
          `git log --oneline -n ${limit}`,
          { cwd: WORKSPACE_ROOT }
        );
        return {
          content: [{ type: "text", text: stdout }],
        };
      }

      case "run_command": {
        const { stdout, stderr } = await execAsync(args.command, {
          cwd: WORKSPACE_ROOT,
        });
        return {
          content: [
            { type: "text", text: `STDOUT:\n${stdout}\n\nSTDERR:\n${stderr}` },
          ],
        };
      }

      case "analyze_code": {
        const filepath = resolvePath(args.filepath);
        const content = await fs.readFile(filepath, "utf-8");
        const lines = content.split("\n");
        const stats = {
          total_lines: lines.length,
          non_empty_lines: lines.filter((l) => l.trim()).length,
          functions: (content.match(/function\s+\w+|const\s+\w+\s*=/g) || [])
            .length,
          imports: (content.match(/^import\s+/gm) || []).length,
          exports: (content.match(/^export\s+/gm) || []).length,
        };
        return {
          content: [{ type: "text", text: JSON.stringify(stats, null, 2) }],
        };
      }

      case "create_file_structure": {
        const structure = args.structure;
        
        async function createStructure(obj, basePath) {
          for (const [key, value] of Object.entries(obj)) {
            const fullPath = resolvePath(path.join(basePath, key));
            
            if (typeof value === "string") {
              // It's a file
              await fs.mkdir(path.dirname(fullPath), { recursive: true });
              await fs.writeFile(fullPath, value, "utf-8");
            } else if (typeof value === "object") {
              // It's a directory
              await fs.mkdir(fullPath, { recursive: true });
              await createStructure(value, path.join(basePath, key));
            }
          }
        }
        
        await createStructure(structure, "");
        return {
          content: [
            { type: "text", text: "File structure created successfully" },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Coding Assistant MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
