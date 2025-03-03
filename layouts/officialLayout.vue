<template>
  <div class="min-h-screen w-screen">
    <header
      class="bg-background/80 sticky left-0 top-0 z-50 flex w-full flex-row border-b border-solid backdrop-blur"
    >
      <div class="flex h-16 w-full flex-row items-center gap-1 px-8 py-4">
        <div class="flex-1 text-lg font-bold">{{ $t("Interview Notes") }}</div>
        <div></div>
        <UiDropdownMenu>
          <UiDropdownMenuTrigger as-child>
            <UiButton size="icon-sm" variant="outline">
              <Icon
                class="size-5"
                name="material-symbols-light:light-mode-outline"
                v-if="stores.broswerStore.getColorMode() === 'light'"
              />
              <Icon
                class="size-5"
                name="material-symbols-light:dark-mode-outline"
                v-if="stores.broswerStore.getColorMode() === 'dark'"
              />
            </UiButton>
          </UiDropdownMenuTrigger>
          <UiDropdownMenuContent class="w-24">
            <UiDropdownMenuItem
              :title="$t('Light Mode')"
              icon="material-symbols-light:light-mode-outline"
              @click="
                () => {
                  stores.broswerStore.setColorMode('light');
                }
              "
            />
            <UiDropdownMenuItem
              :title="$t('Dark Mode')"
              icon="material-symbols-light:dark-mode-outline"
              @click="
                () => {
                  stores.broswerStore.setColorMode('dark');
                }
              "
            />
          </UiDropdownMenuContent>
        </UiDropdownMenu>
      </div>
    </header>
    <main class="grid grid-cols-[290px_minmax(0,1fr)]">
      <div class="h-[calc(100dvh-65px)] border-r">
        <LazyPageSiteMenu :page-metas="data.sideMenus" class="p-2" />
      </div>
      <div class="h-[calc(100dvh-65px)] w-full">
        <slot />
      </div>
    </main>
  </div>
</template>
<script lang="ts">
  import { useBrowserStore } from "~/stores/broswer";
  import { buildDefineComponentSetup } from "~/utils/internal";
  import pages from "~/assets/pages/index.json";
  import { PageMeta } from "~/types/Page";

  export default defineComponent({
    components: {},
    setup() {
      definePageMeta({
        layout: false,
      });
      const broswerStore = useBrowserStore();
      const sideMenus = PageMeta.OfArray(pages, []);
      return buildDefineComponentSetup(
        {
          data: {
            sideMenus,
          },
          methods: {},
          stores: {
            broswerStore,
          },
        },
        {}
      );
    },
  });
</script>
