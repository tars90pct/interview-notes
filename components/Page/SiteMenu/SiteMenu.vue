<template>
  <div class="flex flex-col gap-2">
    <PageSiteMenuItem :page-meta="pageMeta" v-for="pageMeta of $props.pageMetas" />
  </div>
</template>
<script lang="ts">
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent } from "vue";
  import type { NuxtError } from "#app";
  import type { PageMeta } from "~/types/Page";

  export default defineComponent({
    components: {},
    props: {
      pageMetas: {
        type: Object as () => PageMeta[],
        default: () => {
          return [];
        },
      },
      error: {
        type: Object as () => NuxtError,
        default: () => {
          return {
            statusCode: 404,
          };
        },
      },
    },
    setup(props) {
      return buildDefineComponentSetup(
        {
          data: {},
          methods: {},
          stores: {},
        },
        {}
      );
    },
  });
</script>
