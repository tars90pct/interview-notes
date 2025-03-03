import { defineStore } from "pinia";
import pageIndex from "~/assets/pages/index.json";
import { PageMeta } from "~/types/Page";

function flattenPageMetas(pages: PageMeta[]): PageMeta[] {
  return pages.flatMap((page) => {
    const flattenedChildren = flattenPageMetas(page.children);
    return [page, ...flattenedChildren];
  });
}

export const usePageStore = defineStore("page", {
  state: () => {
    const pages = PageMeta.OfArray(pageIndex, []);
    const pageLookup = new Map(
      flattenPageMetas(pages).map((page) => {
        return [page.getLink(), page];
      })
    );
    return {
      pages,
      pageLookup,
    };
  },
  actions: {
    getPageMeta(paths: string[]) {
      return this.pageLookup.get(paths.join("/"));
    },
  },
});
