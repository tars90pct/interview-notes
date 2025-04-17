import { PageMeta } from "~/types/Page";
import { defineStore } from "pinia";

export const PAGE_INDEX = [
  {
    key: "getting-started",
    icon: "material-symbols-light:rocket-launch-outline-rounded",
  },
  {
    key: "system-design",
    icon: "material-symbols-light:design-services-rounded",
    children: [
      {
        key: "delivery-framework",
        icon: "carbon:idea",
      },
      {
        key: "classic",
        icon: "carbon:idea",
        children: [
          {
            key: "design-a-distributed-metrics-logging-and-aggregation-system",
          },
          {
            key: "design-a-distributed-stream-processing-system-like-kafka",
          },
          {
            key: "design-a-key-value-store",
          },
          {
            key: "design-the-k-most-shared-articles-in-various-time-windows",
          },
          {
            key: "design-an-api-rate-limiter",
          },
          {
            key: "design-a-google-calendar",
          },
          {
            key: "design-a-distributed-queue-like-rabbitmq",
          },
        ],
      },
      {
        key: "core-concepts",
        icon: "carbon:idea",
        children: [
          {
            key: "scaling",
          },
          {
            key: "cap-theorem",
          },
          {
            key: "locking",
          },
          {
            key: "indexing",
          },
          {
            key: "communication-protocols",
          },
          {
            key: "security",
          },
        ],
      },
      {
        key: "key-technologies",
        icon: "carbon:idea",
        children: [
          {
            key: "database",
          },
          {
            key: "api-gateway",
          },
          {
            key: "load-balancer",
          },
          {
            key: "queue",
          },
          {
            key: "streams-event-sourcing",
          },
          {
            key: "distributed-lock",
          },
          {
            key: "distributed-cache",
          },
          {
            key: "cdn",
          },
        ],
      },
    ],
  },
  {
    key: "problem-solving",
    icon: "hugeicons:leetcode",
    children: [
      {
        key: "prefix-sum",
        icon: "carbon:idea",
        children: [
          {
            key: "303.range-sum-query-immutable",
          },
          {
            key: "525.contiguous-array",
          },
          {
            key: "560.subarray-sum-equals-k",
          },
        ],
      },
      {
        key: "two-pointers",
        icon: "carbon:idea",
        children: [
          {
            key: "15.3-sum",
          },
          {
            key: "11.container-with-most-water",
          },
          {
            key: "27.remove-element",
          },
          {
            key: "344.reverse-string",
          },
          {
            key: "209.minimum-size-subarray-sum",
          },
        ],
      },
      {
        key: "linked-list",
        icon: "carbon:idea",
        children: [
          {
            key: "206.reverse-linked-list",
          },
          {
            key: "21.merge-two-sorted-lists",
          },
          {
            key: "82.remove-duplicates-from-sorted-list-ii",
          },
          {
            key: "83.remove-duplicates-from-sorted-list",
          },
          {
            key: "86.partition-list",
          },
          {
            key: "138.copy-list-with-random-pointer",
          },
          {
            key: "141.linked-list-cycle",
          },
          {
            key: "142.linked-list-cycle-ii",
          },
          {
            key: "143.reorder-list",
          },
          {
            key: "148.sort-list",
          },
          {
            key: "234.palindrome-linked-list",
          },
        ],
      },
      {
        key: "tree",
        icon: "carbon:idea",
        children: [
          {
            key: "144.binary-tree-preorder-traversal",
          },
          {
            key: "145.binary-tree-postorder-traversal",
          },
          {
            key: "94.binary-tree-inorder-traversal",
          },
          {
            key: "102.binary-tree-level-order-traversal",
          },
          {
            key: "107.binary-tree-level-order-traversal-ii",
          },
          {
            key: "199.binary-tree-right-side-view",
          },
          {
            key: "637.average-of-levels-in-binary-tree",
          },
          {
            key: "429.n-ary-tree-level-order-traversal",
          },
          {
            key: "515.find-largest-value-in-each-tree-row",
          },
          {
            key: "116.populating-next-right-pointers-in-each-node",
          },
          {
            key: "117.populating-next-right-pointers-in-each-node-ii",
          },
          {
            key: "104.maximum-depth-of-binary-tree",
          },
          {
            key: "111.minimum-depth-of-binary-tree",
          },
          {
            key: "226.invert-binary-tree",
          },
          {
            key: "101.symmetric-tree",
          },
          {
            key: "222.count-complete-tree-nodes",
          },
          {
            key: "110.balanced-binary-tree",
          },
          {
            key: "257.binary-tree-paths",
          },
          {
            key: "404.sum-of-left-leaves",
          },
          {
            key: "513.find-bottom-left-tree-value",
          },
          {
            key: "112.path-sum",
          },
          {
            key: "106.construct-binary-tree-from-inorder-and-postorder-traversal",
          },
          {
            key: "654.maximum-binary-tree",
          },
          {
            key: "700.search-in-a-binary-search-tree",
          },
          {
            key: "98.validate-binary-search-tree",
          },
          {
            key: "530.minimum-absolute-difference-in-bst",
          },
          {
            key: "501.find-mode-in-binary-search-tree",
          },
          {
            key: "236.lowest-common-ancestor-of-a-binary-tree",
          },
          {
            key: "235.lowest-common-ancestor-of-a-binary-search-tree",
          },
          {
            key: "450.delete-node-in-a-bst",
          },
          {
            key: "669.trim-a-binary-search-tree",
          },
          {
            key: "538.convert-bst-to-greater-tree",
          },
        ],
      },
      {
        key: "backtracking",
        icon: "carbon:idea",
        children: [],
      },
    ],
  },
  {
    key: "services",
    icon: "icons8:services",
    children: [{ key: "elasticsearch" }],
  },
  {
    key: "contact",
    icon: "grommet-icons:contact",
  },
];

function flattenPageMetas(pages: PageMeta[]): PageMeta[] {
  return pages.flatMap((page) => {
    const flattenedChildren = flattenPageMetas(page.children);
    return [page, ...flattenedChildren];
  });
}

export const usePageStore = defineStore("page", {
  state: () => {
    const pages = PageMeta.OfArray(PAGE_INDEX, []);
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
