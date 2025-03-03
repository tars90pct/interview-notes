import { useColorMode } from "@vueuse/core";
import { defineStore } from "pinia";

const COLOR_MODE = "COLOR_MODE";

export const useBrowserStore = defineStore("browser", {
  state: () => {
    const c = useColorMode();
    c.value = (localStorage.getItem(COLOR_MODE) || "light") as "light" | "dark";
    return {
      colorMode: c.value,
      screenWidth: 0,
      screenHeight: 0,
    };
  },
  actions: {
    getColorMode(): "light" | "dark" {
      const colorMode = localStorage.getItem(COLOR_MODE);
      if (!colorMode) {
        this.setColorMode("light");
      }
      return localStorage.getItem(COLOR_MODE) as "light" | "dark";
    },
    setColorMode(colorMode: "light" | "dark") {
      this.colorMode = colorMode;
      localStorage.setItem(COLOR_MODE, colorMode);
      const c = useColorMode();
      c.value = colorMode;
    },
  },
});
