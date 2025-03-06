export enum MarkdownFileCodes {
  LEETCODE = "LEETCODE",
  FILE = "FILE",
}
export function findFiles(base: MarkdownFileCodes, text: string): string[] {
  const regex = new RegExp(`\\{\\{${base}\\|([^}]+)\\}\\}`, "g");
  let matches: string[] = [];
  let match;

  while ((match = regex.exec(text)) !== null) {
    matches.push(match[1]);
  }

  return matches;
}

export const fetchLeetcode = async (baseUrl: string, path: string): Promise<string> => {
  const text = (await $fetch(`${baseUrl}/${path}`, {
    responseType: "text",
  })) as string;
  const regex = /# @lc code=start([\s\S]*?)# @lc code=end/;
  const match = text.match(regex);
  return match ? match[1].trim() : "";
};

export const fetchFile = async (baseUrl: string, path: string): Promise<string> => {
  const text = (await $fetch(`${baseUrl}/${path}`, {
    responseType: "text",
  })) as string;
  return text;
};

export function constructSyntax(base: MarkdownFileCodes, path: string): string {
  return `{{${base}|${path}}}`;
}
