import pageIndex from "~/assets/pages/index.json";
import { PageMeta } from "~/types/Page";
import { defineStore } from "pinia";

function flattenPageMetas(pages: PageMeta[]): PageMeta[] {
  return pages.flatMap((page) => {
    const flattenedChildren = flattenPageMetas(page.children);
    return [page, ...flattenedChildren];
  });
}

export const usePageStore = defineStore("page", {
  state: () => {
    const pages = PageMeta.OfArray(pageIndex, []);
    const flattenPageMeta = flattenPageMetas(pages);
    const pagesIndex = flattenPageMeta.map((page) => {
      return page.getLink();
    });
    const pageLookup = new Map(
      flattenPageMeta.map((page) => {
        return [page.getLink(), page];
      })
    );
    return {
      pages,
      pageLookup,
      pagesIndex,
    };
  },
  actions: {
    getPageMeta(paths: string[]) {
      return this.pageLookup.get(paths.join("/"));
    },
  },
});
