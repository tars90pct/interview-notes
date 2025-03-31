<template>
  <div class="flex h-screen w-full items-center justify-center">
    <Icon name="eos-icons:bubble-loading" size="48" />
  </div>
</template>
<script lang="ts" setup>
  import link from "@nuxtjs/mdc/runtime/parser/handlers/link";
  import { navigateTo } from "#app";
  import { usePageStore } from "#imports";
  import { PageMeta } from "~/types/Page";
  import { routes } from "vue-router/auto-routes";

  const route = useRoute();
  const pageStore = usePageStore();

  onMounted(() => {
    const link = route.query.link as string;
    if (!link) {
      navigateTo("/");
    }
    const index = Number(link);
    if (isNaN(index)) {
      navigateTo("/");
    }
    if (index < 0 || index >= pageStore.pagesIndex.length) {
      navigateTo("/");
    }
    navigateTo(pageStore.pagesIndex[index]);
  });
</script>
