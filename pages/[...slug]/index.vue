<template>
  <div class="flex flex-col gap-3 p-4">
    <UiBreadcrumbs :items="data.crumbs" class="hidden md:flex" />
    <div class="flex h-[calc(100dvh-129px)] w-full flex-col overflow-x-auto p-4">
      <MDC
        :key="markdown"
        class="prose max-w-none flex-1 dark:prose-invert [&>h2>a]:no-underline [&>h3>a]:no-underline"
        :value="markdown"
        tag="article"
      />
      <div class="flex flex-row items-center justify-center gap-2 pt-4">
        <div class="cursor-pointer" v-if="data.prevPage">
          <a
            @click="
              () => {
                methods.goTo(data.prevPage);
              }
            "
            >Prev</a
          >
        </div>
        <div class="cursor-pointer" v-if="data.nextPage">
          <a
            @click="
              () => {
                methods.goTo(data.nextPage);
              }
            "
            >Next</a
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
  import { constructSyntax, MarkdownFileCodes, useI18n, useRoute } from "#imports";
  import { usePageStore } from "~/stores/page";
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent, onMounted, ref, watch } from "vue";
  import type { Crumbs } from "~/components/Ui/Breadcrumbs.vue";

  export default defineComponent({
    components: {},
    props: {},
    async setup(props) {
      definePageMeta({
        layout: "official-layout",
      });
      onMounted(async () => {
        const protocol = window.location.protocol;
        const hostname = window.location.hostname;
        const port = window.location.port ? `:${window.location.port}` : "";
        const fullUrl = `${protocol}//${hostname}${port}`;
        const baseURL = `${fullUrl}${useRuntimeConfig().app.baseURL}`;

        let text = (await $fetch(`/markdown/${i18n.getLocaleCookie()}/${pageMeta.getLink()}.md`, {
          responseType: "text",
        })) as string;
        markdown.value = text.replace("{{BASEURL}}", baseURL);
        findFiles(MarkdownFileCodes.LEETCODE, markdown.value).forEach(async (path) => {
          const content = await fetchLeetcode(baseURL, path);
          if (content) {
            const target = constructSyntax(MarkdownFileCodes.LEETCODE, path);
            const escapedTarget = target.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");
            const regexTarget = new RegExp(escapedTarget, "g");

            markdown.value = markdown.value.replace(regexTarget, content);
          }
        });
        findFiles(MarkdownFileCodes.FILE, markdown.value).forEach(async (path) => {
          const content = await fetchFile(baseURL, path);

          if (content) {
            const target = constructSyntax(MarkdownFileCodes.FILE, path);
            const escapedTarget = target.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");

            const regexTarget = new RegExp(escapedTarget, "g");
            markdown.value = markdown.value.replace(regexTarget, content);
          }
        });
      });
      const i18n = useI18n();
      const route = useRoute();
      const router = useRouter();
      const markdown = ref<string>("");
      const pageStore = usePageStore();
      const paths = route.params.slug as string[];
      const pageMeta = pageStore.getPageMeta(paths)!;
      if (!pageMeta) {
        router.push("/");
      }
      const pageKey = paths.join("/");
      const pageIndexes = pageStore.pagesIndex;
      const currentPageIndex = pageIndexes.indexOf(pageKey);
      const nextPage =
        currentPageIndex + 1 >= pageIndexes.length ? "" : `/${pageIndexes[currentPageIndex + 1]}`;
      const prevPage = currentPageIndex - 1 >= 0 ? `/${pageIndexes[currentPageIndex - 1]}` : "";
      const goTo = (path: string) => {
        router.push(path);
      };

      const crumbs: Crumbs[] = [
        {
          link: "/",
          icon: "lucide:home",
        },
        ...paths.map((key, index) => {
          return {
            label: i18n.t(key),
            link: `/${paths.slice(0, index + 1).join("/")}`,
          };
        }),
      ];

      return buildDefineComponentSetup(
        {
          data: {
            crumbs,
            nextPage,
            prevPage,
          },
          methods: {
            goTo,
          },
          stores: {},
        },
        {
          markdown,
        }
      );
    },
  });
</script>

<style lang="postcss" scoped>
  .prose h2 a,
  .prose h3 a,
  .prose h4 a,
  .prose h5 a {
    text-decoration: none !important;
  }
  a {
    text-decoration: none !important;
  }
</style>
