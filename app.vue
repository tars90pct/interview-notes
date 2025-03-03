<template>
  <NuxtLayout>
    <NuxtPage></NuxtPage>
    <div
      class="hidden"
      :class="{
        [data.version]: true,
      }"
    ></div>
  </NuxtLayout>
</template>
<script lang="ts">
  import { defineComponent, onMounted } from "vue";

  export default defineComponent({
    components: {},
    setup() {
      const version = useRuntimeConfig().public.version as string;
      const i18n = useI18n();
      i18n.setLocale("zh-tw");

      useHead({
        title: "Interview Notes",
        meta: [{ name: "Interview Notes", content: "" }],
        bodyAttrs: {
          class: "",
        },
        script: [],
      });
      definePageMeta({
        layout: false,
      });
      onMounted(() => {});
      return buildDefineComponentSetup(
        {
          data: {
            version,
          },
          methods: {},
          stores: {},
        },
        {}
      );
    },
  });
</script>
<style lang="postcss">
  body {
    @apply m-0 !important;
    @apply h-screen !important;
    @apply select-auto !important;
    font-family: "Noto Sans TC", serif;
  }
</style>
