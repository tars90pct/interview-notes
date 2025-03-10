<template>
  <div class="min-h-screen w-screen overflow-y-hidden">
    <header
      class="sticky left-0 top-0 z-50 flex w-full flex-row border-b border-solid bg-background/80 backdrop-blur"
    >
      <div class="flex h-16 w-full flex-row items-center gap-1 px-8 py-4">
        <UiDrawer should-scale-background>
          <UiDrawerTrigger as-child>
            <UiButton size="icon-sm" variant="outline" class="md:hidden">
              <Icon name="material-symbols-light:menu" class="size-5" />
            </UiButton>
          </UiDrawerTrigger>
          <UiDrawerContent>
            <LazyPageSiteMenu :page-metas="data.sideMenus" class="overflow-x-auto p-2" />
            <UiDrawerClose class="absolute right-4 top-3 h-7 w-7" as-child>
              <UiButton variant="ghost" size="icon-sm" class="opacity-50 hover:opacity-100">
                <Icon name="lucide:x" />
              </UiButton>
            </UiDrawerClose>
          </UiDrawerContent>
        </UiDrawer>
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
    <main class="grid md:grid-cols-[290px_minmax(0,1fr)]">
      <div class="hidden h-[calc(100dvh-69px)] overflow-y-auto border-r md:block">
        <LazyPageSiteMenu :page-metas="data.sideMenus" class="p-2" />
      </div>
      <div class="h-[calc(100dvh-69px)] w-full overflow-y-hidden">
        <slot />
      </div>
    </main>
  </div>
</template>
<script lang="ts">
  import pages from "~/assets/pages/index.json";
  import { useBrowserStore } from "~/stores/broswer";
  import { PageMeta } from "~/types/Page";
  import { buildDefineComponentSetup } from "~/utils/internal";

  export default defineComponent({
    components: {},
    setup() {
      definePageMeta({
        layout: false,
      });
      const broswerStore = useBrowserStore();
      const i18n = useI18n();
      i18n.setLocaleCookie("zh-tw");
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
