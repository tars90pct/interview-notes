export function copyToClipboard(text: string) {
  return navigator.clipboard.writeText(text);
}

export function formatUnixTimestamp(unixTimestamp: number) {
  const dateObject = new Date(unixTimestamp * 1000);

  // Use the toLocaleString method with options for formatting
  const year = dateObject.getFullYear();
  const month = String(dateObject.getMonth() + 1).padStart(2, "0");
  const day = String(dateObject.getDate()).padStart(2, "0");
  const hours = String(dateObject.getHours()).padStart(2, "0");
  const minutes = String(dateObject.getMinutes()).padStart(2, "0");
  const seconds = String(dateObject.getSeconds()).padStart(2, "0");

  return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}

export function getUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
}

export function isValidJSON(str: string): boolean {
  try {
    JSON.parse(str);
    return true;
  } catch (error) {
    return false;
  }
}

export function parseJSON(str: string): any {
  try {
    return JSON.parse(str);
  } catch (error) {
    return {} as any;
  }
}

export function isFloat(n: any) {
  const fn = parseFloat(n);
  return Number(fn) === fn && fn % 1 !== 0;
}

export function isInteger(n: any) {
  const value = parseInt(n);
  return Number(value) === value && value % 1 === 0;
}
