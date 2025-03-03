<template>
  <div class="flex w-full flex-col">
    <UiButton
      class="flex w-full items-center justify-between rounded-md px-3 py-2 hover:bg-accent"
      :class="{
        'bg-accent': isActive,
      }"
      variant="ghost"
      @click="methods.link"
    >
      <div class="flex items-center gap-2.5">
        <Icon :name="$props.pageMeta.icon" v-if="$props.pageMeta.icon" class="size-4" />
        <div v-else class="size-4" />
        <span>{{ $t($props.pageMeta.key) }}</span>
      </div>
      <Icon
        name="i-lucide:chevron-down"
        v-if="!open && $props.pageMeta.children && $props.pageMeta.children.length > 0"
        class="size-4"
        @click="open = !open"
      />
      <Icon
        name="i-lucide:chevron-up"
        v-if="open && $props.pageMeta.children && $props.pageMeta.children.length > 0"
        class="size-4"
        @click="open = !open"
      />
    </UiButton>
    <SiteMenuItem
      v-for="pageMeta of $props.pageMeta.children"
      :page-meta="pageMeta"
      v-if="open && $props.pageMeta.children && $props.pageMeta.children.length > 0"
    />
  </div>
</template>
<script lang="ts">
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent } from "vue";
  import type { PageMeta } from "~/types/Page";

  export default defineComponent({
    components: {},
    props: {
      pageMeta: {
        type: Object as () => PageMeta,
        required: true,
      },
    },
    setup(props) {
      const open = ref(true);
      const router = useRouter();
      const route = useRoute();
      const isActive = ref(false);

      // methods
      const link = () => {
        router.push(`/${props.pageMeta.getLink()}`);
      };
      const checkActive = () => {
        const slugs = route.params.slug as string[];
        if (slugs) {
          const slug = slugs.join("/");
          const path = [...props.pageMeta.paths, props.pageMeta.key].join("/");
          return slug == path;
        }
        return false;
      };
      isActive.value = checkActive();
      watch(
        () => route.fullPath,
        (newPath) => {
          isActive.value = checkActive();
        }
      );
      return buildDefineComponentSetup(
        {
          data: {},
          methods: {
            link,
          },
          stores: {},
        },
        {
          open,
          isActive,
        }
      );
    },
  });
</script>
